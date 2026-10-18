#!/usr/bin/env python3
"""AJST-Data 数据仓库校验器（纯标准库，无第三方依赖）。

用法 / Usage:
    python3 tools/validate.py            # 全量校验；结构性问题 → 退出码 1
    python3 tools/validate.py --strict   # 值域警告也算失败
    python3 tools/validate.py --quiet    # 只输出汇总

校验范围（契约全文见 SCHEMA.md）：
  - info/*.json   必备键、字段类型、transient_id 与文件名一致、T0 为 ISO8601
  - lc/*.csv      表头恰为 24 列规范、每行 24 字段、time 数值、y/n 列取值、
                  band 落在两条车道内（filters.json 键，或频率/能量串，见 SCHEMA.md §3.1）
  - 互引完整性    lc 文件必须有同名 info（孤儿 CSV 报错）；info 可无 lc（纯信息源合法）
  - audit/leads/ 线索卡命名/status/目标源/已审核残留（**警告级**，不改变数据校验判定）
  - filters.json / tags.json 顶层形状
"""
import csv
import json
import os
import re
import sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LC_HEADER = [
    'time', 'time_err', 'time_unit', 'mjd', 'band', 'flux_density',
    'flux_density_err', 'flux_density_unit', 'mag_system', 'Gext_corr',
    'upperlimit', 'Gext_Alambda', 'mag_Gextcor', 'mag_Gextcor_err',
    'flux_density_Gextcor', 'flux_density_Gextcor_err',
    'flux_density_Gextcor_unit', 'weights', 'discard', 'telescope',
    'instrument', 'reference', 'comment', 'source',
]

# lc 的 band 两条车道（契约见 SCHEMA.md §3.1）：车道一 = filters.json 的键；
# 车道二/二′ = 「数字 + 单位」串（射电 Hz–THz、X 射线光子能量 eV–GeV）。
# 本正则必须与代码仓库 backend/fitting/jobs.py 的 _FREQ_BAND_RE 保持一致，改动时两边同步。
BAND_FREQ_RE = re.compile(
    r'^\s*(\d+(?:\.\d+)?)\s*(Hz|kHz|MHz|GHz|THz|eV|keV|MeV|GeV)\s*$',
    re.IGNORECASE)
BAND_COL = LC_HEADER.index('band')
TIME_COL = LC_HEADER.index('time')
MJD_COL = LC_HEADER.index('mjd')
TIME_UNIT_COL = LC_HEADER.index('time_unit')
# time_unit → 秒（SCHEMA.md §3）
TIME_UNIT_FACTOR = {'s': 1.0, 'sec': 1.0, 'm': 60.0, 'min': 60.0,
                    'h': 3600.0, 'hour': 3600.0, 'd': 86400.0, 'day': 86400.0}
MJD_OFFSET = 40587.0          # datetime.timestamp()/86400 → MJD
MJD_CONSIST_TOL_S = 1.0       # 与三层验收 L3 不变量同一容差

# audit/leads/：多目标文献线索卡（人工维护，不参与审核状态机；契约见 audit/leads/README.md）
LEADS_DIR = os.path.join(ROOT, 'audit', 'leads')
LEAD_KEYS = ('source_id', 'status', 'paper', 'pr', 'helper', 'date')
LEAD_STATUS = {'extracted', 'mention-only'}
LEAD_KEY_RE = re.compile(r'^\s*[-*]?\s*([A-Za-z_]+)\s*[:：]\s*(.+?)\s*$')


def t0_to_mjd(iso):
    """ISO8601 UTC（如 2016-01-19T12:15:00Z）→ MJD；非法/空值返回 None"""
    if not isinstance(iso, str) or not iso:
        return None
    s = iso.strip().replace('Z', '+00:00')
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return None
    if dt.tzinfo is None:
        from datetime import timezone
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp() / 86400.0 + MJD_OFFSET


# info JSON 规范字段集（v2.30 起键恒在，空值显式为 null）
INFO_REQUIRED = {
    'transient_id': str,
    'alias': list,
    'tag': list,
    'sub_tag': list,
    'articles': list,
}
INFO_NULLABLE_STR = ['T0_ref', 'T0_offset_ref', 'Trigger_Instrument',
                     'redshift_type', 'redshift_ref', 'pos_ref', 'comment']
INFO_NULLABLE_NUM = ['ra', 'dec', 'T0_offset', 'redshift', 'pos_error']

# 别名伪形（导入管线产物：「日期+触发序列」拼接 / 10 字符截断；见《数据审核提示词》§3.10）
ALIAS_JUNK_RE = re.compile(r'^GRB ?\d{9}$|^GRB ?\d{5,6}\.\d+$')
# 受控取值（见 SCHEMA.md §2；2026-10-12 新增，按警告级检查）
REDSHIFT_TYPES = {'spec', 'phot', 'upperlimit', 'spec-host', 'value', 'est'}
POS_ERROR_CONF = {'90', '68', '3sigma', '1sigma'}
# 别名伪形普查：逐项收集、最后汇总成一条警告（避免逐源刷屏）
alias_junk = []

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def _is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def check_info(path):
    name = os.path.basename(path)
    try:
        with open(path, encoding='utf-8') as f:
            d = json.load(f)
    except Exception as e:
        err(f'{name}: JSON 解析失败（{e}）')
        return
    if not isinstance(d, dict):
        err(f'{name}: 顶层必须是对象')
        return

    tid = d.get('transient_id')
    if tid != os.path.splitext(name)[0]:
        err(f'{name}: transient_id={tid!r} 与文件名不一致')

    for key, typ in INFO_REQUIRED.items():
        if key not in d:
            err(f'{name}: 缺必备键 {key}')
        elif not isinstance(d[key], typ):
            err(f'{name}: {key} 应为 {typ.__name__}，实为 {type(d[key]).__name__}')

    for key in INFO_NULLABLE_STR:
        if key in d and d[key] is not None and not isinstance(d[key], str):
            err(f'{name}: {key} 应为 string|null')
    for key in INFO_NULLABLE_NUM:
        if key in d and d[key] is not None and not _is_num(d[key]):
            err(f'{name}: {key} 应为 number|null，实为 {d[key]!r}')

    t0 = d.get('T0')
    if t0 is not None:
        if not isinstance(t0, str):
            err(f'{name}: T0 应为 ISO8601 字符串或 null')
        else:
            try:
                datetime.fromisoformat(t0.replace('Z', '+00:00'))
            except ValueError:
                err(f'{name}: T0={t0!r} 不是合法 ISO8601')

    ra, dec = d.get('ra'), d.get('dec')
    if ra is not None and _is_num(ra) and not (0 <= ra <= 360):
        warn(f'{name}: ra={ra} 超出 [0,360]')
    if dec is not None and _is_num(dec) and not (-90 <= dec <= 90):
        err(f'{name}: dec={dec} 超出 [-90,90]')

    for key in ('alias', 'tag', 'sub_tag'):
        if isinstance(d.get(key), list):
            for i, v in enumerate(d[key]):
                if not isinstance(v, str):
                    err(f'{name}: {key}[{i}] 应为字符串，实为 {v!r}')

    # 别名格式（警告级，见《数据审核提示词》§3.10）
    al = d.get('alias')
    if isinstance(al, list):
        for v in al:
            if isinstance(v, str):
                if not v.strip():
                    warn(f'{name}: alias 含空字符串（只收录有出处的名字）')
                elif ALIAS_JUNK_RE.match(v):
                    alias_junk.append(f'{name}:{v}')

    # 受控取值（警告级，见 SCHEMA.md §2）
    rt = d.get('redshift_type')
    if rt is not None and rt not in REDSHIFT_TYPES:
        warn(f'{name}: redshift_type={rt!r} 不在受控取值 {sorted(REDSHIFT_TYPES)} 内')
    pc = d.get('pos_error_confidence')
    if pc is not None and pc not in POS_ERROR_CONF:
        warn(f'{name}: pos_error_confidence={pc!r} 不在受控取值 {sorted(POS_ERROR_CONF)} 内')

    if 'pos_error_unit' in d and d['pos_error_unit'] is not None \
            and not isinstance(d['pos_error_unit'], str):
        err(f'{name}: pos_error_unit 应为 string|null')

    ed = d.get('extra_data')
    if ed is not None and not isinstance(ed, dict):
        err(f'{name}: extra_data 应为 object|null')

    arts = d.get('articles')
    if isinstance(arts, list):
        for i, a in enumerate(arts):
            if not isinstance(a, dict) or not a.get('name') or not a.get('url'):
                err(f'{name}: articles[{i}] 缺 name/url 或不是对象')

    hg = d.get('host_galaxy')
    if hg is not None:
        if not isinstance(hg, dict):
            err(f'{name}: host_galaxy 应为 object|null')
        else:
            for key in ('ra', 'dec', 'redshift', 'redshift_err'):
                if key in hg and hg[key] is not None and not _is_num(hg[key]):
                    err(f'{name}: host_galaxy.{key} 应为 number|null')
            if 'photometry' in hg and not isinstance(hg['photometry'], list):
                err(f'{name}: host_galaxy.photometry 应为数组')
            if 'derived' in hg and not isinstance(hg['derived'], dict):
                err(f'{name}: host_galaxy.derived 应为对象')


def check_lc(path, band_keys, t0_by_id=None):
    name = os.path.basename(path)
    mjd0 = t0_to_mjd((t0_by_id or {}).get(name[:-4]))
    try:
        with open(path, newline='', encoding='utf-8') as f:
            rows = list(csv.reader(f))
    except Exception as e:
        err(f'{name}: CSV 读取失败（{e}）')
        return
    if not rows:
        err(f'{name}: 空文件')
        return
    if rows[0] != LC_HEADER:
        err(f'{name}: 表头与 24 列规范不一致（见 SCHEMA.md）')
        return
    n_bad_width = n_bad_time = n_empty_band = n_bad_band = 0
    n_mjd_drift = 0
    mjd_drift_ex = []
    bad_band_ex = []
    for i, row in enumerate(rows[1:], start=2):
        if len(row) != len(LC_HEADER):
            n_bad_width += 1
            continue
        try:
            float(row[TIME_COL])
        except ValueError:
            n_bad_time += 1
        # mjd ↔ T0+time 自洽（《数据审核提示词》§3.2 / SCHEMA.md §3；警告级、按文件聚合）
        if mjd0 is not None and row[MJD_COL].strip() and row[TIME_COL].strip():
            try:
                f_t = TIME_UNIT_FACTOR.get(row[TIME_UNIT_COL].strip(), 1.0)
                drift = abs(float(row[TIME_COL]) * f_t
                            - (float(row[MJD_COL]) - mjd0) * 86400.0)
                if drift > MJD_CONSIST_TOL_S:
                    n_mjd_drift += 1
                    if len(mjd_drift_ex) < 3:
                        mjd_drift_ex.append(f'行{i}(mjd={row[MJD_COL].strip()}, '
                                            f'time={row[TIME_COL].strip()}'
                                            f'{row[TIME_UNIT_COL].strip()}, 差 {drift:.1f}s)')
            except ValueError:
                pass
        for col in ('Gext_corr', 'upperlimit', 'discard'):
            v = row[LC_HEADER.index(col)]
            if v not in ('y', 'n', ''):
                warn(f'{name}:{i}: {col}={v!r} 应为 y/n')
        # band 两条车道（SCHEMA.md §3.1）；filters.json 不可用时只判频率/能量串车道
        b = row[BAND_COL].strip()
        if not b:
            n_empty_band += 1
        elif band_keys and b not in band_keys and not BAND_FREQ_RE.match(b):
            n_bad_band += 1
            if len(bad_band_ex) < 3:
                bad_band_ex.append(b)
    if n_bad_width:
        err(f'{name}: {n_bad_width} 行字段数 ≠ 24')
    if n_bad_time:
        warn(f'{name}: {n_bad_time} 行 time 非数值')
    if n_empty_band:
        err(f'{name}: {n_empty_band} 行 band 为空（SCHEMA.md §3 band 为必填）')
    if n_bad_band:
        err(f'{name}: {n_bad_band} 行 band 不在两条车道内（应为 filters.json 的键，或频率/能量串'
            f'如 4.86GHz、10keV；见 SCHEMA.md §3.1）｜示例：' + '、'.join(bad_band_ex))
    if n_mjd_drift:
        warn(f'{name}: {n_mjd_drift} 行 mjd 与 T0+time 不自洽（差 > {MJD_CONSIST_TOL_S:g} s）'
             f'—— 由 T0+time 换算的 mjd 须保留 7 位小数（4–5 位小数的舍入就会超过 1 s，'
             f'见 SCHEMA.md §3 / 《数据审核提示词》§3.2）｜示例：' + '；'.join(mjd_drift_ex))


def check_leads(info_ids, reviewed_ids):
    """线索卡一致性（警告级）：文件名=source_id、status 合法、目标源存在、已审核源不留卡。"""
    if not os.path.isdir(LEADS_DIR):
        return
    seen = {}
    for fn in sorted(os.listdir(LEADS_DIR)):
        if not fn.endswith('.md') or fn.lower() == 'readme.md':
            continue
        path = os.path.join(LEADS_DIR, fn)
        rel = f'audit/leads/{fn}'
        sid = fn[:-3]
        meta = {}
        try:
            with open(path, encoding='utf-8') as f:
                for ln in f:
                    if ln.startswith('##'):        # 元数据区到此结束
                        break
                    m = LEAD_KEY_RE.match(ln)
                    if m and m.group(1) in LEAD_KEYS and m.group(1) not in meta:
                        meta[m.group(1)] = m.group(2)
        except OSError as e:
            err(f'{rel}: 读取失败（{e}）')
            continue
        if meta.get('source_id') != sid:
            warn(f'{rel}: source_id={meta.get("source_id")!r} 与文件名（源 id={sid!r}）不一致')
        if sid not in info_ids:
            warn(f'{rel}: 目标源 info/{sid}.json 不存在 —— 新源应改开 new-source Issue'
                 f'（《数据审核提示词》§3.11）')
        st = (meta.get('status') or '').strip()
        if st not in LEAD_STATUS:
            warn(f'{rel}: status={st!r} 应为 extracted / mention-only')
        elif st == 'extracted' and not (meta.get('paper') or '').strip():
            warn(f'{rel}: status=extracted 但缺 paper 出处')
        seen.setdefault(sid, []).append(fn)
        if sid in reviewed_ids:
            warn(f'{rel}: 源 {sid} 已是 reviewed，线索卡应在其审核 PR 中删除（§3.11）')
    for sid, fns in seen.items():
        if len(fns) > 1:
            warn(f'audit/leads/: 源 {sid} 有 {len(fns)} 张线索卡'
                 f'（{", ".join(fns)}）—— 每源一张，冲突时合并')


def main():
    strict = '--strict' in sys.argv
    quiet = '--quiet' in sys.argv

    # filters.json 先加载：lc 的 band 校验要用它的键集（车道一）
    band_keys = set()
    fj = os.path.join(ROOT, 'filters.json')
    if not os.path.exists(fj):
        err('filters.json: 缺失（band 车道一无法校验）')
    else:
        try:
            with open(fj, encoding='utf-8') as f:
                d = json.load(f)
            if not isinstance(d, dict) or not d:
                err('filters.json: 应为非空对象')
            else:
                band_keys = set(d)
                for k, v in d.items():
                    if not isinstance(v, dict) or not _is_num(v.get('wavelength')):
                        err(f'filters.json: {k} 缺数值 wavelength')
                        break
        except Exception as e:
            err(f'filters.json: 解析失败（{e}）')
    if not band_keys:
        warn('filters.json 不可用 → lc 的 band 一律跳过车道一判定（根因已单独报错，'
             '避免逐行洪水）；修好 filters.json 后重跑')

    info_dir = os.path.join(ROOT, 'info')
    lc_dir = os.path.join(ROOT, 'lc')
    info_files = sorted(f for f in os.listdir(info_dir) if f.endswith('.json'))
    lc_files = sorted(f for f in os.listdir(lc_dir) if f.endswith('.csv')) \
        if os.path.isdir(lc_dir) else []

    t0_by_id = {}
    reviewed_ids = set()
    for f in info_files:
        p = os.path.join(info_dir, f)
        check_info(p)
        sid = os.path.splitext(f)[0]
        try:
            with open(p, encoding='utf-8') as fh:
                d = json.load(fh)
            t0_by_id[sid] = d.get('T0')
            audit = (d.get('extra_data') or {}).get('audit') or {}
            if isinstance(audit, dict) and str(audit.get('status') or '').strip().lower() == 'reviewed':
                reviewed_ids.add(sid)
        except Exception:
            pass          # 解析失败已由 check_info 报错
    for f in lc_files:
        check_lc(os.path.join(lc_dir, f), band_keys, t0_by_id)

    # 互引：lc 必须有同名 info（反向不要求 —— 纯信息源合法）
    info_ids = {os.path.splitext(f)[0] for f in info_files}
    for f in lc_files:
        if os.path.splitext(f)[0] not in info_ids:
            err(f'lc/{f}: 孤儿光变文件（无同名 info JSON）')

    # 线索卡一致性（警告级；多目标文献交接，见《数据审核提示词》§3.11）
    check_leads(info_ids, reviewed_ids)

    # tags.json 顶层形状
    tj = os.path.join(ROOT, 'tags.json')
    if os.path.exists(tj):
        try:
            d = json.load(open(tj, encoding='utf-8'))
            if not isinstance(d, list) or any(
                    not isinstance(x, dict) or 'name' not in x or 'kind' not in x
                    for x in d):
                err('tags.json: 应为 [{name, kind, ...}] 数组')
        except Exception as e:
            err(f'tags.json: 解析失败（{e}）')

    if alias_junk:
        warn(f'alias 伪形普查：{len(alias_junk)} 项（例：{", ".join(alias_junk[:3])} …）——'
             f'「日期+触发序列」拼接形/截断形不应作为别名，见《数据审核提示词》§3.10 与 Issue #69')

    if not quiet:
        for m in errors:
            print(f'[ERROR] {m}')
        for m in warnings:
            print(f'[warn ] {m}')
    print(f'校验完成：{len(info_files)} 个 info / {len(lc_files)} 个 lc；'
          f'{len(errors)} 个错误，{len(warnings)} 个警告')
    if errors or (strict and warnings):
        sys.exit(1)


if __name__ == '__main__':
    main()
