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


def check_lc(path, band_keys):
    name = os.path.basename(path)
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
    bad_band_ex = []
    for i, row in enumerate(rows[1:], start=2):
        if len(row) != len(LC_HEADER):
            n_bad_width += 1
            continue
        try:
            float(row[0])
        except ValueError:
            n_bad_time += 1
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

    for f in info_files:
        check_info(os.path.join(info_dir, f))
    for f in lc_files:
        check_lc(os.path.join(lc_dir, f), band_keys)

    # 互引：lc 必须有同名 info（反向不要求 —— 纯信息源合法）
    info_ids = {os.path.splitext(f)[0] for f in info_files}
    for f in lc_files:
        if os.path.splitext(f)[0] not in info_ids:
            err(f'lc/{f}: 孤儿光变文件（无同名 info JSON）')

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
