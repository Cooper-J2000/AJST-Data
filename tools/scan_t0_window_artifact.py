#!/usr/bin/env python3
"""扫「T0 = 观测窗口边界」这类导入残留（只读，纯标准库）。

背景（Issue #68 家族）：`gcn_llm_extract` 会把 GCN 通告里观测窗口的**结束时刻**当成 trigger-time。
已确证 2 例：AT2026nuz（原值 = COLIBRÍ 窗口结束）、GRB260529A（库值 = GOTO 观测 "through to
04:55:50 UT (+2.10 h post trigger)" 的结束）。本脚本用仓内外部目录快照做**全库普查**。

判据（两级）：
  A 类「目录不一致」：库 T0 与所有可比对的目录触发时刻都差 > --tol 秒（默认 60）。
  B 类「整数边界」：在 A 类基础下，Δ 与整数分钟（60/120/…/7200 s）的差 ≤ --snap 秒（默认 5）
     或与整点半（1800 s 的倍数）的差 ≤ --snap —— 观测窗口结束时刻几乎总是这种整分/整半点，
     真实触发时刻不会。B 类是**强怀疑**，A 类只能算「需人工看」。

快照来源：`external/*/normalized.jsonl`（cat/name/name_alt/trigger_time）。只用有 trigger_time 的目录。

用法 / Usage:
  python3 tools/scan_t0_window_artifact.py                 # 汇总 + B 类明细（前 40 行）
  python3 tools/scan_t0_window_artifact.py --all           # 连 A 类明细一起打
  python3 tools/scan_t0_window_artifact.py --tsv out.tsv   # 全量落盘（只读，不改任何数据）
  python3 tools/scan_t0_window_artifact.py --id GRB260529A # 单源依据
  python3 tools/scan_t0_window_artifact.py --gcn-check     # 用本地 GCN 存档取证（关键一步）
退出码：0 正常（无论命中与否）；2 参数错误。
"""
import argparse
import glob
import json
import os
import re
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INFO_DIR = os.path.join(ROOT, 'info')
EXT_DIR = os.path.join(ROOT, 'external')
EPOCH = datetime(1858, 11, 17, tzinfo=timezone.utc)
CANON_RE = re.compile(r'[^A-Za-z0-9]')
GCN_DIR = os.path.join(ROOT, 'gcn', 'archive')
# 把 T0 的钟点当成"观测时刻"而不是触发时刻的语境特征（GCN 原文里）
OBS_WORDS = ('observ', 'exposur', 'started', 'starting', 'from ', ' to ', 'UT',
             'telescope', 'imager', 'camera', 'field of', 'follow')
RANGE_RE = re.compile(r'\d{1,2}:\d{2}\s*(?:-|–|to)\s*\d{1,2}:\d{2}')


def canon(s):
    """归一化源名：去空格/点/下划线，大写。GRB 260529A 与 GRB260529A 等价。"""
    return CANON_RE.sub('', str(s)).upper()


def parse_t(s):
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(str(s).replace('Z', '+00:00'))
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def load_ref_index():
    """→ {canon(名): [(cat, name, datetime)]}；只收有 trigger_time 的目录条目。"""
    idx = {}
    for path in sorted(glob.glob(os.path.join(EXT_DIR, '*', 'normalized.jsonl'))):
        cat = os.path.basename(os.path.dirname(path))
        try:
            fh = open(path, encoding='utf-8')
        except OSError:
            continue
        with fh:
            for ln in fh:
                ln = ln.strip()
                if not ln:
                    continue
                try:
                    d = json.loads(ln)
                except ValueError:
                    continue
                t = parse_t(d.get('trigger_time'))
                if not t:
                    continue
                names = [d.get('name')] + list(d.get('name_alt') or [])
                for nm in names:
                    if not nm:
                        continue
                    idx.setdefault(canon(nm), []).append((cat, nm, t))
    return idx


def classify(t0, delta_s, basis, tol, snap):
    """→ 'P' 占位 / 'W' 窗口边界强怀疑 / 'B2' 整分且晚于触发 / 'B3' 整分但早于触发 / 'A' 其他 / None

    P：T0 是「日期 + 00:00:00」或 basis=name_date —— 数据缺失占位，不是窗口残留。
    W：|Δ|>tol 且 T0 的秒为 00、Δ 落在整分/半小时边界（≤snap）且**晚于**目录触发时刻。
       观测窗口的结束/开始时刻几乎总是这种整分时刻；两个已确证案例都落在这里。
    """
    if t0.strftime('%H:%M:%S') == '00:00:00' or basis == 'name_date':
        return 'P'
    a = abs(delta_s)
    if a <= tol:
        return None
    on_boundary = any(abs(a / base - round(a / base)) * base <= snap for base in (60.0, 1800.0))
    if not on_boundary:
        return 'A'
    if delta_s > 0 and t0.strftime('%S') == '00':
        return 'W'
    return 'B2' if delta_s > 0 else 'B3'


def load_gcn_index():
    """→ {canon(eventId): [circular dict]}；本地 GCN 存档（gcn/archive/*.json，可再生成、不进 git）。"""
    idx = {}
    if not os.path.isdir(GCN_DIR):
        return idx
    for path in glob.glob(os.path.join(GCN_DIR, '*.json')):
        try:
            d = json.load(open(path, encoding='utf-8'))
        except Exception:
            continue
        ev = d.get('eventId')
        if ev:
            idx.setdefault(canon(ev), []).append(d)
    return idx


def gcn_evidence(sid, t0_str, gidx, aliases=()):
    """该源的 circular 里是否出现过 T0 的这个钟点，且语境是观测而非触发。

    → (kind, circularId, snippet) 或 None；kind ∈ {'obs'（观测窗口语境，强证据）, 'mention'}
    """
    if not t0_str or len(t0_str) < 19:
        return None
    keys = {canon(sid)} | {canon(a) for a in aliases if a}
    hhmmss, hhmm = t0_str[11:19], t0_str[11:16]
    best = None
    for k in keys:
        for d in gidx.get(k, []):
            body = d.get('body') or ''
            for pat in (hhmmss, hhmm):
                i = body.find(pat)
                if i < 0:
                    continue
                snip = body[max(0, i - 110):i + 110].replace('\n', ' ')
                low = snip.lower()
                is_obs = bool(RANGE_RE.search(snip)) or any(w.lower() in low for w in OBS_WORDS)
                rec = (0 if is_obs else 1, d.get('circularId'), 'obs' if is_obs else 'mention', snip)
                if best is None or rec[0] < best[0]:
                    best = rec
                break
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tol', type=float, default=60.0, help='与目录触发时刻的容差秒（默认 60）')
    ap.add_argument('--snap', type=float, default=5.0, help='整数分钟的贴合容差秒（默认 5）')
    ap.add_argument('--all', action='store_true', help='打印 A 类明细')
    ap.add_argument('--tsv', metavar='PATH', help='全量 TSV 落盘')
    ap.add_argument('--id', metavar='源ID', help='只看一个源的依据')
    ap.add_argument('--gcn-check', action='store_true',
                    help='用本地 gcn/archive 取证：T0 钟点是否出现在该源的观测窗口描述里（慢 ~10 s）')
    args = ap.parse_args()

    idx = load_ref_index()
    rows = []
    for path in sorted(glob.glob(os.path.join(INFO_DIR, '*.json'))):
        sid = os.path.splitext(os.path.basename(path))[0]
        if args.id and sid != args.id:
            continue
        try:
            d = json.load(open(path, encoding='utf-8'))
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        t0 = parse_t(d.get('T0'))
        if not t0:
            continue
        names = [sid] + [a for a in (d.get('alias') or []) if isinstance(a, str)]
        refs = []
        for nm in names:
            refs.extend(idx.get(canon(nm), []))
        if args.id and not refs:
            print(f'{sid}: 无任何目录触发时刻可比对（alias={d.get("alias")}）')
            return 0
        if not refs:
            continue
        best = min(refs, key=lambda r: abs((t0 - r[2]).total_seconds()))
        delta = (t0 - best[2]).total_seconds()
        _ed = d.get('extra_data') if isinstance(d.get('extra_data'), dict) else {}
        cls = classify(t0, delta, _ed.get('t0_basis'), args.tol, args.snap)
        if not cls:
            continue
        ed = _ed
        audit = ed.get('audit') if isinstance(ed, dict) else None
        rows.append({
            'id': sid,
            'class': cls,
            'delta_s': round(delta, 3),
            'T0': d.get('T0'),
            'catalog': best[0],
            'catalog_name': best[1],
            'catalog_trigger': best[2].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'n_refs': len(refs),
            't0_basis': ed.get('t0_basis') if isinstance(ed, dict) else None,
            'T0_ref': (d.get('T0_ref') or '')[:60],
            'trigger_instrument': d.get('Trigger_Instrument'),
            'reviewed': bool(isinstance(audit, dict) and str(audit.get('status') or '').lower() == 'reviewed'),
            'aliases': names[1:],
        })

    if args.gcn_check:
        gidx = load_gcn_index()
        print(f'# 本地 GCN 存档：{len(gidx)} 个 eventId（gcn/archive）')
        for r in rows:
            ev = gcn_evidence(r['id'], r['T0'], gidx, r['aliases'])
            r['gcn_circ'], r['gcn_kind'], r['gcn_snip'] = (ev[1], ev[2], ev[3]) if ev else ('', '', '')
        n_obs = sum(1 for r in rows if r.get('gcn_kind') == 'obs')
        print(f'# 取证结果：{n_obs}/{len(rows)} 个命中源的 circular 里，T0 钟点出现在**观测语境**中'
              f'（其余为仅提及或未提及）')

    if args.id:
        for r in rows:
            print(json.dumps({k: v for k, v in r.items() if k != 'aliases'}, ensure_ascii=False, indent=2))
        if not rows:
            print(f'{args.id}: T0 与可比的目录触发时刻一致（≤{args.tol:.0f} s），未命中')
        return 0

    cls_order = {'W': 0, 'B2': 1, 'B3': 2, 'A': 3, 'P': 4}
    rows.sort(key=lambda r: (cls_order.get(r['class'], 9), -abs(r['delta_s'])))
    by = {}
    for r in rows:
        by.setdefault(r['class'], []).append(r)
    w = by.get('W', [])
    print(f'# 快照目录索引：{len(idx)} 个源名；命中合计 {len(rows)} 个')
    print('# 分层：'
          f'W 窗口边界强怀疑 {len(by.get("W", []))}'
          f' / B2 整分且晚于触发 {len(by.get("B2", []))}'
          f' / B3 整分但早于触发 {len(by.get("B3", []))}'
          f' / A 其他不一致 {len(by.get("A", []))}'
          f' / P 占位（日期+00:00:00，单列）{len(by.get("P", []))}'
          f'；其中已 reviewed {sum(1 for r in rows if r["reviewed"])} 个')
    if args.gcn_check:
        print(f'# GCN 取证：W 类中 {sum(1 for r in w if r.get("gcn_kind") == "obs")}/{len(w)} '
              f'在原文里是「观测窗口」语境')

    def show(r):
        rb = 'reviewed' if r['reviewed'] else '未审'
        line = (f'{r["class"]:<3} {r["id"]:<20} Δ={r["delta_s"]:>10.3f}s  {rb:<8} {r["catalog"]:<12} '
                f'{r["catalog_name"]:<16} 目录={r["catalog_trigger"]}  库 T0={r["T0"]}'
                f'  basis={r["t0_basis"]}')
        if r.get('gcn_kind'):
            line += f'\n    ↳ GCN {r["gcn_circ"]} [{r["gcn_kind"]}]: …{r["gcn_snip"][:200]}…'
        return line

    if w:
        print('\n## W 类（T0 的秒为 00、Δ 落在整分/半小时边界、且晚于目录触发时刻 —— 观测窗口边界强怀疑）')
        for r in w:
            print(show(r))
    if args.all:
        for cls, title in (('B2', 'B2 类（整分边界且晚于触发，但秒不为 00）'),
                           ('B3', 'B3 类（整分边界但早于触发）'),
                           ('A', 'A 类（与目录差 > 容差但不在整分边界；可能是仪器/纪元差异）'),
                           ('P', 'P 类（T0 = 日期 + 00:00:00 或 basis=name_date，属数据缺失占位）')):
            lst = by.get(cls, [])
            if not lst:
                continue
            print(f'\n## {title}')
            for r in lst[:40]:
                print(show(r))
            if len(lst) > 40:
                print(f'… 另 {len(lst) - 40} 行见 --tsv')

    if args.tsv:
        cols = ['id', 'class', 'delta_s', 'T0', 'catalog', 'catalog_name', 'catalog_trigger',
                'n_refs', 't0_basis', 'trigger_instrument', 'reviewed', 'T0_ref',
                'gcn_kind', 'gcn_circ', 'gcn_snip']
        with open(args.tsv, 'w', encoding='utf-8') as fh:
            fh.write('\t'.join(cols) + '\n')
            for r in rows:
                fh.write('\t'.join(str(r.get(c, '')).replace('\t', ' ').replace('\n', ' ')
                                    for c in cols) + '\n')
        print(f'\n已写入 {args.tsv}（{len(rows)} 行）')
    return 0


if __name__ == '__main__':
    sys.exit(main())
