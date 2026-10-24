#!/usr/bin/env python3
"""AJST-Data 审核队列 / 认领工具（纯标准库，零第三方依赖）。

职责：
  1) 从仓库文件（`info/*.json` 的 `extra_data.audit`、`lc/*.csv` 行数）与认领快照
     （`audit/state.tsv`）派生每个源的审核状态；
  2) 给出**确定性**的可认领队列 —— 同一份仓库，任何人、任何机器算出同一结果；
  3) 生成认领快照（唯一写入方；由 `.github/workflows/audit-snapshot.yml` 每日调用）。

状态机（与 README / 提示词一致）：
  reviewed    info 里 `extra_data.audit.status == "reviewed"`（已合并）
  in-review   有 open 非 draft PR 改了该源
  claimed     有 open draft PR 改了该源（"开工即开 draft claim PR"）
  stale-pr / stale-claim
              上述 PR 超过 TTL 无更新（巨源 30 天，其余 14 天）——软过期，可接手
  reserved    维护者自留（`audit/reserved.tsv`，人工维护，不是 PR 认领）→ **不得认领**
  reserved-expired
              预留已过 `until` → 软过期，按 48 h 沟通协议可接手
  free        以上都不是 → 可认领
  带 `?` 后缀 认领信息来自过期快照，未实时确认（只作"可能被占用"用）

线索卡（`audit/leads/<源ID>.md`，人工维护）**只读取、只展示**：它记录别人审别的文献时
顺带发现的同一目标的资料，**不参与上面的状态机**——有线索卡不等于被认领，更不等于已审核。

用法 / Usage:
  python3 tools/audit_queue.py --limit 20              # 可认领队列（代价升序）
  python3 tools/audit_queue.py --bucket 1/4 --limit 50 # 确定性分片，多人互不重叠
  python3 tools/audit_queue.py --id GRB130427A         # 单源状态与依据（含线索卡）
  python3 tools/audit_queue.py --leads                 # 列出全部线索卡（多目标文献交接）
  python3 tools/audit_queue.py --reserved              # 列出维护者预留（自留源，外部不得认领）
  python3 tools/audit_queue.py --check-reserved        # PR 守卫：改动文件是否触及自留源（警告级）
  python3 tools/audit_queue.py --pack 3 --limit 9      # 按批打包（3 源/批）
  python3 tools/audit_queue.py --live                  # 实时查 gh（判据）
  python3 tools/audit_queue.py --emit-snapshot         # 原子写 audit/state.tsv

退出码：0 正常；2 取数失败（`gh` 不可用/失败，快照文件未被触碰）；3 写入失败。
"""
import argparse
import fnmatch
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INFO_DIR = os.path.join(ROOT, 'info')
LC_DIR = os.path.join(ROOT, 'lc')
SNAPSHOT = os.path.join(ROOT, 'audit', 'state.tsv')
LEADS_DIR = os.path.join(ROOT, 'audit', 'leads')
PAPER_DIR = os.path.join(LEADS_DIR, 'papers')   # 文献级索引卡：一篇多源文献一张，不参与状态机
RCARD_MIN_WARN = 5          # 同一 PR 新增源级卡 ≥ 此数且无文献级卡 → 提示改用文献级卡（§3.11）
PAPER_KEYS = ('paper_key', 'paper', 'date', 'helper', 'sources', 'out_of_repo')
RESERVED_TSV = os.path.join(ROOT, 'audit', 'reserved.tsv')
DENIED_TSV = os.path.join(ROOT, 'audit', 'denied.tsv')   # 已否证源清单（人写、工具只读）
DENIED_COLS = ('source_id', 'reason_code', 'evidence', 'decided_by', 'date', 'ref')
DENIED_REASONS = ('retracted', 'duplicate', 'noise', 'other')

SNAPSHOT_STALE_DAYS = 3     # 快照超过这个天数即视为过期（工具会告警）
CLAIM_TTL_DAYS = 14         # 普通源的认领软过期
GIANT_ROWS = 1000           # 超过这么多行的源算"巨源"
GIANT_TTL_DAYS = 30         # 巨源的认领软过期
GH_TIMEOUT = 60

REVIEWED = 'reviewed'
IN_REVIEW = 'in-review'
CLAIMED = 'claimed'
RESERVED = 'reserved'
RESERVED_EXPIRED = 'reserved-expired'
FREE = 'free'

GH_JSON_FIELDS = 'number,title,isDraft,files,createdAt,updatedAt,author'
GH_JSON_FIELDS_NOFILES = 'number,title,isDraft,createdAt,updatedAt,author'


# ─── 基础工具 ────────────────────────────────────────────────────────────────
def now_utc():
    return datetime.now(timezone.utc)


def parse_iso(s):
    """解析 ISO8601；无时区的（如 '2026-07-10'）按 UTC 处理，避免 naive/aware 混算。"""
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(str(s).replace('Z', '+00:00'))
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def days_since(dt, ref=None) -> float:
    """dt 必须是 datetime（调用方先判空）。返回相对 ref（默认现在）的天数。"""
    return ((ref or now_utc()) - dt).total_seconds() / 86400.0


def ttl_days(rows):
    return GIANT_TTL_DAYS if (rows or 0) > GIANT_ROWS else CLAIM_TTL_DAYS


def bucket_of(source_id, n):
    """确定性分片：sha1(id) % n。与当前认领状况无关，因此分片随时间稳定。"""
    return int(hashlib.sha1(source_id.encode('utf-8')).hexdigest(), 16) % n


def bucket_index(source_id, n):
    return bucket_of(source_id, n) + 1        # 对外用 1..N


# ─── 仓库侧数据 ──────────────────────────────────────────────────────────────
def load_sources():
    """→ {id: {id, rows, audit, audit_status}}；rows=0 表示纯信息源（无 lc）。"""
    out = {}
    if os.path.isdir(INFO_DIR):
        for f in sorted(os.listdir(INFO_DIR)):
            if not f.endswith('.json'):
                continue
            sid = f[:-5]
            try:
                with open(os.path.join(INFO_DIR, f), encoding='utf-8') as fh:
                    d = json.load(fh)
            except Exception:
                d = {}
            ed = d.get('extra_data') if isinstance(d, dict) else None
            audit = ed.get('audit') if isinstance(ed, dict) else None
            if not isinstance(audit, dict):
                audit = None
            out[sid] = {'id': sid, 'rows': None, 'audit': audit,
                        'audit_status': str((audit or {}).get('status') or '').strip().lower()}
    if os.path.isdir(LC_DIR):
        for f in os.listdir(LC_DIR):
            if not f.endswith('.csv'):
                continue
            sid = f[:-4]
            try:
                with open(os.path.join(LC_DIR, f), 'rb') as fh:
                    data = fh.read()
            except OSError:
                continue
            lines = data.count(b'\n') + (0 if (data.endswith(b'\n') or not data) else 1)
            rows = max(lines - 1, 0)          # 去掉表头
            out.setdefault(sid, {'id': sid, 'rows': 0, 'audit': None, 'audit_status': ''})
            out[sid]['rows'] = rows
    for v in out.values():
        if v['rows'] is None:
            v['rows'] = 0
    return out


def make_published_filter():
    """→ (is_published(sid)->bool, 说明)。只把"已进入公开仓库"的源放进队列。

    未发布源（本机 `.gitignore` 排除，如 `info/EP*.json`）不进队列：外部 agent 的
    clone 里没有这些文件，而且这些源名不该出现在可能被复制外传的输出里。
    """
    try:
        p = subprocess.run(['git', '-C', ROOT, 'ls-files', '-z', '--', 'info', 'lc'],
                           capture_output=True, text=True, timeout=180)
        if p.returncode == 0:
            tracked = set()
            for path in p.stdout.split('\0'):
                m = re.match(r'^(?:info|lc)/(.+)\.(?:json|csv)$', path.strip())
                if m:
                    tracked.add(m.group(1))
            if tracked:
                return (lambda sid: sid in tracked), f'git ls-files（{len(tracked)} 个已跟踪源）'
    except (OSError, subprocess.SubprocessError):
        pass
    try:
        with open(os.path.join(ROOT, '.gitignore'), encoding='utf-8') as fh:
            pats = [l.strip() for l in fh if l.strip() and not l.strip().startswith('#')]
    except OSError:
        return (lambda sid: True), '⚠ 无法判定是否已发布（git 与 .gitignore 都不可用）→ 未做过滤'

    def _pub(sid):
        return not any(fnmatch.fnmatch(f'info/{sid}.json', p)
                       or fnmatch.fnmatch(f'lc/{sid}.csv', p) for p in pats)

    return _pub, f'.gitignore 模式（{len(pats)} 条）'


# ─── 线索卡（audit/leads/，人工维护，不参与状态机）────────────────────────────
LEAD_KEYS = ('source_id', 'status', 'paper', 'pr', 'helper', 'date')
LEAD_KEY_RE = re.compile(r'^\s*[-*]?\s*([A-Za-z_]+)\s*[:：]\s*(.+?)\s*$')


def load_leads(dirpath=None):
    """→ {source_id: {rel, status, paper, pr, helper, date, ...}}

    文件名即源 id（`audit/leads/<源ID>.md`）。只解析第一个 `##` 标题之前的 key: value 行，
    格式契约见 `audit/leads/README.md`。工具必须离线可用，坏文件不抛异常，只记 parse_error。
    """
    out = {}
    d = dirpath or LEADS_DIR
    if not os.path.isdir(d):
        return out
    for fn in sorted(os.listdir(d)):
        if not fn.endswith('.md') or fn.lower() == 'readme.md':
            continue
        sid = fn[:-3]
        meta = {'rel': f'audit/leads/{fn}', 'file': os.path.join(d, fn)}
        try:
            with open(meta['file'], encoding='utf-8') as fh:
                for ln in fh:
                    if ln.startswith('##'):      # 元数据区到此结束
                        break
                    m = LEAD_KEY_RE.match(ln)
                    if m and m.group(1) in LEAD_KEYS and m.group(1) not in meta:
                        meta[m.group(1)] = m.group(2).strip()
        except OSError as e:
            meta['parse_error'] = str(e)
        if meta.get('source_id') and meta['source_id'] != sid:
            meta['mismatch'] = f'source_id={meta["source_id"]}≠文件名'
        out[sid] = meta
    return out


def split_ids(v):
    """把 `sources: GRB1, GRB2` 这类单元格拆成 id 列表；'无'/'-'/'' 视为空。"""
    raw = str(v or '')
    return [x.strip() for x in re.split(r'[,，;；\s]+', raw)
            if x.strip() and x.strip() not in ('无', '-', '—', 'none')]


def load_paper_cards(dirpath=None):
    """→ {paper_key: {rel, file, paper, date, helper, sources[], out_of_repo[]}}

    文献级索引卡 `audit/leads/papers/<paper_key>.md`：一篇多源文献一张，只承载索引，
    不参与状态机、不代替源级线索卡。只解析第一个 `##` 标题之前的 key: value 行；
    `sources:` 缺失时退回解析「涉及源一览」表格的第一列。坏文件不抛异常。
    契约见 `audit/leads/papers/README.md`。
    """
    out = {}
    d = dirpath or PAPER_DIR
    if not os.path.isdir(d):
        return out
    for fn in sorted(os.listdir(d)):
        if not fn.endswith('.md') or fn.lower() == 'readme.md':
            continue
        key = fn[:-3]
        meta = {'rel': f'audit/leads/papers/{fn}', 'file': os.path.join(d, fn),
                'sources': [], 'out_of_repo': []}
        try:
            with open(meta['file'], encoding='utf-8') as fh:
                txt = fh.read()
        except OSError as e:
            meta['parse_error'] = str(e)
            out[key] = meta
            continue
        head, _, body = txt.partition('\n##')
        for ln in head.splitlines():
            if ln.startswith('##'):
                break
            m = LEAD_KEY_RE.match(ln)
            if m and m.group(1) in PAPER_KEYS and m.group(1) not in meta:
                meta[m.group(1)] = m.group(2).strip()
        meta['sources'] = split_ids(meta.get('sources'))
        meta['out_of_repo'] = split_ids(meta.get('out_of_repo'))
        if not meta['sources']:
            for ln in body.splitlines():          # 退回表格：| 源 | 表号 | ...
                cells = [c.strip() for c in ln.strip().strip('|').split('|')]
                if len(cells) >= 2 and re.fullmatch(r'[A-Za-z]{2,6}\d{6}[A-Za-z]?', cells[0]):
                    meta['sources'].append(cells[0])
        if meta.get('paper_key') and meta['paper_key'] != key:
            meta['mismatch'] = f'paper_key={meta["paper_key"]}≠文件名'
        out[key] = meta
    return out


# ─── 认领快照 ────────────────────────────────────────────────────────────────
def load_snapshot(path=SNAPSHOT):
    meta = {'path': path, 'exists': os.path.exists(path), 'snapshot_at': None,
            'healthy': None, 'open_prs': None, 'reviewed': None, 'repo': None,
            'stale_days': None, 'fresh': False, 'rows': {}}
    if not meta['exists']:
        return meta
    try:
        with open(path, encoding='utf-8') as fh:
            lines = fh.read().splitlines()
    except OSError as e:
        meta['read_error'] = str(e)
        return meta
    cols = None
    for ln in lines:
        if not ln.strip():
            continue
        if ln.startswith('#'):
            m = re.match(r'#\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$', ln)
            if m:
                meta[m.group(1)] = m.group(2).strip()
            continue
        parts = [p.strip() for p in ln.split('\t')]
        if cols is None:
            cols = parts
            continue
        row = dict(zip(cols, parts))
        sid = row.get('source_id') or ''
        if sid:
            meta['rows'][sid] = row
    dt = parse_iso(meta.get('snapshot_at'))
    if dt:
        age = days_since(dt)
        meta['stale_days'] = age
        meta['fresh'] = age <= SNAPSHOT_STALE_DAYS
    return meta

# ─── 维护者预留台账（audit/reserved.tsv，人工维护）───────────────────────────
RESERVED_COLS = ('source_id', 'holder', 'since', 'until', 'reason', 'ref')


def load_denied(path=None):
    """→ {'path','exists','rows':{sid:rec},'errors':[...]}

    已否证源清单（audit/denied.tsv）：维护者裁定删除的源。**不参与**状态机——它们根本
    不该有 info 文件，所以也不会进可认领队列；这张表的作用是让人在重建/复审时立刻知道
    「这个源已经被否证过，判据是什么」，见 Issue #183。
    容错优先：坏行只记 errors，绝不抛异常。
    """
    path = path or DENIED_TSV
    meta = {'path': path, 'exists': os.path.exists(path), 'rows': {}, 'errors': []}
    if not meta['exists']:
        return meta
    try:
        with open(path, encoding='utf-8') as fh:
            lines = fh.read().splitlines()
    except OSError as e:
        meta['unreadable'] = str(e)
        return meta
    for n, ln in enumerate(lines, 1):
        if not ln.strip() or ln.lstrip().startswith('#'):
            continue
        parts = [p.strip() for p in ln.split('\t')]
        if parts[0] == 'source_id':
            continue
        sid = parts[0]
        if not sid:
            meta['errors'].append(f'第 {n} 行：首列为空，已忽略')
            continue
        rec: dict = dict(zip(DENIED_COLS, parts + [''] * max(0, len(DENIED_COLS) - len(parts))))
        rec['line'] = n
        if sid in meta['rows']:
            meta['errors'].append(f'第 {n} 行：{sid} 重复，保留先出现的一行')
            continue
        meta['rows'][sid] = rec
    return meta


def denied_note(denied):
    """一行摘要：denied.tsv 是否在用。"""
    if not denied or not denied.get('exists'):
        return ''
    n = len(denied.get('rows') or {})
    if not n:
        return '已否证源清单：audit/denied.tsv 存在但为空'
    return f'已否证源清单：{n} 个源（audit/denied.tsv，删除后不得重建，见 Issue #183）'


def cmd_denied(args, denied):
    """列出已否证源（只读）。"""
    rows = denied.get('rows') or {}
    if not denied.get('exists'):
        print(f'{denied["path"]} 不存在 → 还没有任何已否证源', file=sys.stderr)
        return 4
    if not rows:
        print('已否证源清单：0 个源')
        return 0
    print(f'已否证源清单（{len(rows)} 个，{denied["path"]}）')
    for sid in sorted(rows):
        r = rows[sid]
        print(f'{sid}\t{r.get("reason_code") or "?"}\t{r.get("date") or "?"}\t{r.get("ref") or "—"}')
        if r.get('evidence'):
            print(f'    判据：{r["evidence"]}')
        if r.get('decided_by'):
            print(f'    裁定人：{r["decided_by"]}')
    for e in denied.get('errors') or []:
        print(f'  ⚠ {e}', file=sys.stderr)
    print('→ 这些源已从库中删除：**不要认领、不要审核、不要重建**；若 info/ 里又出现同名文件，'
          '说明导入管线把源重建了（见 Issue #183）')
    return 0


def load_reserved(path=None):
    """→ {'path','exists','rows':{sid:rec},'errors':[...],'unreadable':str}

    维护者自留台账：被预留的源**不进入可认领队列**（`claimable='no'`）。
    与 `audit/leads/` 相反，它**参与**状态机（`reserved` 是一个状态），但**不写进**
    `info/*.json`（认领/预留状态一律不进数据文件）。
    容错优先：坏行只记 errors，绝不抛异常，也绝不因此把源当成 free。
    """
    path = path or RESERVED_TSV
    meta = {'path': path, 'exists': os.path.exists(path), 'rows': {}, 'errors': []}
    if not meta['exists']:
        return meta
    try:
        with open(path, encoding='utf-8') as fh:
            lines = fh.read().splitlines()
    except OSError as e:
        meta['unreadable'] = str(e)
        return meta
    seen_cols = False
    for n, ln in enumerate(lines, 1):
        if not ln.strip() or ln.lstrip().startswith('#'):
            continue
        parts = [p.strip() for p in ln.split('\t')]
        if not seen_cols and parts[0] == 'source_id':      # 列名行（可选）
            seen_cols = True
            continue
        seen_cols = True
        sid = parts[0]
        if not sid:
            meta['errors'].append(f'第 {n} 行：首列为空，已忽略')
            continue
        rec: dict = dict(zip(RESERVED_COLS, parts + [''] * max(0, len(RESERVED_COLS) - len(parts))))
        rec['line'] = n
        if not rec.get('holder'):
            # 缺 holder 但源 ID 在 → **保留预留**（fail-closed）：坏行不能等于放人
            rec['holder'] = '?'
            meta['errors'].append(f'第 {n} 行：{sid} 缺 holder（占位 ?），预留仍然生效')
        if sid in meta['rows']:
            meta['errors'].append(f'第 {n} 行：{sid} 重复，保留先出现的一行')
            continue
        until = parse_iso(rec.get('until'))
        rec['until_dt'] = until
        rec['expired'] = bool(until and days_since(until) > 0)
        rec['days_left'] = (round((until - now_utc()).total_seconds() / 86400.0, 1)
                            if until else None)
        if not until:
            meta['errors'].append(f'第 {n} 行：{sid} 的 until={rec.get("until")!r} 缺失/非法'
                                  f' → 按不过期处理（硬锁），请补截止日')
        meta['rows'][sid] = rec
    return meta



# ─── GitHub 侧认领信息 ───────────────────────────────────────────────────────
def gh_open_prs(repo=None, timeout=GH_TIMEOUT):
    """取 open PR 列表（含改动文件）。失败一律抛 RuntimeError。"""
    def _run(fields):
        cmd = ['gh', 'pr', 'list', '--state', 'open', '--limit', '300', '--json', fields]
        if repo:
            cmd += ['--repo', repo]
        try:
            p = subprocess.run(cmd, capture_output=True, text=True,
                               timeout=timeout, cwd=ROOT)
        except FileNotFoundError:
            raise RuntimeError('找不到 gh 可执行文件（未安装或不在 PATH）')
        except subprocess.TimeoutExpired:
            raise RuntimeError(f'gh 超时（>{timeout}s）')
        if p.returncode != 0:
            raise RuntimeError(f'gh pr list 失败（exit {p.returncode}）：'
                               f'{(p.stderr or "").strip().splitlines()[-1][:200] if p.stderr else ""}')
        try:
            data = json.loads(p.stdout or '[]')
        except ValueError as e:
            raise RuntimeError(f'gh 输出无法解析为 JSON：{e}')
        if not isinstance(data, list):
            raise RuntimeError('gh 输出不是数组')
        return data

    try:
        return _run(GH_JSON_FIELDS)
    except RuntimeError as e:
        # 老版本 gh 不认 --json files：降级为只按标题识别来源
        if 'files' in str(e) and 'Unknown' in str(e) or 'unknown JSON' in str(e).lower():
            return _run(GH_JSON_FIELDS_NOFILES)
        raise


PR_FILE_RE = re.compile(r'^(?:info|lc)/(.+)\.(?:json|csv)$')
# 标题里的源 id token：长度放宽到 2（源 id 允许 1–32 位字母数字），
# 误匹配由 "token 必须是已知源 id" 兜住。
TITLE_TOKEN_RE = re.compile(r'[A-Za-z0-9]{2,32}')


def ids_touched_by_pr(pr, known_ids):
    """该 PR 触及的源 id：先看改动文件（权威），再看标题里出现的已知 id。"""
    ids = set()
    for f in pr.get('files') or []:
        path = f.get('path') if isinstance(f, dict) else str(f)
        m = PR_FILE_RE.match(path or '')
        if m:
            ids.add(m.group(1))
    if not ids:
        for tok in TITLE_TOKEN_RE.findall(pr.get('title') or ''):
            if tok in known_ids:
                ids.add(tok)
    return ids


def claims_from_prs(prs, sources):
    """→ {id: {state, holder, since, updated, pr, ttl}}（同一源多条 PR 时取最早一条）"""
    agg = {}
    for pr in prs:
        ids = ids_touched_by_pr(pr, sources)
        if not ids:
            continue
        num = pr.get('number')
        draft = bool(pr.get('isDraft'))
        author = pr.get('author')
        login = author.get('login') if isinstance(author, dict) else (author or '?')
        created = (pr.get('createdAt') or '')[:10]
        updated_dt = parse_iso(pr.get('updatedAt'))
        for sid in ids:
            rec = agg.setdefault(sid, {'prs': [], 'created': [], 'updated': [],
                                       'draft': True, 'holder': login or '?'})
            rec['prs'].append(num)
            rec['created'].append(created)
            rec['updated'].append(updated_dt)
            rec['draft'] = rec['draft'] and draft
            rec['holder'] = rec['holder'] or (login or '?')
    out = {}
    for sid, rec in agg.items():
        rows = (sources.get(sid) or {}).get('rows', 0)
        ttl = ttl_days(rows)
        last = max([d for d in rec['updated'] if d], default=None)
        age = days_since(last) if last else None
        if rec['draft']:
            state = 'stale-claim' if (age is not None and age > ttl) else CLAIMED
        else:
            state = 'stale-pr' if (age is not None and age > ttl) else IN_REVIEW
        out[sid] = {
            'state': state,
            'holder': rec['holder'],
            'since': min([d for d in rec['created'] if d], default=''),
            'updated': (last.strftime('%Y-%m-%d') if last else ''),
            'pr': ','.join('#' + str(n) for n in sorted(rec['prs'])),
            'ttl': ttl,
        }
    return out


# ─── 状态合成 ────────────────────────────────────────────────────────────────
def resolve(sources, claims, snap, reserved=None):
    """→ {id: {state, basis, claim, claimable, rows}}；claimable ∈ {yes, takeover, no}

    优先级：`reviewed`（已完成）> `reserved`（维护者自留）> 认领（PR/快照）> `free`。
    claims 非 None 时（--live 成功）**以实时查询为唯一判据**，完全不看快照。
    台账里可能有尚未入库的源：照样派生状态（rows=0），避免预留"看不见"。
    """
    rsv = (reserved or {}).get('rows') or {}
    out = {}
    work = dict(sources)
    for sid, rec in rsv.items():
        work.setdefault(sid, {'id': sid, 'rows': 0, 'audit': None, 'audit_status': ''})
    for sid, src in work.items():
        rows = src['rows']
        if src['audit_status'] == REVIEWED:
            out[sid] = {'state': REVIEWED, 'basis': 'info.extra_data.audit.status=reviewed',
                        'claim': None, 'claimable': 'no', 'rows': rows}
            continue
        r = rsv.get(sid)
        if r:
            # 预留优先于认领：维护者自留是授权行为，不是排队；同时暴露冲突以免静默。
            c0 = (claims or {}).get(sid) if claims is not None else None
            note = ''
            if c0:
                note = f'；⚠ 同时有 open PR {c0["pr"]}（{c0["holder"]}），需协调'
            elif claims is None and snap.get('exists') and snap['rows'].get(sid):
                note = f'；⚠ 快照里也有占用记录（{snap["rows"][sid].get("pr") or "?"}）'
            stale = bool(r.get('expired'))
            basis = (f'维护者自留（{r.get("reason") or "未写原因"}；'
                     f'{"已于 " + str(r.get("until") or "?") + " 到期" if stale else "至 " + str(r.get("until") or "?")}'
                     f'；{r.get("holder")}）' + note
                     + ('；⚠ 该源尚未入库' if sid not in sources else ''))
            out[sid] = {'state': RESERVED_EXPIRED if stale else RESERVED, 'basis': basis,
                        'claim': c0, 'claimable': 'takeover' if stale else 'no',
                        'rows': rows, 'reserved': r}
            continue
        claim, basis, conf = None, '', True
        if claims is not None:
            claim = claims.get(sid)
            if claim:
                basis = (f'{claim["pr"]}（{"draft" if claim["state"].endswith("claim") else "正式"} PR，'
                         f'{claim["holder"]}，更新 {claim["updated"]}）')
        if claim is None and claims is None and snap['exists']:
            row = snap['rows'].get(sid)
            if row:
                claim = {'state': row.get('state') or '?', 'holder': row.get('holder') or '?',
                         'since': row.get('since') or '', 'updated': row.get('updated') or '',
                         'pr': row.get('pr') or '', 'ttl': ttl_days(rows)}
                conf = bool(snap['fresh'])
                basis = (f'快照 {snap["snapshot_at"]}（{row.get("state")}'
                         + (f'，{row.get("pr")}' if row.get('pr') else '')
                         + f'，{row.get("holder")}，更新 {row.get("updated") or "?"}）'
                         + ('' if conf else ' ※快照已过期，未实时确认'))
        if claim is not None:
            state = claim['state']
            if not conf:
                state += '?'
            claimable = 'no'
            if conf and state.startswith('stale'):
                claimable = 'takeover'
            out[sid] = {'state': state, 'basis': basis, 'claim': claim,
                        'claimable': claimable, 'rows': rows}
            continue
        out[sid] = {'state': FREE, 'basis': '无 audit 标记、无认领记录',
                    'claim': None, 'claimable': 'yes', 'rows': rows}
    return out


# ─── 输出 ────────────────────────────────────────────────────────────────────
def source_note(snap, claims, live, live_err, extra=()):
    lines = list(extra)
    if not snap['exists']:
        lines.append('快照 audit/state.tsv：不存在 → 认领状态**未知**（缺席不构成"没人做"的证据）')
    elif snap['stale_days'] is None:
        lines.append(f'快照 {snap["path"]}：存在但 snapshot_at 缺失/非法 → 视为过期')
    else:
        tag = '新鲜' if snap['fresh'] else '**已过期**'
        lines.append(f'快照 audit/state.tsv：snapshot_at={snap["snapshot_at"]}'
                     f'（{snap["stale_days"]:.1f} 天前，{tag}；'
                     f'{len(snap["rows"])} 条占用记录）')
    if live:
        lines.append(f'认领信息取自：gh 实时查询（open PR {len(claims or {})} 个源）')
    elif live_err:
        lines.append(f'认领信息取自：快照（--live 失败：{live_err}）')
    else:
        lines.append('认领信息取自：快照（未用 --live）')
    if not live and not snap['fresh']:
        lines.append('⚠ 快照不可用作"空闲"的证据：它只能**排除已占用**。挑源前做一次实时核对'
                     '（能跑 gh 就用 --live 或 gh pr list）；两个渠道都不通就停下来问用户。')
    lines.append('提示：一个源同时只应有一个未过期认领（普通源 14 天 / >1000 行巨源 30 天）。')
    return lines


def cmd_list(args, sources, resolved, snap, claims, live_err, leads=None):
    leads = leads or {}
    free = [s for s, r in resolved.items() if r['claimable'] == 'yes']
    takeover = [s for s, r in resolved.items() if r['claimable'] == 'takeover']
    key = (lambda s: (resolved[s]['rows'], s)) if args.sort == 'rows' else (lambda s: s)
    free.sort(key=key)
    takeover.sort(key=key)
    if args.bucket:
        k, n = args.bucket
        free = [s for s in free if bucket_index(s, n) == k]
        takeover = [s for s in takeover if bucket_index(s, n) == k]
    total_free = len(free)
    if args.limit:
        free = free[:args.limit]

    if args.format == 'json':
        print(json.dumps({
            'generated_at': now_utc().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'snapshot': {k: snap[k] for k in ('exists', 'snapshot_at', 'fresh', 'stale_days') if k in snap},
            'live': bool(args.live and not live_err),
            'claimed_total': sum(1 for r in resolved.values()
                                 if r['state'] not in (FREE, REVIEWED)),
            'available_total': total_free,
            'available': [{'id': s, 'rows': resolved[s]['rows'],
                           'has_lead': s in leads} for s in free],
            'takeover': [{'id': s, 'rows': resolved[s]['rows'],
                          'state': resolved[s]['state'],
                          'has_lead': s in leads,
                          'basis': resolved[s]['basis']} for s in takeover[:20]],
            'leads_total': len(leads),
        }, ensure_ascii=False, indent=2))
        return 0

    extra = [f'源范围：{args.pub_note}'] if getattr(args, 'pub_note', None) else []
    if getattr(args, 'reserved_note', None):
        extra.append(args.reserved_note)
    for ln in source_note(snap, claims, args.live and not live_err, live_err, extra=extra):
        print(f'# {ln}')
    print('# 列：源ID / lc行数 / 状态 / 认领人 / 起始 / PR / 依据（`+lead` = 有线索卡，务必先读）')
    print(f'# 可认领合计 {total_free} 个源'
          + (f'（分片 {args.bucket[0]}/{args.bucket[1]}）' if args.bucket else '')
          + (f'；本页显示 {len(free)} 个' if args.limit else ''))
    if args.pack:
        for i in range(0, len(free), args.pack):
            grp = free[i:i + args.pack]
            rows_sum = sum(resolved[s]['rows'] for s in grp)
            print(f'\n# pack {i // args.pack + 1}（{len(grp)} 源，{rows_sum} 行）')
            for s in grp:
                print(render_row(s, resolved, leads))
    else:
        for s in free:
            print(render_row(s, resolved, leads))

    if takeover:
        print(f'\n# 可接手（认领超 {CLAIM_TTL_DAYS}/{GIANT_TTL_DAYS} 天，或维护者预留已过 until；'
              f'先在该 PR/Issue 评论询问并等 48 小时）：{len(takeover)} 个')
        for s in takeover[:20]:
            print(render_row(s, resolved, leads))
    return 0


def render_row(sid, resolved, leads=None):
    r = resolved[sid]
    c = r['claim'] or {}
    lead = ''
    if leads and sid in leads:
        lead = f' +lead({leads[sid].get("status") or "?"})'
    return (f'{sid:<28} {r["rows"]:>7} {r["state"]:<17} '
            f'{(c.get("holder") or "-"):<20} {(c.get("since") or "-"):<11} '
            f'{(c.get("pr") or "-"):<10} {r["basis"]}{lead}')


def cmd_id(args, sources, resolved, snap, claims, live, live_err, leads=None, denied=None):
    leads = leads or {}
    denied = denied or {}
    extra = [f'源范围：{args.pub_note}'] if getattr(args, 'pub_note', None) else []
    if getattr(args, 'reserved_note', None):
        extra.append(args.reserved_note)
    if getattr(args, 'denied_note', None):
        extra.append(args.denied_note)
    sid = args.id
    drow = (denied.get('rows') or {}).get(sid)
    if drow:
        print(f'源 {sid}：**已被否证**（不在库中，也不该被重建）')
        print(f'  原因代码        : {drow.get("reason_code") or "?"}')
        print(f'  裁定人/日期     : {drow.get("decided_by") or "?"} / {drow.get("date") or "?"}')
        print(f'  关联            : {drow.get("ref") or "—"}')
        if drow.get('evidence'):
            print(f'  判据            : {drow["evidence"]}')
        print('  → **不要认领、不要审核、不要重建这个源**。若 info/ 里又出现同名文件，'
              '说明导入管线把它重建了，按上面的判据重新否证（见 Issue #183）')
        return 0
    if sid not in sources and sid not in resolved:
        print(f'未找到源 {sid}（info/{sid}.json 不存在）', file=sys.stderr)
        print(f'提示：先查 audit/denied.tsv（python3 tools/audit_queue.py --denied）——'
              f'若已被否证，说明删得对，不要重建', file=sys.stderr)
        return 4
    r = resolved.get(sid) or {'state': FREE, 'rows': 0, 'basis': '—', 'claim': None,
                              'claimable': 'yes'}
    src = sources.get(sid) or {}
    print(f'源 {sid}')
    print(f'  lc 行数        : {r["rows"]}')
    if not r['rows']:
        print('  ⚠ 零测光       : 《数据审核提示词》§3.3（2026-10-24）要求先检索仓内快照'
              '（gcn/archive 全文 / external/rssgrbag / external/grbsn_webtool）')
        print('                   再查 GCN 站 / ADS 或 SciX / TNS，并在 comment 里留证：'
              '检索日期 + 入口与篇数 + 结论 + 补了几行')
    print(f'  审核标记        : {json.dumps(src.get("audit"), ensure_ascii=False) if src.get("audit") else "（无）"}')
    print(f'  状态           : {r["state"]}')
    print(f'  依据           : {r["basis"]}')
    print(f'  可否认领        : {r["claimable"]}')
    rr = r.get('reserved')
    if rr:
        left = rr.get('days_left')
        print(f'  维护者预留      : {rr.get("holder")}（{rr.get("reason") or "未写原因"}）')
        print(f'  预留截止        : {rr.get("until") or "?"}'
              + (f'（**已过期 {abs(left):.1f} 天**，需先沟通）' if rr.get('expired') and left is not None
                 else (f'（还剩 {left:.1f} 天）' if left is not None else '（无截止日，硬锁）')))
        print('  → 该源由维护者自留：**不要认领、不要开 claim PR**；'
              '确需推进请在 Issue 里说明理由并等维护者答复（公平性靠这条，不靠自觉）')
    c = r.get('claim')
    if c:
        ttl = c.get('ttl') or ttl_days(r['rows'])
        up = parse_iso(c.get('updated'))
        age = days_since(up) if up else None
        print(f'  认领 TTL        : {ttl} 天'
              + (f'（最后更新 {c.get("updated")}，已 {age:.1f} 天）' if age is not None else ''))
        if r['state'].startswith('stale'):
            print('  接手流程        : 在该 PR 上评论询问 → 等 48 小时 → 无响应即可接手，并在自己的 PR 里说明')
    if c and c.get('state', '').endswith('?'):
        print('  ⚠ 快照已过期：该占用未实时确认，请用 --live 或 gh pr list 复核后再决定')
    lead = leads.get(sid)
    if lead:
        print(f'  线索卡         : {lead["rel"]}'
              f'（status={lead.get("status") or "?"}'
              + (f'，{lead["pr"]}' if lead.get('pr') else '')
              + (f'，{lead.get("paper") or ""}' if lead.get('paper') else '') + '）')
        print('  → 必读：线索只是待核对清单，不改变本源的 free/claimed 判定；仍须自己认领、'
              '自己打开原文核验。审完（或否证）在**你自己的数据 PR** 里 git rm 该文件')
        if lead.get('mismatch'):
            print(f'  ⚠ 线索卡元数据异常：{lead["mismatch"]}')
        if r['state'] == REVIEWED:
            print('  ⚠ 该源已是 reviewed，线索卡应已在该源审核 PR 中删除 → 维护者清理')
        if lead.get('parse_error'):
            print(f'  ⚠ 线索卡读取失败：{lead["parse_error"]}')
    for ln in source_note(snap, claims, live and not live_err, live_err, extra=extra):
        if ln.startswith(('⚠', '提示', '源范围')):
            print(f'  · {ln}')
    return 0


def cmd_leads(args, sources, resolved, leads, papers=None):
    """列出全部线索卡（人工维护；只读，不影响源状态）。"""
    papers = load_paper_cards() if papers is None else papers
    in_paper = {}
    for k, p in papers.items():
        for s in p['sources']:
            in_paper.setdefault(s, []).append(k)
    if not leads:
        print('# 无线索卡（audit/leads/ 为空或不存在）')
        return 0
    print(f'# 线索卡 {len(leads)} 张（人工维护；不影响源状态，契约见 audit/leads/README.md）')
    print('# 列：源ID / 源状态 / 线索status / 出处 / 提出人 / 日期 / PR')
    for sid in sorted(leads):
        l = leads[sid]
        st = (resolved.get(sid) or {}).get('state', 'unknown')
        print(f'{sid:<24} {st:<12} {(l.get("status") or "?"):<13} '
              f'{(l.get("paper") or "-")[:38]:<38} {(l.get("helper") or "-"):<18} '
              f'{(l.get("date") or "-"):<11} {l.get("pr") or "-"}')
        if l.get('mismatch'):
            print(f'  ⚠ 文件名与 source_id 不一致：{l["mismatch"]}')
        if sid in in_paper:
            print(f'  · 已登记于文献级卡：{", ".join(in_paper[sid])}')
        if sid not in sources:
            print('  ⚠ 目标源不在仓库内 —— 新源应改开 new-source Issue（提示词 §3.11）')
        if st == REVIEWED:
            print('  ⚠ 源已 reviewed，线索卡应在其审核 PR 中删除')
    if papers:
        print(f'\n# 文献级索引卡 {len(papers)} 张（audit/leads/papers/；--paper <paper_key> 展开）')
        print('# 列：paper_key / 涉及源 / 已有源级卡 / 出处')
        for k in sorted(papers):
            p = papers[k]
            have = sum(1 for s in p['sources'] if s in leads)
            print(f'{k:<30} {len(p["sources"]):>4} 源 {have:>4} 张卡   {(p.get("paper") or "-")[:56]}')
            if p.get('mismatch'):
                print(f'  ⚠ {p["mismatch"]}')
            for s in p['out_of_repo']:
                print(f'  · 库外源 {s}（应走 new-source Issue，不建卡）')
    return 0


def cmd_paper(args, sources, resolved, leads, papers):
    """展开一张文献级索引卡：它登记了哪些源、各自有没有源级卡、源现在是什么状态。"""
    key = (args.paper or '').strip()
    p = papers.get(key)
    if not p:
        cand = [k for k in papers if key and key.lower() != k.lower() and key.lower() in k.lower()]
        print(f'没有 paper_key={key!r} 的文献级卡', file=sys.stderr)
        print(f'现有：{", ".join(sorted(papers)) or "（无）"}', file=sys.stderr)
        if cand:
            print(f'相近：{", ".join(cand)}', file=sys.stderr)
        return 5
    print(f'# 文献级卡 {p["rel"]}')
    for k in ('paper_key', 'paper', 'date', 'helper'):
        if p.get(k):
            print(f'{k:<10}: {p[k]}')
    print(f'{"涉及源":<10}: {len(p["sources"])} 个'
          f'（其中 {sum(1 for s in p["sources"] if s in leads)} 个已有源级卡）')
    print('\n# 列：源ID / 源状态 / 源级卡 / status')
    for sid in p['sources']:
        st = (resolved.get(sid) or {}).get('state', 'unknown')
        c = leads.get(sid)
        print(f'{sid:<24} {st:<12} {(c["rel"] if c else "（无源级卡）"):<36} '
              f'{(c.get("status") if c else "-")}')
    missing = [s for s in p['sources'] if s not in sources]
    if missing:
        print(f'\n⚠ 库内不存在：{", ".join(missing)}（新源应走 new-source Issue，不建卡）')
    if p.get('mismatch'):
        print(f'⚠ {p["mismatch"]}')
    return 0


def cmd_check_leads(args, sources, resolved, leads, papers):
    """PR 守卫（警告级，**永不失败**）：线索卡规模/形态是否按 §3.11 收敛到文献级卡。

    只在 PR 里跑：判据是**本 PR 新增**的卡，避免拿历史欠账（如 Ershova+2020 已合并的
    45 张源级卡）天天刷警告。
    """
    base = getattr(args, 'base', None) or 'origin/main'
    try:
        p = subprocess.run(['git', '-C', ROOT, 'diff', '--name-status', f'{base}...HEAD',
                            '--', 'audit/leads'], capture_output=True, text=True, timeout=120)
        if p.returncode != 0:
            p = subprocess.run(['git', '-C', ROOT, 'diff', '--name-status', base,
                                '--', 'audit/leads'], capture_output=True, text=True, timeout=120)
        if p.returncode != 0:
            err = [l for l in (p.stderr or '').strip().splitlines() if l.strip()]
            raise RuntimeError((err or ['git diff 失败'])[-1][:200])
        lines = [ln for ln in (p.stdout or '').splitlines() if ln.strip()]
    except (OSError, subprocess.SubprocessError, RuntimeError) as e:
        print(f'::notice::无法计算 audit/leads 改动（{e}）→ 线索卡守卫跳过（不阻断）')
        return 0
    added_src, added_paper = [], []
    for ln in lines:
        parts = ln.split('\t')
        if len(parts) < 2:
            continue
        status, path = parts[0][:1], parts[-1]
        if not path.endswith('.md') or os.path.basename(path).lower() == 'readme.md':
            continue
        if '/papers/' in path:
            if status == 'A':
                added_paper.append(path)
        elif status == 'A':
            added_src.append(path)
    if not added_src and not added_paper:
        print(f'线索卡守卫：本 PR 未新增线索卡（{len(lines)} 处 audit/leads 改动）→ 通过')
        return 0
    print(f'线索卡守卫：新增源级卡 {len(added_src)} 张、文献级卡 {len(added_paper)} 张')
    if len(added_src) >= RCARD_MIN_WARN and not added_paper:
        print(f'::warning::本 PR 新增 {len(added_src)} 张源级线索卡但没有文献级卡 —— 一篇多源文献应先用 '
              f'`audit/leads/papers/<paper_key>.md` 收敛（《数据审核提示词》§3.11；增量门槛见 '
              f'audit/leads/README.md）。已合并的历史卡不追溯。')
    trans = []
    for path in added_src:
        try:
            txt = open(os.path.join(ROOT, path), encoding='utf-8').read()
        except OSError:
            continue
        if 'mention-only' in txt and any(k in txt for k in
                                         ('转引', '汇总表', '仅确认行存在', '未逐字段提取')):
            trans.append(os.path.basename(path)[:-3])
    if len(trans) >= 3:
        print(f'::warning::{len(trans)} 张新增源级卡自述为「转引/汇总表」性质'
              f'（{", ".join(sorted(trans)[:6])}{" …" if len(trans) > 6 else ""}）——按 §3.11 增量门槛'
              f'这类不该开源级卡，把行信息写进文献级卡即可')
    print('线索卡守卫：警告级，不阻断')
    return 0


# ─── 维护者预留：摘要 / 列表 / PR 守卫 ────────────────────────────────────────
def reserved_note(reserved, sources=None):
    """一行摘要（进队列与单源输出的头部注释）。台账不存在/为空时返回 ''。"""
    if not reserved or not reserved.get('exists'):
        return ''
    rows = reserved.get('rows') or {}
    if not rows:
        return ''
    exp = sum(1 for r in rows.values() if r.get('expired'))
    outside = (len([s for s in rows if s not in sources]) if sources is not None else 0)
    txt = (f'维护者预留：{len(rows)} 个源（audit/reserved.tsv'
           + (f'，其中 {exp} 个已过期' if exp else '')
           + (f'，{outside} 个尚未入库' if outside else '')
           + '）→ 这些源不进入可认领队列，外部协作者不得认领')
    if reserved.get('errors'):
        txt += f'；⚠ 台账有 {len(reserved["errors"])} 处问题（--reserved 查看）'
    if reserved.get('unreadable'):
        txt += f'；⚠ 台账读取失败：{reserved["unreadable"]}'
    return txt


def cmd_reserved(args, reserved, sources=None):
    """列出维护者预留台账（人工维护；参与状态机，但不写进数据文件）。"""
    if not reserved.get('exists'):
        print(f'# 无预留台账（audit/reserved.tsv 不存在）→ 当前无源被预留')
        return 0
    rows = reserved.get('rows') or {}
    print(f'# 维护者预留 {len(rows)} 个源（契约见 audit/README.md；外部协作者不得认领这些源）')
    if not rows:
        print('# 台账为空')
    print('# 列：源ID / 状态 / 预留人 / 起始 / 截止 / 剩余 / 原因')
    for sid in sorted(rows, key=lambda s_: (bool(rows[s_].get('expired')),
                                            str(rows[s_].get('until') or ''), s_)):
        r = rows[sid]
        left = r.get('days_left')
        try:
            left_txt = '已过期' if r.get('expired') else (f'{left:.1f} 天' if left is not None else '-')
        except (TypeError, ValueError):
            left_txt = '?'
        print(f'{sid:<24} {(RESERVED_EXPIRED if r.get("expired") else RESERVED):<17} '
              f'{(r.get("holder") or "?"):<20} {(r.get("since") or "-"):<11} '
              f'{(r.get("until") or "-"):<11} {left_txt:<10} {r.get("reason") or ""}')
        if sources is not None and sid not in sources:
            print('  ⚠ 该源尚未入库（预留仍生效，入库后自动接管）')
        if r.get('expired'):
            print('  → 已过 until：续期（改 until）或删掉该行；接手方按 48 h 沟通协议处理')
    for e in reserved.get('errors') or []:
        print(f'  ⚠ {e}')
    return 0


def cmd_check_reserved(args, reserved):
    """PR 守卫（警告级，**永不失败**）：本 PR 改动的 info/lc 是否触及维护者自留源。"""
    rows = (reserved or {}).get('rows') or {}
    if not rows:
        print('无维护者预留 → 跳过')
        return 0
    base = getattr(args, 'base', None) or 'origin/main'
    try:
        p = subprocess.run(['git', '-C', ROOT, 'diff', '--name-only', f'{base}...HEAD'],
                           capture_output=True, text=True, timeout=120)
        if p.returncode != 0 or not (p.stdout or '').strip():
            p = subprocess.run(['git', '-C', ROOT, 'diff', '--name-only', base],
                               capture_output=True, text=True, timeout=120)
        if p.returncode != 0:
            err_lines = [l for l in (p.stderr or '').strip().splitlines() if l.strip()]
            key = [l for l in err_lines if l.startswith(('fatal', 'error'))]
            raise RuntimeError((key or err_lines or ['git diff 失败'])[-1][:200])
        changed = (p.stdout or '').split()
    except (OSError, subprocess.SubprocessError, RuntimeError) as e:
        print(f'::notice::无法计算改动文件（{e}）→ 预留守卫跳过（不阻断）')
        return 0
    hit = {}
    for path in changed:
        m = PR_FILE_RE.match(path)
        if m and m.group(1) in rows:
            hit.setdefault(m.group(1), []).append(path)
    if not hit:
        print(f'预留守卫：改动文件未触及 {len(rows)} 个维护者自留源 → 通过')
        return 0
    for sid in sorted(hit):
        r = rows[sid]
        print(f'::warning::{sid} 是维护者自留源（{r.get("holder")}，'
              f'{r.get("reason") or "未写原因"}，至 {r.get("until") or "?"}），'
              f'本 PR 改动了 {", ".join(hit[sid])}；若非维护者本人发起，请改审其他源')
    print(f'预留守卫：{len(hit)} 个自留源被本 PR 改动（警告级，不阻断）：{", ".join(sorted(hit))}')
    return 0


# ─── 快照生成 ────────────────────────────────────────────────────────────────
def render_snapshot(sources, claims, repo, reserved=None):
    ts = now_utc().strftime('%Y-%m-%dT%H:%M:%SZ')
    reviewed = sum(1 for s in sources.values() if s['audit_status'] == REVIEWED)
    lines = [
        '# audit/state.tsv — AJST-Data 认领快照（机器生成，**勿手改**）',
        '# 由 .github/workflows/audit-snapshot.yml 每日生成；本地重建：',
        '#   python3 tools/audit_queue.py --emit-snapshot',
        '# 契约与读取规则见 audit/README.md',
        f'# snapshot_at={ts}',
        '# healthy=true',
        f'# repo={repo or ""}',
        f'# open_sources={len(claims)}',
        f'# reviewed={reviewed}/{len(sources)}',
        f'# reserved={len((reserved or {}).get("rows") or {})}',
        '# 状态：claimed=open draft PR；in-review=open 正式 PR；stale-*=超过 TTL 未更新（可接手）',
        '# 只列"仓库文件里看不到"的占用状态；reviewed 见各 info/*.json，free 即未列出者',
        '\t'.join(['source_id', 'state', 'holder', 'since', 'updated', 'pr']),
    ]
    for sid in sorted(claims):
        c = claims[sid]
        lines.append('\t'.join([sid, c['state'], c['holder'], c['since'], c['updated'], c['pr']]))
    return '\n'.join(lines) + '\n'


def atomic_write(path, text):
    d = os.path.dirname(os.path.abspath(path)) or '.'
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix='.state-', suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def cmd_emit(args, sources, repo):
    try:
        prs = gh_open_prs(repo, args.gh_timeout)
    except RuntimeError as e:
        print(f'[ERROR] 取 open PR 失败，快照未改动：{e}', file=sys.stderr)
        return 2
    claims = claims_from_prs(prs, sources)
    reserved = load_reserved()
    text = render_snapshot(sources, claims, repo, reserved)
    try:
        atomic_write(args.out or SNAPSHOT, text)
    except OSError as e:
        print(f'[ERROR] 写入失败：{e}', file=sys.stderr)
        return 3
    print(f'已写入 {args.out or SNAPSHOT}：{len(claims)} 个占用源，'
          f'{len((reserved or {}).get("rows") or {})} 个维护者预留（只记数量，不入快照），'
          f'{sum(1 for s in sources.values() if s["audit_status"] == REVIEWED)}/'
          f'{len(sources)} 已审核', file=sys.stderr)
    return 0


# ─── CLI ─────────────────────────────────────────────────────────────────────
def main(argv=None):
    ap = argparse.ArgumentParser(
        description='AJST-Data 审核队列 / 认领工具（确定性、离线优先）')
    ap.add_argument('--limit', type=int, default=20, help='最多列出多少个可认领源（0=全部）')
    ap.add_argument('--bucket', metavar='K/N', help='确定性分片，如 1/4（1 ≤ K ≤ N）')
    ap.add_argument('--id', metavar='SOURCE_ID', help='查单个源的状态与依据')
    ap.add_argument('--pack', type=int, metavar='M', help='按 M 个源一批打包输出')
    ap.add_argument('--sort', choices=['rows', 'id'], default='rows',
                    help='排序：rows=按代价升序（默认），id=按源名')
    ap.add_argument('--include-all', action='store_true', help='列出所有源（含已审核/被占用）')
    ap.add_argument('--leads', action='store_true',
                    help='列出全部线索卡 audit/leads/（多目标文献交接；不影响源状态）')
    ap.add_argument('--paper', metavar='PAPER_KEY',
                    help='展开一张文献级索引卡 audit/leads/papers/<paper_key>.md')
    ap.add_argument('--check-leads', action='store_true',
                    help='PR 守卫：本 PR 新增线索卡的规模/形态（警告级，永不失败）')
    ap.add_argument('--reserved', action='store_true',
                    help='列出维护者预留 audit/reserved.tsv（自留源；外部协作者不得认领）')
    ap.add_argument('--denied', action='store_true',
                    help='列出已否证源 audit/denied.tsv（已删除的源；不得重建，见 Issue #183）')
    ap.add_argument('--check-reserved', action='store_true',
                    help='PR 守卫：改动文件是否触及自留源（警告级，永不失败）')
    ap.add_argument('--base', metavar='REF', help='配合 --check-reserved 指定比对基线（默认 origin/main）')
    ap.add_argument('--include-unpublished', action='store_true',
                    help='纳入未发布/未跟踪源（默认只列公开仓库里有的源）')
    ap.add_argument('--format', choices=['plain', 'json'], default='plain')
    ap.add_argument('--live', action='store_true', help='用 gh 实时查 open PR（判据；失败则退回快照）')
    ap.add_argument('--emit-snapshot', action='store_true', help='生成认领快照（必须能访问 gh）')
    ap.add_argument('--out', metavar='PATH', help='配合 --emit-snapshot 指定输出路径')
    ap.add_argument('--repo', metavar='OWNER/NAME', help='目标仓库（默认取 GITHUB_REPOSITORY 或 gh 推断）')
    ap.add_argument('--gh-timeout', type=int, default=GH_TIMEOUT, help='gh 调用超时秒数')
    args = ap.parse_args(argv)

    if args.bucket:
        try:
            k, n = (int(x) for x in args.bucket.split('/'))
            assert 1 <= k <= n and n > 0
        except Exception:
            print('--bucket 应为 K/N（如 1/4，1 ≤ K ≤ N）', file=sys.stderr)
            return 4
        args.bucket = (k, n)
    if args.limit is not None and args.limit < 0:
        print('--limit 不能为负', file=sys.stderr)
        return 4

    repo = args.repo or os.environ.get('GITHUB_REPOSITORY') or None
    all_sources = load_sources()
    if not all_sources:
        print(f'[ERROR] {INFO_DIR} 下没有 info JSON —— 请在仓库根目录运行本工具', file=sys.stderr)
        return 3
    if args.include_unpublished:
        is_pub, pub_how = (lambda sid: True), ''
    else:
        is_pub, pub_how = make_published_filter()
    sources = {s: v for s, v in all_sources.items() if is_pub(s)}
    hidden = len(all_sources) - len(sources)
    if args.include_unpublished:
        args.pub_note = f'{len(sources)} 个源（含未发布，未做过滤）'
    else:
        args.pub_note = (f'{len(sources)} 个已发布源'
                         + (f'；已排除 {hidden} 个未发布/未跟踪源（{pub_how}）' if hidden else ''))

    if args.emit_snapshot:
        return cmd_emit(args, sources, repo)

    snap = load_snapshot(SNAPSHOT)
    claims = None
    live_err = None
    if args.live:
        try:
            claims = claims_from_prs(gh_open_prs(repo, args.gh_timeout), sources)
        except RuntimeError as e:
            live_err = str(e)
            claims = None
            if args.live:
                print(f'# ⚠ --live 失败，退回快照：{e}', file=sys.stderr)

    reserved = load_reserved()
    denied = load_denied()
    resolved = resolve(sources, claims, snap, reserved)
    leads = load_leads()
    papers = load_paper_cards()
    args.reserved_note = reserved_note(reserved, sources)
    args.denied_note = denied_note(denied)
    if args.include_all:
        order = sorted(resolved, key=lambda s: (resolved[s]['state'], resolved[s]['rows'], s))
        for s in order:
            print(render_row(s, resolved, leads))
        return 0
    if args.leads:
        return cmd_leads(args, all_sources, resolved, leads, papers)
    if args.paper:
        return cmd_paper(args, sources, resolved, leads, papers)
    if args.check_leads:
        return cmd_check_leads(args, sources, resolved, leads, papers)
    if args.reserved:
        return cmd_reserved(args, reserved, sources)
    if args.denied:
        return cmd_denied(args, denied)
    if args.check_reserved:
        return cmd_check_reserved(args, reserved)
    if args.id:
        if args.id not in sources and args.id in all_sources:
            print(f'源 {args.id} 存在但未发布（.gitignore 排除）→ 不在审核队列范围'
                  f'（如需纳入请加 --include-unpublished）', file=sys.stderr)
            return 5
        return cmd_id(args, sources, resolved, snap, claims, args.live, live_err, leads, denied)
    return cmd_list(args, sources, resolved, snap, claims, live_err, leads)


if __name__ == '__main__':
    sys.exit(main())
