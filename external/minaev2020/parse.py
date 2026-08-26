#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
minaev2020 解析器：Minaev & Pozanenko 2020 (MNRAS 492, 1919) Table A1
(VizieR J/MNRAS/492/1919/tablea1, CSV) -> normalized.jsonl

输出契约见 ../SCHEMA.md。T90i/Epi 为静止系值；Eiso 原始单位 1e44 J
(=1e51 erg)，输出 eiso 时换算成 erg。Type 列映射为 grb_type I/II。
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "tablea1.csv")
OUT = os.path.join(HERE, "normalized.jsonl")

EISO_UNIT = 1e51  # Eiso 原始单位：10^44 J = 10^51 erg（VizieR ReadMe 标注）

# Type -> grb_type（I+EE 归 I；II+SNph/II+SNsp 归 II）
TYPE_MAP = {
    "I": "I",
    "I+EE": "I",
    "II": "II",
    "II+SNph": "II",
    "II+SNsp": "II",
}


def fnum(s):
    """空串/缺失记号 -> None，否则 float"""
    s = s.strip()
    return float(s) if s else None


def make_err(pos, neg, scale=1.0):
    """对称误差给单值，不对称给 [正, 负]；任一缺失返回 None"""
    pos = fnum(pos)
    neg = fnum(neg)
    if pos is None or neg is None:
        return None
    pos, neg = pos * scale, neg * scale
    return pos if pos == neg else [pos, neg]


def main():
    records = []
    with open(SRC, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            grb = row["GRB"].strip()
            name = "GRB " + grb
            simbad = row["SimbadName"].strip()

            params = {}
            params["ep_rest"] = {
                "v": fnum(row["Epi"]),
                "err": make_err(row["E_Epi"], row["e_Epi"]),
                "frame": "rest",
            }
            params["eiso"] = {
                "v": fnum(row["Eiso"]) * EISO_UNIT,
                "err": make_err(row["E_Eiso"], row["e_Eiso"], EISO_UNIT),
                "band": None,
                "frame": "rest",
            }
            params["t90"] = {
                "v": fnum(row["T90i"]),
                "err": None,
                "band": None,
                "frame": "rest",
            }
            gtype = TYPE_MAP.get(row["Type"].strip())
            if gtype:
                params["grb_type"] = {"v": gtype}
            z = {"v": fnum(row["z"])}
            z_err = make_err(row["E_z"], row["e_z"])
            if z_err is not None:
                z["err"] = z_err
            params["redshift"] = z

            other = {
                "recno": int(row["recno"]),
                "Type": row["Type"].strip(),
                "Exp": row["Exp"].strip(),
                "Ref": row["Ref"].strip(),
                "EH": fnum(row["EH"]),
                "EHtype": row["EHtype"].strip(),
                "EHD": fnum(row["EHD"]),
                "EHDtype": row["EHDtype"].strip(),
            }
            if row["f_GRB"].strip():
                # '*' = 该源的 Eiso/Epi 由本文作者自行计算
                other["f_GRB"] = row["f_GRB"].strip()
            if row["f_z"].strip():
                # 'PH' = 测光红移
                other["f_z"] = row["f_z"].strip()

            rec = {
                "cat": "minaev2020",
                "name": name,
                "name_alt": [simbad] if simbad and simbad != name else [],
                "trigger_time": None,
                "ra": fnum(row["_RA"]),
                "dec": fnum(row["_DE"]),
                "params": params,
                "other": other,
            }
            records.append(rec)

    with open(OUT, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    def cov(key):
        return sum(1 for r in records if key in r["params"])

    print("records:", len(records))
    for k in ["ep_rest", "eiso", "t90", "grb_type", "redshift"]:
        print("params.%s: %d" % (k, cov(k)))
    print("redshift with err:", sum(1 for r in records
                                   if "err" in r["params"]["redshift"]))
    print("grb_type I:", sum(1 for r in records
                             if r["params"].get("grb_type", {}).get("v") == "I"),
          "II:", sum(1 for r in records
                      if r["params"].get("grb_type", {}).get("v") == "II"))
    print("name nonnull:", sum(1 for r in records if r["name"]))
    print("ra/dec nonnull:", sum(1 for r in records if r["ra"] is not None),
          sum(1 for r in records if r["dec"] is not None))
    print("name_alt:", sum(1 for r in records if r["name_alt"]))
    print("f_GRB:", sum(1 for r in records if "f_GRB" in r["other"]),
          "f_z:", sum(1 for r in records if "f_z" in r["other"]))


if __name__ == "__main__":
    main()
