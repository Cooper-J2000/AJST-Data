#!/usr/bin/env python3
"""JD→MJD 换算守卫 —— `comment` 里引了原文 JD 的行，`mjd` 必须等于 `JD − 2400000.5`。

背景（2026-11-21/22 实测）：同一族错误连批复发——作者把 `mjd = JD − 2400000` 当成换算，
少了 0.5 天，整行时刻晚 **12 h**：
  * PR #922（AT2019kyw，Ho+2023 表 4 的 9 行）：L6–L14 全掉 `.5`，而同文件 L2–L5 是对的；
  * PR #1113（AT2024kt，TNS phot 4 行）：60314.9215 应为 60314.4215。
`validate.py` 只查 `|mjd − (T0+time)| ≤ 1 s` 这**条内部自洽性**——`mjd` 与 `time` 一起错时
自洽性完美成立，校验器全绿（#922 的 CI 就是绿的）。唯一能抓住它的是「拿注释里的原文 JD 反算」。

判据（只认 ±0.5 d 这个指纹，误报率极低）：
  对每行 `comment` 里的每个 `JD 24xxxxx[.xxx]`：`expected = JD − 2400000.5`，
  `delta = mjd − expected`（天）：
    |delta| ≤ tol                 → OK
    |delta − 0.5| ≤ tol           → ERROR「少减 0.5 d（写成 JD−2400000）」
    |delta + 0.5| ≤ tol           → ERROR「多减 0.5 d（写成 JD−2400001）」
    其它                          → WARN（多为交叉引用其它行/其它曝光的 JD，不阻断）
  容差默认 0.02 d ≈ 29 min（原文 JD 常只给到 0.01 d，故不能卡太紧）。

用法 / Usage：
  python3 tools/check_jd_mjd.py --selftest                     # 离线跑判定用例
  python3 tools/check_jd_mjd.py                                # 扫全部 lc/*.csv（CI 用）
  python3 tools/check_jd_mjd.py --files lc/AT2019kyw.csv       # 只扫指定文件
  python3 tools/check_jd_mjd.py --base origin/main --head HEAD # 只扫本分支改过的 lc
  python3 tools/check_jd_mjd.py --strict                       # 有 ERROR 即非零退出（CI）
退出码：0 = 通过（可带 WARN）；1 = 有 ERROR（--strict 时）；2 = 前置失败
"""
import argparse
import csv
import io
import os
import re
import subprocess
import sys

TOL_D = 0.02                      # ≈29 min：原文 JD 常只给到 0.01 d
JD_RE = re.compile(r'JD\s*(24\d{5}(?:\.\d+)?)')
SENTINEL = 2400000.5
LC_DIR = 'lc'


def scan_text(text, sid):
    """返回 [(行号, 分类, 说明)]，分类 ∈ {'ERROR','WARN'}（OK 不入表）。"""
    out = []
    rd = list(csv.reader(io.StringIO(text)))
    if not rd:
        return out
    hdr = rd[0]
    idx = {c: i for i, c in enumerate(hdr)}
    if 'mjd' not in idx or 'comment' not in idx:
        return out
    for ln, row in enumerate(rd[1:], 2):
        if not row or len(row) != len(hdr):
            continue
        try:
            mjd = float(row[idx['mjd']])
        except (TypeError, ValueError):
            continue
        com = row[idx['comment']] or ''
        for m in JD_RE.finditer(com):
            # 「T0=JD 2460563.66718」这类把 JD 当 T0 声明（不是本行观测时刻）→ 跳过
            ctx = com[max(0, m.start() - 12):m.start()]
            if re.search(r'T0\s*[=＝]?\s*$', ctx):
                continue
            try:
                jd = float(m.group(1))
            except ValueError:
                continue
            delta = mjd - (jd - SENTINEL)
            tag = None
            why = ''
            if abs(delta) <= TOL_D:
                continue
            elif abs(delta - 0.5) <= TOL_D:
                tag = 'ERROR'
                why = (f'少减 0.5 d：注释原文 JD {m.group(1)} → 应 mjd={jd-SENTINEL:.5f}，'
                       f'行内是 {mjd:.5f}（晚 {(delta)*24:.2f} h）')
            elif abs(delta + 0.5) <= TOL_D:
                tag = 'ERROR'
                why = (f'多减 0.5 d：注释原文 JD {m.group(1)} → 应 mjd={jd-SENTINEL:.5f}，'
                       f'行内是 {mjd:.5f}（早 {(-delta)*24:.2f} h）')
            else:
                tag = 'WARN'
                why = (f'与注释原文 JD 相差 {delta*24:+.2f} h（非 ±12 h 指纹，'
                       f'多为交叉引用其它曝光/其它源的 JD，需人看一眼）')
            out.append((ln, tag, f'{sid}:{ln}: {why}'))
    return out


def changed_lc(base, head):
    r = subprocess.run(['git', 'diff', '--name-only', f'{base}..{head}', '--', f'{LC_DIR}/'],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f'git diff 失败：{r.stderr.strip()[:200]}')
    return [p for p in r.stdout.splitlines() if p.endswith('.csv') and os.path.exists(p)]


def all_lc():
    if not os.path.isdir(LC_DIR):
        return []
    return sorted(os.path.join(LC_DIR, f) for f in os.listdir(LC_DIR) if f.endswith('.csv'))


def selftest():
    """离线用例：三种指纹 + 交叉引用 + 正常行。"""
    hdr = 'time,time_err,time_unit,mjd,band,flux_density,flux_density_err,flux_density_unit,mag_system,Gext_corr,upperlimit,Gext_Alambda,mag_Gextcor,mag_Gextcor_err,flux_density_Gextcor,flux_density_Gextcor_err,flux_density_Gextcor_unit,weights,discard,telescope,instrument,reference,comment,source\r\n'
    def row(mjd, com):
        return (f'0,,s,{mjd},g,20.0,0.1,magnitude,AB,n,n,,,,,,,1.0,n,P48,ZTF-Cam,GCN1,{com},t\r\n')
    text = (hdr
            + row('58670.1800000', '原文 JD 2458670.68')                 # OK
            + row('58673.6800000', '原文 JD 2458673.68')                 # ERROR 少减 .5
            + row('58666.2000000', '原文 JD 2458667.20')                 # ERROR 多减 .5
            + row('58673.1800000', '交叉引用的同曝光 TNS 行 JD 2459610.90')  # WARN
            + row('60563.6542201', 'T0=JD 2460563.66718＝Fermi 触发；本行 mjd=T0+time')  # 跳过
            + row('58673.1800000', '无 JD'))
    got = scan_text(text, 'TEST')
    tags = [t for _, t, _ in got]
    exp = ['ERROR', 'ERROR', 'WARN']
    ok = tags == exp
    print(f'selftest: 分类 {tags} 期望 {exp} → {"PASS" if ok else "FAIL"}')
    for ln, t, msg in got:
        print('   ', msg)
    return ok


def main(argv):
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument('--files', nargs='*')
    ap.add_argument('--base')
    ap.add_argument('--head', default='HEAD')
    ap.add_argument('--strict', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv[1:])
    if a.selftest:
        return 0 if selftest() else 1
    try:
        files = a.files or (changed_lc(a.base, a.head) if a.base else all_lc())
    except Exception as e:                       # 前置失败 ≠ 通过
        print(f'[前置失败] {e}', file=sys.stderr)
        return 2
    errs, warns, rows = 0, 0, 0
    for p in files:
        try:
            text = open(p, encoding='utf-8', errors='replace').read()
        except OSError:
            continue
        rows += max(0, text.count('\n') - 1)
        for ln, tag, msg in scan_text(text, os.path.basename(p)[:-4]):
            if tag == 'ERROR':
                errs += 1
                print(f'[ERROR] {msg}')
            else:
                warns += 1
                if warns <= 20:          # 存量交叉引用很多，只示例前 20 条
                    print(f'[warn ] {msg}')
    print(f'检查 {len(files)} 个 lc 文件 / {rows} 行：{errs} 个错误，{warns} 个告警')
    if errs and a.strict:
        print('修法：`mjd = JD − 2400000.5`；若该行 `time` 是相对 T0 的秒数，'
              '同时 `time = (mjd − T0_mjd) × 86400`。', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
