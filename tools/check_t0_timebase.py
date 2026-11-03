#!/usr/bin/env python3
"""T0 时间基准守卫 —— 本 PR 改了 `T0`，就必须保证 lc 行 `mjd = T0 + time` 自洽。

背景（2026-11-03 批次实测）：75 个正式 PR 里有 23 个改了 `T0`，其中 **8 个**把 X 射线块
（`band` 含 `keV`，reference=UKSSDC Swift Burst Analyser）漏在旧历元上——`mjd` 仍按旧 `T0`
推出、或 `time` 没随 `T0` 平移，整块偏 1.9 s ~ 21 h（#732 75600 s、#748 18246 s、#798 5.86 s、
#772 63.598 s …）。`validate.py` 对这一现象只有**警告**级检查，作者普遍不知道「改了 T0 要重算」，
于是同一族错误连批复发。本守卫把它变成 PR 上会红的阻断级事实。

判据（与 `validate.py` 同口径，容差默认 1.0 s）：
  * 只看**本 PR 改过的** `info/<id>.json`：`base` 与 `head` 的 `T0` 不同（含 null↔值）；
  * 该源 `lc/<id>.csv` 的每一行都必须满足 `|mjd − (T0 + time/86400)| ≤ 1 s`；
  * **不规定修法**：`mjd` 重算（时间不变）或 `time` 随 T0 平移（mjd 不变）都通过——
    两条路线各自对应不同的来源口径（见《数据审核提示词》§3.8）：
      - XRT/BA 的 `time` 本身就是新 T0 的 T−T0 → 重算 `mjd`（2026-10-31 维护者裁定的「只动 mjd」）；
      - `time` 是旧历元（如 BATSS slew 起点）的 T−T0 → 平移 `time`、`mjd` 不动（#772 实测）。
  * 新源（base 无 info 文件）不检查：没有「T0 改动」，行级自洽由 `validate.py` 警告覆盖。

用法 / Usage：
  python3 tools/check_t0_timebase.py --selftest                      # 离线跑判定用例（不联网、不读 git）
  python3 tools/check_t0_timebase.py --base origin/main --head HEAD   # 本地查当前分支
  python3 tools/check_t0_timebase.py --pr 772 --repo Cooper-J2000/AJST-Data   # 查指定 PR（需 GH_TOKEN）
  python3 tools/check_t0_timebase.py --strict                        # CI：违规非零退出
退出码：0 = 通过；1 = 有 ERROR（`--strict` 时）；2 = 前置失败（拿不到 base/head、查询失败）
"""
import argparse
import csv
import datetime as dt
import io
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_TOL_S = 1.0          # 与 validate.py 的「mjd 与 T0+time 不自洽（差 > 1 s）」同口径
T0_RE = re.compile(r'(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2}):(\d{2}(?:\.\d+)?)')


def mjd_of(iso):
    """ISO8601 → MJD（UTC，按字符串给到的精度，不四舍五入到秒）。"""
    if not iso:
        return None
    m = T0_RE.match(str(iso).strip())
    if not m:
        return None
    y, mo, d, h, mi = (int(m.group(i)) for i in range(1, 6))
    sec = float(m.group(6))
    when = dt.datetime(y, mo, d, h, mi, int(sec), round((sec - int(sec)) * 1e6))
    return (when - dt.datetime(1858, 11, 17)).total_seconds() / 86400.0


def read_rows(text):
    """CSV 文本 → list[dict]（容忍 CRLF / BOM）。"""
    return list(csv.DictReader(io.StringIO(text.replace('\r\n', '\n').lstrip('\ufeff'))))


def evaluate(sid, t0_base, t0_head, rows, tol=DEFAULT_TOL_S, base_exists=True):
    """纯函数：判一个源是否需要重算、以及是否已自洽。返回 (errors, warnings, info)。

    base_exists=False（新源，base 里没有 info 文件）时不检查：没有「T0 改动」，
    行级自洽仍由 `validate.py` 的警告覆盖。
    """
    errors, warnings = [], []
    if not base_exists:
        return errors, warnings, None
    if t0_base is None and t0_head is None:
        return errors, warnings, None
    if (t0_base or '') == (t0_head or ''):
        return errors, warnings, None          # T0 没动，不在本守卫范围
    if not t0_head:
        warnings.append(f'{sid}: 本 PR 把 T0 清成 null，但 lc 仍有 {len(rows)} 行——请确认是否漏删')
        return errors, warnings, None
    t0m = mjd_of(t0_head)
    if t0m is None:
        errors.append(f'{sid}: T0 无法解析（{t0_head!r}）')
        return errors, warnings, None

    bad = []
    for i, r in enumerate(rows, start=2):
        try:
            delta = (float(r['mjd']) - (t0m + float(r['time']) / 86400.0)) * 86400.0
        except (KeyError, TypeError, ValueError):
            continue                            # 空 mjd / time 交给 validate.py
        if abs(delta) > tol:
            bad.append((i, r.get('band', ''), r.get('time', ''), r.get('mjd', ''), delta))
    if bad:
        per = {}
        for _, band, _, _, delta in bad:
            key = 'keV' if 'keV' in (band or '') else band
            per.setdefault(key, []).append(delta)
        groups = '；'.join(f'{k} {len(v)} 行（{min(v):+.3f}~{max(v):+.3f} s）' for k, v in sorted(per.items()))
        ex = '，'.join(f'行{i}({b}, time={t}, mjd={m}, 差 {d:+.3f}s)' for i, b, t, m, d in bad[:3])
        errors.append(f'{sid}: T0 已改为 {t0_head}，但 {len(bad)} 行 mjd 与 T0+time 不自洽 —— {groups}'
                      f'｜示例：{ex}｜修法二选一：① mjd := T0+time（只动 mjd，适用 XRT/BA 等 time 已是新 T0 的 T−T0）；'
                      f'② time 随 T0 平移、mjd 不动（适用 time 取自旧历元）')
    return errors, warnings, {'sid': sid, 't0_base': t0_base, 't0_head': t0_head,
                              'rows': len(rows), 'bad': len(bad)}


# ---------------------------------------------------------------- 数据来源

def git(*a, cwd=None):
    r = subprocess.run(['git', *a], capture_output=True, cwd=cwd)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.decode()[:400])
    return r.stdout.decode('utf-8', 'replace')


def changed_info(base, head, cwd=None):
    try:
        out = git('diff', '--name-only', '--diff-filter=AM', f'{base}...{head}', cwd=cwd)
    except RuntimeError:                      # 浅克隆没有 merge-base（CI 深 1）→ 两点 diff
        out = git('diff', '--name-only', '--diff-filter=AM', base, head, cwd=cwd)
    return [p for p in out.splitlines() if p.startswith('info/') and p.endswith('.json')]


def blob(ref, path, cwd=None):
    r = subprocess.run(['git', 'show', f'{ref}:{path}'], capture_output=True, cwd=cwd)
    return r.stdout.decode('utf-8', 'replace') if r.returncode == 0 else None


def t0_of(text):
    try:
        return json.loads(text).get('T0')
    except (ValueError, AttributeError):
        return None


def from_git(base, head, cwd=None):
    results = []
    for path in changed_info(base, head, cwd=cwd):
        sid = os.path.basename(path)[:-5]
        base_text = blob(base, path, cwd)
        head_text = blob(head, path, cwd) or '{}'
        if base_text is None:                 # 新源：没有「T0 改动」可判
            continue
        t0b, t0h = t0_of(base_text), t0_of(head_text)
        if (t0b or '') == (t0h or ''):
            continue
        lc_text = blob(head, f'lc/{sid}.csv', cwd)
        results.append(evaluate(sid, t0b, t0h, read_rows(lc_text) if lc_text else [],
                                base_exists=True))
    return results


def gh_api(path, token):
    req = urllib.request.Request(f'https://api.github.com{path}',
                                 headers={'Authorization': f'Bearer {token}',
                                          'Accept': 'application/vnd.github+json',
                                          'User-Agent': 'ajst-t0-guard'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def from_pr(repo, n, token):
    import base64

    def content(ref, path):
        try:
            return base64.b64decode(gh_api(
                f'/repos/{repo}/contents/{urllib.parse.quote(path)}?ref={ref}', token)['content']).decode()
        except (urllib.error.HTTPError, KeyError, TypeError, ValueError):
            return None

    pr = gh_api(f'/repos/{repo}/pulls/{n}', token)
    base_sha, head_sha = pr['base']['sha'], pr['head']['sha']
    files, page = [], 1
    while True:
        batch = gh_api(f'/repos/{repo}/pulls/{n}/files?per_page=100&page={page}', token)
        files.extend(batch)
        if len(batch) < 100 or page >= 10:
            break
        page += 1
    results = []
    for f in files:
        path = f['filename']
        if not (path.startswith('info/') and path.endswith('.json')) or f['status'] not in ('modified', 'added'):
            continue
        sid = os.path.basename(path)[:-5]
        base_text = content(base_sha, path)
        if base_text is None:                 # 新源：没有「T0 改动」可判
            continue
        t0b, t0h = t0_of(base_text), t0_of(content(head_sha, path) or '{}')
        if (t0b or '') == (t0h or ''):
            continue
        lc_text = content(head_sha, f'lc/{sid}.csv')
        results.append(evaluate(sid, t0b, t0h, read_rows(lc_text) if lc_text else [],
                                base_exists=True))
    return results


# ---------------------------------------------------------------- 自检

def _mjd(iso, time_s):
    """selftest 辅助：由 T0 + time 反推 mjd 字符串。"""
    v = mjd_of(iso)
    assert v is not None
    return '%.9f' % (v + float(time_s) / 86400.0)


SELFTEST = [
    ('T0 没动 → 不检查', '2026-01-01T00:00:00Z', '2026-01-01T00:00:00Z',
     [{'band': '10keV', 'time': '100', 'mjd': '0'}], 0),
    ('T0 改动 + mjd 已重算 → 通过', '2026-01-01T00:00:00Z', '2026-01-01T00:00:01Z',
     [{'band': '10keV', 'time': '100', 'mjd': _mjd('2026-01-01T00:00:01Z', 100)}], 0),
    ('T0 改动 + mjd 仍按旧 T0 → 违规', '2026-01-01T00:00:00Z', '2026-01-01T00:00:01Z',
     [{'band': '10keV', 'time': '100', 'mjd': _mjd('2026-01-01T00:00:00Z', 100)}], 1),
    ('T0 改动 + time 已随 T0 平移 → 通过', '2026-01-01T00:00:00Z', '2026-01-01T00:00:01Z',
     [{'band': '10keV', 'time': '99', 'mjd': _mjd('2026-01-01T00:00:00Z', 100)}], 0),
    ('亚秒位移 0.5 s 在容差内 → 通过', '2026-01-01T00:00:00Z', '2026-01-01T00:00:00.5Z',
     [{'band': '10keV', 'time': '100', 'mjd': _mjd('2026-01-01T00:00:00Z', 100)}], 0),
    ('新源（base 无 info）→ 不检查', None, '2026-01-01T00:00:00Z',
     [{'band': '10keV', 'time': '100', 'mjd': '1.0'}], 0, False),
    ('T0 清成 null → 只警告', '2026-01-01T00:00:00Z', None,
     [{'band': '10keV', 'time': '100', 'mjd': '1.0'}], 0),
    ('T0 改成不可解析 → 违规', '2026-01-01T00:00:00Z', 'not-a-date',
     [{'band': '10keV', 'time': '100', 'mjd': '1.0'}], 1),
]


def selftest():
    ok = True
    for case in SELFTEST:
        name, t0b, t0h, rows, want_err = case[:5]
        base_exists = case[5] if len(case) > 5 else True
        errors, warnings, _ = evaluate('TEST', t0b, t0h, rows, base_exists=base_exists)
        good = len(errors) == want_err
        ok = ok and good
        print(('PASS' if good else 'FAIL') + f'\t{name}\t错误 {len(errors)}（期望 {want_err}）'
              + (f'\t警告 {len(warnings)}' if warnings else ''))
        if not good:
            for e in errors:
                print('      →', e)
    print('自检结果：' + ('全部通过' if ok else '有失败'))
    return 0 if ok else 1


# ---------------------------------------------------------------- 报告

def report(label, results, strict):
    errors = [e for r in results for e in r[0]]
    warnings = [w for r in results for w in r[1]]
    checked = [r[2] for r in results if r[2]]
    print(f'{label}：{len(checked)} 个源改了 T0（{", ".join(c["sid"] for c in checked) or "无"}）')
    for w in warnings:
        print(('[WARN] ' + w) if not strict else f'::warning::{w}')
    for e in errors:
        print(('[ERROR] ' + e) if not strict else f'::error::{e}')
    if errors:
        print(f'  汇总：{len(errors)} 错误 → FAIL（改了 T0 就必须让 mjd = T0 + time 自洽）')
        return 1
    print('  汇总：0 错误 → PASS')
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base', help='git ref（默认 origin/$GITHUB_BASE_REF 或 origin/main）')
    ap.add_argument('--head', default='HEAD')
    ap.add_argument('--pr', type=int)
    ap.add_argument('--repo', default=os.environ.get('GITHUB_REPOSITORY'))
    ap.add_argument('--repo-path', default='.', help='git 仓库路径（默认当前目录）')
    ap.add_argument('--strict', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    strict = a.strict or bool(os.environ.get('GITHUB_ACTIONS'))
    try:
        if a.pr:
            token = os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
            if not a.repo or not token:
                print('缺少 --repo / token（GH_TOKEN）', file=sys.stderr)
                return 2
            results = from_pr(a.repo, a.pr, token)
            label = f'PR #{a.pr}'
        else:
            base = a.base or f"origin/{os.environ.get('GITHUB_BASE_REF') or 'main'}"
            results = from_git(base, a.head, cwd=a.repo_path)
            label = f'{base}...{a.head}'
    except (RuntimeError, urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as e:
        print(f'前置失败（拿不到 base/head，不要当成通过）：{e}', file=sys.stderr)
        return 2
    return report(label, results, strict)


if __name__ == '__main__':
    sys.exit(main())
