#!/usr/bin/env python3
"""数据体检（只读）：Fermi/GBM 系源的 T0 是否漏扣闰秒。

背景：库内一批源（`extra_data.catalog_data.fermi_lat` 来自 Fermi LAT 2FLGC）的 T0 是
2FLGC `trigger_met`（MET，2001-01-01T00:00:00 UTC 起算的连续秒）**直接**换算成 UTC 得到的，
没有扣除期间插入的闰秒 ⇒ T0 比真实触发时刻晚 1–5 秒（2006/2009/2012-07/2015-07/2017 各插一秒）。

本脚本对每个这种源：
  1. 取 trigger_met 的整数部分（= GBM trigger number）→ 抓 GCN/Fermi 官方通告页
     https://gcn.gsfc.nasa.gov/other/<trigger>.fermi 的 GRB_DATE（yy/mm/dd）+ GRB_TIME <sod> SOD；
  2. 与库内 T0 相减得 Δ = T0 − 官方通告时刻；
  3. 与「该时刻之前累计插入的闰秒数」比较：Δ 相等 ⇒ 确证为漏扣闰秒；Δ=0 ⇒ 口径本就正确。

用法（只读，不写库、不改文件）：
    python3 tools/scan_met_leapsecond.py                 # 输出汇总
    python3 tools/scan_met_leapsecond.py --tsv out.tsv    # 逐源明细（TSV）
    python3 tools/scan_met_leapsecond.py --cache DIR      # 通告页缓存目录（默认系统临时目录）
"""
import argparse
import csv
import glob
import json
import os
import re
import sys
import tempfile
import time
import urllib.request
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INFO = os.path.join(ROOT, 'info')
UA = {'User-Agent': 'Mozilla/5.0 (ajst-data scan)'}
# 2001-01-01 之后插入的闰秒（UTC 生效时刻）
LEAP = [datetime(2006, 1, 1, tzinfo=timezone.utc), datetime(2009, 1, 1, tzinfo=timezone.utc),
        datetime(2012, 7, 1, tzinfo=timezone.utc), datetime(2015, 7, 1, tzinfo=timezone.utc),
        datetime(2017, 1, 1, tzinfo=timezone.utc)]


def n_leap(dt):
    return sum(1 for x in LEAP if x <= dt)


def fetch(trigger, cache):
    p = os.path.join(cache, '%s.fermi' % trigger)
    if os.path.exists(p):
        return open(p, encoding='utf-8', errors='replace').read()
    for _ in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(
                    'https://gcn.gsfc.nasa.gov/other/%s.fermi' % trigger, headers=UA), timeout=30) as r:
                txt = r.read().decode('utf-8', 'replace')
            if txt.strip().startswith('<!DOCTYPE') or 'Not Found' in txt[:200]:
                return ''
            open(p, 'w').write(txt)
            return txt
        except Exception:
            time.sleep(2)
    return ''


def sources():
    out = []
    for f in sorted(glob.glob(os.path.join(INFO, '*.json'))):
        js = json.load(open(f, encoding='utf-8'))
        ed = js.get('extra_data') or {}
        fl = (ed.get('catalog_data') or {}).get('fermi_lat') or {}
        tm = (fl.get('other') or {}).get('trigger_met')
        if tm:
            out.append((js['transient_id'], js.get('T0'), float(tm),
                        (ed.get('audit') or {}).get('status') == 'reviewed', js.get('T0_offset')))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--tsv')
    ap.add_argument('--cache', default=os.path.join(tempfile.gettempdir(), 'ajst_gcn_notice'))
    a = ap.parse_args()
    os.makedirs(a.cache, exist_ok=True)
    rows, no_notice = [], []
    for sid, T0, tm, audited, off in sources():
        trig = str(int(tm))
        txt = fetch(trig, a.cache)
        m = re.search(r'GRB_DATE:\s*(\d+)\s*TJD;\s*(\d+)\s*DOY;\s*(\d\d)/(\d\d)/(\d\d)', txt)
        mt = re.search(r'GRB_TIME:\s*([\d.]+)\s*SOD\s*\{([\d:.]+)\}', txt)
        if not (m and mt and T0):
            no_notice.append(sid)
            continue
        yy, mm, dd = int(m.group(3)), int(m.group(4)), int(m.group(5))
        notice = datetime(2000 + yy if yy < 70 else 1900 + yy, mm, dd, tzinfo=timezone.utc) \
            + timedelta(seconds=float(mt.group(1)))
        t0 = datetime.fromisoformat(T0.replace('Z', '+00:00'))
        rows.append({'id': sid, 't0': T0, 'notice_utc': notice.isoformat().replace('+00:00', 'Z'),
                     'delta_s': round((t0 - notice).total_seconds(), 3), 'leap': n_leap(t0),
                     'audited': audited, 't0_offset': off})
    exact = [r for r in rows if abs(r['delta_s'] - r['leap']) <= 0.05]
    zero = [r for r in rows if abs(r['delta_s']) <= 0.05]
    other = [r for r in rows if r not in exact and r not in zero]
    unaud = [r for r in exact if not r['audited']]
    print('fermi_lat 系源（有 trigger_met）: %d' % (len(rows) + len(no_notice)))
    print('可与官方通告页比对          : %d（无通告页 %d）' % (len(rows), len(no_notice)))
    print('Δ == 该日累计闰秒数（确证漏扣）: %d，其中未审核 %d' % (len(exact), len(unaud)))
    print('Δ == 0（口径正确）           : %d' % len(zero))
    print('其他异常（需单独查）          : %d  %s' % (len(other), [(r['id'], r['delta_s']) for r in other]))
    if a.tsv:
        with open(a.tsv, 'w', encoding='utf-8', newline='') as fh:
            w = csv.writer(fh, delimiter='\t', lineterminator='\n')
            w.writerow(['id', 'lib_T0', 'official_notice_utc', 'delta_s', 'true_trigger=T0-delta',
                        'audited', 't0_offset'])
            for r in sorted(exact, key=lambda x: x['id']):
                t0 = datetime.fromisoformat(r['t0'].replace('Z', '+00:00'))
                w.writerow([r['id'], r['t0'], r['notice_utc'], r['leap'],
                            (t0 - timedelta(seconds=r['leap'])).isoformat().replace('+00:00', 'Z'),
                            r['audited'], r['t0_offset']])
        print('已写逐源明细: %s' % a.tsv)


if __name__ == '__main__':
    sys.exit(main())
