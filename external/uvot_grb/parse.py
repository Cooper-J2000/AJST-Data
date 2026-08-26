#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
uvot_grb 解析器：Swift/UVOT 第二版 GRB 余辉目录（Roming et al. 2017, ApJS, 228, 13）

输入：hlsp_uvotgrb_swift_uvot_all_multi_v1_grb-cat.fits（626 行 × 349 列，BinTable 在第 1 扩展）
输出：normalized.jsonl（每行一条记录，契约见 ../SCHEMA.md）

提取：T90(+ref/能段)、BAT fluence(15-150 keV)、BAT 1s 峰光子流、BAT 光子指数(PL/CPL)。
缺失记号（逐列清洗，见 README.md "发现的坑"）：
  BAT_FL/BAT_FL_ERR: -1.0e-07（物理上不可能的小负数，统一按 <0 判缺失）
  BAT_PPF/BAT_PPF_ERR/BAT_PI/BAT_PI_ERR: -1.00（按 <0 判缺失）
  T90: 2 行为 0（GRB090515、GRB100628A），视为缺失
  Z: -1.0；字符串列: 'NULL'；BAT_PIT 缺失实为字符串 '-1.00'，另有 1 行怪值 '(PL)'
注意：BAT 四参数误差为 90% 置信（cl=90），非 1σ。

运行：python3 parse.py（需要 astropy；输入 FITS 需从 MAST HLSP 下载，见 README.md）
"""
import json
import os
from datetime import datetime, timedelta

from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
FITS_PATH = os.path.join(
    HERE, "hlsp_uvotgrb_swift_uvot_all_multi_v1_grb-cat.fits"
)
OUT_PATH = os.path.join(HERE, "normalized.jsonl")

BAT_BAND = "15-150 keV"

# DISC_BY 旗标 → T90 能段（README：Swift 15-350 keV，HETE2 30-400 keV，个别 80-400 keV）
DISC_BY_NAME = {
    0: "Swift", 1: "HETE2", 2: "INTEGRAL", 3: "IPN",
    4: "Fermi", 5: "BATSS", 6: "AGILE", 7: "Swift(ground)",
}


def t90_band(disc_by):
    if disc_by in (0, 5, 7):  # Swift / BAT Slew Survey / Swift 地面分析
        return "15-350 keV"
    if disc_by == 1:  # HETE2
        return "30-400 keV"
    return None  # 其他仪器能段不确定，按契约写 null


def clean_str(v):
    """FITS 字符串列：strip；'NULL'/空 → None。"""
    s = str(v).strip()
    return s if s and s.upper() != "NULL" else None


def norm_name(obj):
    """'GRB050117' / 'GRB051021A' -> 'GRB 050117' / 'GRB 051021A'。"""
    s = clean_str(obj)
    if s is None:
        return None
    if s.startswith("GRB"):
        return "GRB " + s[3:]
    return s


def parse_trig_ut(s):
    """'2005-017-12:52:36'（年-年积日-时分秒）-> ISO UTC。"""
    s = clean_str(s)
    if s is None:
        return None
    try:
        y, doy, hms = s.split("-", 2)
        dt = datetime(int(y), 1, 1) + timedelta(days=int(doy) - 1)
        hh, mm, ss = hms.split(":")
        dt = dt.replace(hour=int(hh), minute=int(mm), second=int(float(ss)))
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except (ValueError, TypeError):
        return None


def pos_float(v):
    """转 float；缺失记号（负值占位）-> None。用于以负号为缺失记号的列。"""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    if f != f or f < 0:  # NaN 或负值缺失记号（-1.0e-07 / -1.00 / -99 等）
        return None
    return f


def main():
    tab = fits.getdata(FITS_PATH, 1)
    n_out = 0
    with open(OUT_PATH, "w") as fo:
        for row in tab:
            obj_raw = clean_str(row["OBJECT"])
            disc_by = int(row["DISC_BY"])

            params = {}

            # T90（观测系；0 视为缺失；误差目录未给 -> null）
            t90 = float(row["T90"])
            if t90 == t90 and t90 > 0:
                params["t90"] = {"v": t90, "err": None, "band": t90_band(disc_by)}

            # BAT fluence，15-150 keV，观测系；误差 90% 置信
            fl = pos_float(row["BAT_FL"])
            if fl is not None:
                params["fluence"] = {
                    "v": fl,
                    "err": pos_float(row["BAT_FL_ERR"]),
                    "band": BAT_BAND,
                    "cl": 90,
                }

            # BAT 1s 峰值光子流量，15-150 keV；误差 90% 置信
            ppf = pos_float(row["BAT_PPF"])
            if ppf is not None:
                params["peak_flux"] = {
                    "v": ppf,
                    "err": pos_float(row["BAT_PPF_ERR"]),
                    "band": BAT_BAND,
                    "dt": "1s",
                    "cl": 90,
                }

            # BAT 光子指数（PL 简单幂律 / CPL 截断幂律，模型存 other.BAT_PIT）；误差 90% 置信
            pi = pos_float(row["BAT_PI"])
            if pi is not None:
                params["spectral_index"] = {
                    "v": pi,
                    "err": pos_float(row["BAT_PI_ERR"]),
                    "cl": 90,
                }

            # 红移（目录自带；缺失 = -1.0）
            z = pos_float(row["Z"])
            if z is not None:
                params["redshift"] = {"v": z}

            # BAT_PIT：合法模型 PL/CPL；缺失 '-1.00'/'NULL'，怪值 '(PL)' 归为 PL
            pit = clean_str(row["BAT_PIT"])
            if pit in ("-1.00",):
                pit = None
            elif pit == "(PL)":
                pit = "PL"

            rec = {
                "cat": "uvot_grb",
                "name": norm_name(obj_raw),
                "name_alt": [],
                "trigger_time": parse_trig_ut(row["TRIG_UT"]),
                "ra": float(row["RA"]),
                "dec": float(row["DEC"]),
                "params": params,
                "other": {
                    "OBJECT": obj_raw,
                    "DISC_BY": DISC_BY_NAME.get(disc_by, str(disc_by)),
                    "TRIGTIME": float(row["TRIGTIME"]),  # Swift MET 秒（2001-01-01 UTC 起算）
                    "TRIG_UT": clean_str(row["TRIG_UT"]),
                    "POS_ERR": float(row["POS_ERR"]),    # 角秒
                    "POS_REF": clean_str(row["POS_REF"]),
                    "T90_REF": clean_str(row["T90_REF"]),  # SGA 或 GCNnnnn
                    "BAT_PIT": pit,                        # PL=简单幂律, CPL=截断幂律
                },
            }
            fo.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n_out += 1
    print(f"wrote {n_out} records -> {OUT_PATH}")


if __name__ == "__main__":
    main()
