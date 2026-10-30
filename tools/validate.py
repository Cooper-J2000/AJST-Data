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
  - audit/reserved.tsv 维护者预留台账：字段/重复/截止日/已审核残留/未入库源（**警告级**）
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
FLUX_COL = LC_HEADER.index('flux_density')
SRC_COL = LC_HEADER.index('source')
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
PAPER_DIR = os.path.join(LEADS_DIR, 'papers')     # 文献级索引卡：一篇多源文献一张
RESERVED_TSV = os.path.join(ROOT, 'audit', 'reserved.tsv')
RESERVED_COLS = ('source_id', 'holder', 'since', 'until', 'reason', 'ref')
DENIED_TSV = os.path.join(ROOT, 'audit', 'denied.tsv')      # 已否证源清单（人写、工具只读）
DENIED_COLS = ('source_id', 'reason_code', 'evidence', 'decided_by', 'date', 'ref')
DENIED_REASONS = ('retracted', 'duplicate', 'noise', 'other')
UNVERIFIED_TSV = os.path.join(ROOT, 'audit', 'unverified.tsv')   # 未能核实的文献材料（人写、工具只读）
UNVERIFIED_COLS = ('source_id', 'pr', 'paper', 'missing', 'attempted',
                   'blocker', 'substitute', 'status', 'date')
UNVERIFIED_STATUS = ('substituted', 'missing', 'search-limited')
LEAD_KEYS = ('source_id', 'status', 'paper', 'pr', 'helper', 'date')
PAPER_KEYS = ('paper_key', 'paper', 'date', 'helper', 'sources', 'out_of_repo')
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
# 伪形豁免（2026-10-26 维护者裁定，见《数据审核提示词》§3.10 与 Issue #69）：
# 在 comment 里给出「<GCN nnn> … 原文用名」证据串的伪形，视为有出处，不计入普查。
ALIAS_EVIDENCE_KEY = '原文用名'
ALIAS_EVIDENCE_WINDOW = 200
# articles[] 不收 GCN 通告（2026-10-26 维护者裁定，见《数据审核提示词》§3.5）
GCN_ART_RE = re.compile(r'gcn\.(?:gsfc\.nasa|nasa)\.gov', re.I)
# 受控取值（见 SCHEMA.md §2；2026-10-12 新增，按警告级检查）
REDSHIFT_TYPES = {'spec', 'phot', 'upperlimit', 'spec-host', 'value', 'est'}
POS_ERROR_CONF = {'90', '68', '3sigma', '1sigma'}
# 别名伪形普查：逐项收集、最后汇总成一条警告（避免逐源刷屏）
alias_junk = []
alias_exempt = []
gcn_articles = []


def _alias_has_evidence(alias, blob):
    """alias 是否在「原文用名」证据串窗口内、且同窗口给出 GCN 编号。"""
    if not blob:
        return False
    norm = alias.replace(' ', '').upper()
    for m in re.finditer(ALIAS_EVIDENCE_KEY, blob):
        seg = blob[max(0, m.start() - ALIAS_EVIDENCE_WINDOW): m.end() + ALIAS_EVIDENCE_WINDOW]
        if re.search(r'GCN\s*\d{4,5}', seg, re.I) and norm in seg.replace(' ', '').upper():
            return True
    return False

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
        ed0 = d.get('extra_data') if isinstance(d.get('extra_data'), dict) else {}
        blob = ' '.join(str(x) for x in [d.get('comment'), json.dumps(ed0, ensure_ascii=False)] if x)
        for v in al:
            if isinstance(v, str):
                if not v.strip():
                    warn(f'{name}: alias 含空字符串（只收录有出处的名字）')
                elif ALIAS_JUNK_RE.match(v):
                    if _alias_has_evidence(v, blob):
                        alias_exempt.append(f'{name}:{v}')
                    else:
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
                continue
            if GCN_ART_RE.search(str(a.get('url')) + ' ' + str(a.get('name'))):
                gcn_articles.append(f'{name}:{a.get("name")}')

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
    n_empty_flux = 0
    mjd_drift_ex = []
    bad_band_ex = []
    empty_flux_ex = []
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
        # 每行都必须带量值：上限行的限度、探测行的测量值都写进列，只写在 comment 里不算
        # （《数据审核提示词》§3.3 / §8；2026-10-29 维护者裁定，main 基线 0 行为空）
        if not row[FLUX_COL].strip():
            n_empty_flux += 1
            if len(empty_flux_ex) < 3:
                empty_flux_ex.append(f'行{i}(band={row[BAND_COL].strip() or "空"}, '
                                     f'telescope={row[LC_HEADER.index("telescope")].strip() or "空"})')
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
    if n_empty_flux:
        err(f'{name}: {n_empty_flux} 行 flux_density 为空 —— 每行都必须带量值（上限行的限度、'
            f'探测行的测量值），只写在 comment 里不算（《数据审核提示词》§3.3 / §8）'
            f'｜示例：' + '；'.join(empty_flux_ex))
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


ZERO_LC_EVIDENCE_KEYS = ('测光检索', '检索未命中', '未检索到', 'no photometry',
                         'no usable photometry', '无可用测光')


def _split_ids(v):
    return [x.strip() for x in re.split(r'[,，;；\s]+', str(v or ''))
            if x.strip() and x.strip() not in ('无', '-', '—', 'none')]


def check_paper_cards(info_ids):
    """文献级索引卡（警告级，§3.11）：命名/必填键/登记源存在性/一源多卡。

    契约见 `audit/leads/papers/README.md`。文献级卡只承载索引，不参与状态机，
    也不代替源级线索卡；这里只保证它能被工具可靠解析。
    """
    if not os.path.isdir(PAPER_DIR):
        return
    seen = {}
    dois = {}
    for fn in sorted(os.listdir(PAPER_DIR)):
        if not fn.endswith('.md') or fn.lower() == 'readme.md':
            continue
        path = os.path.join(PAPER_DIR, fn)
        rel = f'audit/leads/papers/{fn}'
        key = fn[:-3]
        meta = {}
        try:
            with open(path, encoding='utf-8') as fh:
                for ln in fh:
                    if ln.startswith('##'):
                        break
                    m = LEAD_KEY_RE.match(ln)
                    if m and m.group(1) in PAPER_KEYS and m.group(1) not in meta:
                        meta[m.group(1)] = m.group(2)
        except OSError as e:
            err(f'{rel}: 读取失败（{e}）')
            continue
        if meta.get('paper_key') != key:
            warn(f'{rel}: paper_key={meta.get("paper_key")!r} 与文件名（{key!r}）不一致')
        for k in ('paper', 'date'):
            if not (meta.get(k) or '').strip():
                warn(f'{rel}: 缺 {k}（文献级卡必填 paper_key / paper / date）')
        for doi in re.findall(r'10\.\d{4,}/[^\s）)，,;；]+', meta.get('paper') or ''):
            dois.setdefault(doi.rstrip('.'), []).append(key)
        srcs = _split_ids(meta.get('sources'))
        if not srcs:
            warn(f'{rel}: 缺 sources:（列出该文涉及的库内源，逗号分隔）—— 工具靠它反查'
                 f'「某源被哪篇多源文献提到」')
        for sid in srcs:
            if sid not in info_ids:
                warn(f'{rel}: 登记的源 {sid} 不在 info/ —— 库外新源应改开 new-source Issue，'
                     f'不写进文献级卡')
            seen.setdefault(sid, []).append(key)
    # 一个源被多篇**不同**文献覆盖是正常的（Ershova+2020 与 Fraija+2026 会提到同一批暴），
    # 只有「同一篇文献出现两张卡」才是重复——按 DOI 判，不按源判。
    for doi, keys in dois.items():
        if len(keys) > 1:
            warn(f'audit/leads/papers/: 同一篇文献（DOI {doi}）有 {len(keys)} 张文献级卡'
                 f'（{", ".join(sorted(set(keys)))}）—— 一篇一张，请合并')


def check_zero_lc_evidence(reviewed_ids):
    """零测光源的检索留证（警告级，§3.3）。

    reviewed 且 `lc/<id>.csv` 不存在、`comment` 里又没有任何检索留证痕迹的源 → 警告。
    只看 reviewed：未审的源本来就该有空表，不告警。2026-10-24 之前审核的属历史欠账，
    不要求回溯（提示语里写清）；新审核必须按 §3.3 留证。
    """
    lc_dir = os.path.join(ROOT, 'lc')
    info_dir = os.path.join(ROOT, 'info')
    missing = []
    for sid in sorted(reviewed_ids):
        if os.path.exists(os.path.join(lc_dir, f'{sid}.csv')):
            continue
        try:
            d = json.load(open(os.path.join(info_dir, f'{sid}.json'), encoding='utf-8'))
        except Exception:
            continue
        c = str(d.get('comment') or '')
        if any(k in c for k in ZERO_LC_EVIDENCE_KEYS):
            continue
        missing.append(sid)
    if missing:
        warn(f'零测光留证普查：{len(missing)} 个已 reviewed 的源既无 lc、comment 里也没有测光检索记录'
             f'（例：{", ".join(missing[:3])} …）——《数据审核提示词》§3.3 要求零测光源按'
             f'「检索日期 / 入口与篇数 / 结论 / 补了几行」留证；2026-10-24 前审核的不回溯，'
             f'之后新审核的必须有')


def check_reserved(info_ids, reviewed_ids):
    """维护者预留台账（警告级）：字段完整、不重复、未到期、不留已审核源。

    契约见 audit/README.md。台账是**人写**的权威记录（不是派生物），所以这里只警告不改；
    缺 holder 的行在 audit_queue.py 里按 `?` 保留（fail-closed），这里只提示补全。
    """
    if not os.path.exists(RESERVED_TSV):
        return
    rel = 'audit/reserved.tsv'
    try:
        with open(RESERVED_TSV, encoding='utf-8') as fh:
            lines = fh.read().splitlines()
    except OSError as e:
        warn(f'{rel}: 读取失败（{e}）')
        return
    today = datetime.now().date()
    seen = set()
    for n, ln in enumerate(lines, 1):
        if not ln.strip() or ln.lstrip().startswith('#'):
            continue
        cols = [c.strip() for c in ln.split('\t')]
        if cols[0] == 'source_id':
            continue
        sid = cols[0]
        if not sid:
            warn(f'{rel}:{n}: 首列为空')
            continue
        if sid in seen:
            warn(f'{rel}:{n}: 源 {sid} 重复出现（一行一源）')
            continue
        seen.add(sid)
        row = dict(zip(RESERVED_COLS, cols + [''] * max(0, len(RESERVED_COLS) - len(cols))))
        if not row['holder']:
            warn(f'{rel}:{n}: {sid} 缺 holder（工具按 `?` 保留，仍然是自留态）')
        if not row['until']:
            warn(f'{rel}:{n}: {sid} 缺 until —— 无截止日的预留会变成硬锁，请补日期')
        else:
            try:
                u = datetime.strptime(row['until'][:10], '%Y-%m-%d').date()
            except ValueError:
                warn(f'{rel}:{n}: {sid} 的 until={row["until"]!r} 不是 YYYY-MM-DD')
                u = None
            if u is not None and u < today:
                warn(f'{rel}:{n}: {sid} 的预留已于 {u} 到期 → 续期（改 until）或删掉该行')
        if sid in reviewed_ids:
            warn(f'{rel}:{n}: 源 {sid} 已是 reviewed，预留行应删除')
        if sid not in info_ids:
            warn(f'{rel}:{n}: 源 {sid} 尚未入库（预留仍生效，入库后自动接管）')


def check_unverified(info_ids):
    """未能核实的文献材料登记表（警告级）：格式完整、status 合法、源可定位。

    契约见 audit/README.md 的「unverified.tsv」小节。存在理由：§3.3 要求「补充材料必须先查后取」、
    「拿不到 VoR 要在 comment 与 PR 说明写明尝试路径」，但 PR 正文合并后基本没人回头翻——
    这张表是唯一的结构化汇总入口，让「正文表见在线材料、而在线材料取不到」不再随 PR 沉底。
    「missing」的行不许填 substitute（没拿到就是没拿到），「substituted」必须写清替代覆盖范围。
    """
    if not os.path.exists(UNVERIFIED_TSV):
        return
    rel = 'audit/unverified.tsv'
    denied = set()
    if os.path.exists(DENIED_TSV):
        for ln in open(DENIED_TSV, encoding='utf-8').read().splitlines():
            if ln.strip() and not ln.lstrip().startswith('#'):
                denied.add(ln.split('\t')[0].strip())
    try:
        with open(UNVERIFIED_TSV, encoding='utf-8') as fh:
            lines = fh.read().splitlines()
    except OSError as e:
        warn(f'{rel}: 读取失败（{e}）')
        return
    seen = set()
    for n, ln in enumerate(lines, 1):
        if not ln.strip() or ln.lstrip().startswith('#'):
            continue
        cols = [c.strip() for c in ln.split('\t')]
        if cols[0] == 'source_id':
            continue
        if len(cols) != len(UNVERIFIED_COLS):
            warn(f'{rel}:{n}: {len(cols)} 列（应为 {len(UNVERIFIED_COLS)} 列：'
                 f'{" / ".join(UNVERIFIED_COLS)}）')
            continue
        row = dict(zip(UNVERIFIED_COLS, cols))
        sid = row['source_id']
        if not sid:
            warn(f'{rel}:{n}: source_id 为空（通道级问题写 `*`）')
            continue
        if row['status'] not in UNVERIFIED_STATUS:
            warn(f'{rel}:{n}: {sid} 的 status={row["status"]!r} 不在 '
                 f'{"|".join(UNVERIFIED_STATUS)} 之内')
        for k in ('paper', 'missing', 'attempted', 'blocker', 'date'):
            if not row[k]:
                warn(f'{rel}:{n}: {sid} 缺 {k}（「取不到」必须留得下尝试路径与卡点）')
        if row['date'] and not re.match(r'^\d{4}-\d{2}-\d{2}$', row['date']):
            warn(f'{rel}:{n}: {sid} 的 date={row["date"]!r} 不是 YYYY-MM-DD')
        if row['status'] == 'missing' and row['substitute']:
            warn(f'{rel}:{n}: {sid} status=missing 却填了 substitute（没拿到就是没拿到，'
                 '要写替代来源请改 status=substituted）')
        if sid == '*':
            continue
        key = (sid, row['paper'])
        if key in seen:
            warn(f'{rel}:{n}: {sid} / {row["paper"]} 重复出现')
        seen.add(key)
        if sid not in info_ids and sid not in denied:
            warn(f'{rel}:{n}: 源 {sid} 既不在 info/ 也不在 denied.tsv（写错源 ID？）')


def check_denied(info_ids, lc_ids):
    """已否证源清单（警告级）：字段完整、reason_code 合法、不重复、源不得复活。

    契约见 audit/README.md 的「denied.tsv」小节，背景见 Issue #183。
    核心判据只有一条：**denied 里的源不得再出现 info/lc 文件**——出现了说明源被重新导入/误恢复
    重建了，这时要按 evidence 重新否证，而不是当成新源从头审。
    """
    if not os.path.exists(DENIED_TSV):
        return
    rel = 'audit/denied.tsv'
    try:
        with open(DENIED_TSV, encoding='utf-8') as fh:
            lines = fh.read().splitlines()
    except OSError as e:
        warn(f'{rel}: 读取失败（{e}）')
        return
    seen = set()
    for n, ln in enumerate(lines, 1):
        if not ln.strip() or ln.lstrip().startswith('#'):
            continue
        cols = [c.strip() for c in ln.split('\t')]
        if cols[0] == 'source_id':
            continue
        sid = cols[0]
        if not sid:
            warn(f'{rel}:{n}: 首列为空')
            continue
        if sid in seen:
            warn(f'{rel}:{n}: 源 {sid} 重复出现（一行一源）')
            continue
        seen.add(sid)
        row = dict(zip(DENIED_COLS, cols + [''] * max(0, len(DENIED_COLS) - len(cols))))
        if row['reason_code'] not in DENIED_REASONS:
            warn(f'{rel}:{n}: {sid} 的 reason_code={row["reason_code"]!r} 不在 '
                 f'{"|".join(DENIED_REASONS)} 之内')
        for k in ('evidence', 'decided_by', 'date', 'ref'):
            if not row[k]:
                warn(f'{rel}:{n}: {sid} 缺 {k}（否证必须留得下判据与裁定人）')
        if row['date']:
            try:
                datetime.strptime(row['date'][:10], '%Y-%m-%d')
            except ValueError:
                warn(f'{rel}:{n}: {sid} 的 date={row["date"]!r} 不是 YYYY-MM-DD')
        if sid in info_ids or sid in lc_ids:
            warn(f'{rel}:{n}: 源 {sid} 已被否证（{row["reason_code"]}，{row["ref"]}），'
                 f'但 info/lc 文件又出现了 → 被重新导入/误恢复？按 evidence 再否证一次，不要从头审核')


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
    check_paper_cards(info_ids)

    # 维护者预留台账（警告级；见 audit/README.md 的 reserved.tsv 小节）
    check_reserved(info_ids, reviewed_ids)
    # 已否证源清单（警告级；见 audit/README.md 的 denied.tsv 小节与 Issue #183）
    check_denied(info_ids, {os.path.splitext(f)[0] for f in lc_files})
    check_unverified(info_ids)
    check_zero_lc_evidence(reviewed_ids)

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
        msg = (f'alias 伪形普查：{len(alias_junk)} 项（例：{", ".join(alias_junk[:3])} …）——'
               f'「日期+触发序列」拼接形/截断形不应作为别名，见《数据审核提示词》§3.10 与 Issue #69')
        if alias_exempt:
            msg += (f'；另 {len(alias_exempt)} 项按 §3.10「<GCN nnn> 原文用名」证据串豁免、'
                    f'不计入（例：{", ".join(alias_exempt[:3])}）')
        warn(msg)
    elif alias_exempt:
        warn(f'alias 伪形背书豁免：{len(alias_exempt)} 项有「<GCN nnn> 原文用名」证据串，不计入普查'
             f'（例：{", ".join(alias_exempt[:3])}）——见《数据审核提示词》§3.10')

    if gcn_articles:
        warn(f'articles 含 GCN 通告：{len(gcn_articles)} 条（例：{", ".join(gcn_articles[:3])} …）——'
             f'按 2026-10-26 裁定 GCN 通告不登记进 articles[]，出处只在 comment 与 lc 的 reference 留证，'
             f'见《数据审核提示词》§3.5 与 Issue #69')

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
