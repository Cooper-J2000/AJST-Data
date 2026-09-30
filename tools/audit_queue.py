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
  free        以上都不是 → 可认领
  带 `?` 后缀 认领信息来自过期快照，未实时确认（只作"可能被占用"用）

用法 / Usage:
  python3 tools/audit_queue.py --limit 20              # 可认领队列（代价升序）
  python3 tools/audit_queue.py --bucket 1/4 --limit 50 # 确定性分片，多人互不重叠
  python3 tools/audit_queue.py --id GRB130427A         # 单源状态与依据
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

SNAPSHOT_STALE_DAYS = 3     # 快照超过这个天数即视为过期（工具会告警）
CLAIM_TTL_DAYS = 14         # 普通源的认领软过期
GIANT_ROWS = 1000           # 超过这么多行的源算"巨源"
GIANT_TTL_DAYS = 30         # 巨源的认领软过期
GH_TIMEOUT = 60

REVIEWED = 'reviewed'
IN_REVIEW = 'in-review'
CLAIMED = 'claimed'
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
def resolve(sources, claims, snap):
    """→ {id: {state, basis, claim, claimable, rows}}；claimable ∈ {yes, takeover, no}

    claims 非 None 时（--live 成功）**以实时查询为唯一判据**，完全不看快照。
    """
    out = {}
    for sid, src in sources.items():
        rows = src['rows']
        if src['audit_status'] == REVIEWED:
            out[sid] = {'state': REVIEWED, 'basis': 'info.extra_data.audit.status=reviewed',
                        'claim': None, 'claimable': 'no', 'rows': rows}
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


def cmd_list(args, sources, resolved, snap, claims, live_err):
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
            'available': [{'id': s, 'rows': resolved[s]['rows']} for s in free],
            'takeover': [{'id': s, 'rows': resolved[s]['rows'],
                          'state': resolved[s]['state'],
                          'basis': resolved[s]['basis']} for s in takeover[:20]],
        }, ensure_ascii=False, indent=2))
        return 0

    extra = [f'源范围：{args.pub_note}'] if getattr(args, 'pub_note', None) else []
    for ln in source_note(snap, claims, args.live and not live_err, live_err, extra=extra):
        print(f'# {ln}')
    print('# 列：源ID / lc行数 / 状态 / 认领人 / 起始 / PR / 依据')
    print(f'# 可认领合计 {total_free} 个源'
          + (f'（分片 {args.bucket[0]}/{args.bucket[1]}）' if args.bucket else '')
          + (f'；本页显示 {len(free)} 个' if args.limit else ''))
    if args.pack:
        for i in range(0, len(free), args.pack):
            grp = free[i:i + args.pack]
            rows_sum = sum(resolved[s]['rows'] for s in grp)
            print(f'\n# pack {i // args.pack + 1}（{len(grp)} 源，{rows_sum} 行）')
            for s in grp:
                print(render_row(s, resolved))
    else:
        for s in free:
            print(render_row(s, resolved))

    if takeover:
        print(f'\n# 可接手（原认领已软过期 {CLAIM_TTL_DAYS}/{GIANT_TTL_DAYS} 天；'
              f'先在该 PR 评论询问并等 48 小时）：{len(takeover)} 个')
        for s in takeover[:20]:
            print(render_row(s, resolved))
    return 0


def render_row(sid, resolved):
    r = resolved[sid]
    c = r['claim'] or {}
    return (f'{sid:<28} {r["rows"]:>7} {r["state"]:<14} '
            f'{(c.get("holder") or "-"):<20} {(c.get("since") or "-"):<11} '
            f'{(c.get("pr") or "-"):<10} {r["basis"]}')


def cmd_id(args, sources, resolved, snap, claims, live, live_err):
    extra = [f'源范围：{args.pub_note}'] if getattr(args, 'pub_note', None) else []
    sid = args.id
    if sid not in sources and sid not in resolved:
        print(f'未找到源 {sid}（info/{sid}.json 不存在）', file=sys.stderr)
        return 4
    r = resolved.get(sid) or {'state': FREE, 'rows': 0, 'basis': '—', 'claim': None,
                              'claimable': 'yes'}
    src = sources.get(sid) or {}
    print(f'源 {sid}')
    print(f'  lc 行数        : {r["rows"]}')
    print(f'  审核标记        : {json.dumps(src.get("audit"), ensure_ascii=False) if src.get("audit") else "（无）"}')
    print(f'  状态           : {r["state"]}')
    print(f'  依据           : {r["basis"]}')
    print(f'  可否认领        : {r["claimable"]}')
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
    for ln in source_note(snap, claims, live and not live_err, live_err, extra=extra):
        if ln.startswith(('⚠', '提示', '源范围')):
            print(f'  · {ln}')
    return 0


# ─── 快照生成 ────────────────────────────────────────────────────────────────
def render_snapshot(sources, claims, repo):
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
    text = render_snapshot(sources, claims, repo)
    try:
        atomic_write(args.out or SNAPSHOT, text)
    except OSError as e:
        print(f'[ERROR] 写入失败：{e}', file=sys.stderr)
        return 3
    print(f'已写入 {args.out or SNAPSHOT}：{len(claims)} 个占用源，'
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

    resolved = resolve(sources, claims, snap)
    if args.include_all:
        order = sorted(resolved, key=lambda s: (resolved[s]['state'], resolved[s]['rows'], s))
        for s in order:
            print(render_row(s, resolved))
        return 0
    if args.id:
        if args.id not in sources and args.id in all_sources:
            print(f'源 {args.id} 存在但未发布（.gitignore 排除）→ 不在审核队列范围'
                  f'（如需纳入请加 --include-unpublished）', file=sys.stderr)
            return 5
        return cmd_id(args, sources, resolved, snap, claims, args.live, live_err)
    return cmd_list(args, sources, resolved, snap, claims, live_err)


if __name__ == '__main__':
    sys.exit(main())
