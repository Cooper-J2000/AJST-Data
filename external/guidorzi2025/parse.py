#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
guidorzi2025 解析器：Guidorzi et al. 2024 (A&A 690, A261) GRB 变异性-光度样本
(VizieR J/A+A/690/A261) -> normalized.jsonl

输出契约见 ../SCHEMA.md。
- table1.csv：216 个长暴，变异性 V 按 f=0.8 计算（主表，作为主输出）
- table3.csv：188 个暴（table1 子集），V 按 f=0.45 计算，按暴名合并进 other
每表最后 4 行是长时标并合候选（long-duration merger candidates），论文单独处理，
在 other 里加 long_merger_candidate 标志。

params 只放 variability / lp_iso / redshift；Tf、Det、参考文献编号等放 other。
本目录无触发时刻，仅能从暴名推出日期 -> other["obs_date"]，trigger_time 置 null。
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "normalized.jsonl")

# 变异性 V 所用光变曲线能段（论文摘要）：Swift/BAT 15-150 keV，Fermi/GBM 8-900 keV
BAND = {"BAT": "15-150 keV", "GBM": "8-900 keV"}


def load(fname):
    with open(os.path.join(HERE, fname), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def flt(s):
    return float(s) if s not in (None, "") else None


def obs_date(grb):
    """'050219A' -> '2005-02-19'（样本均在 2000 年后）"""
    yy = int(grb[:2])
    year = 1900 + yy if yy > 50 else 2000 + yy
    return "%04d-%s-%s" % (year, grb[2:4], grb[4:6])


def main():
    t1 = load("table1.csv")
    t3 = load("table3.csv")

    # table3（f=0.45）按暴名索引，用于合并
    v3 = {row["GRB"].strip(): row for row in t3}
    # 每表最后 4 行是长时标并合候选（ReadMe 说明）
    merger = {r["GRB"].strip() for r in t1[-4:]} | {r["GRB"].strip() for r in t3[-4:]}

    records = []
    for row in t1:
        grb = row["GRB"].strip()
        det = row["Det"]

        params = {}
        v = flt(row["Vf"])
        if v is not None:
            params["variability"] = {
                "v": v,
                "err": flt(row["s_Vf"]),
                "band": BAND.get(det),
                "f": 0.8,
            }
        logl, e_logl = flt(row["logLiso"]), flt(row["e_logLiso"])
        if logl is not None:
            lp = {"v": 10.0 ** logl, "frame": "rest"}
            if e_logl is not None:
                # log 空间对称误差 -> 线性空间不对称误差 [正, 负]
                lp["err"] = [lp["v"] * (10.0 ** e_logl - 1.0),
                             lp["v"] * (1.0 - 10.0 ** (-e_logl))]
            params["lp_iso"] = lp
        z = flt(row["z"])
        if z is not None:
            params["redshift"] = {"v": z}

        other = {
            "obs_date": obs_date(grb),
            "Tf": flt(row["Tf"]),
            "e_Tf": flt(row["e_Tf"]),
            "Vf05": flt(row["Vf05"]),
            "Vf95": flt(row["Vf95"]),
            "Det": det,
            "r_logLiso": int(row["r_logLiso"]),
            "Npeaks": int(row["Npeaks"]),
        }
        if grb in merger:
            other["long_merger_candidate"] = True
        # table3（f=0.45）的 V / Tf 并入 other
        r3 = v3.get(grb)
        if r3 is not None:
            other["Vf_f0.45"] = flt(r3["Vf"])
            other["s_Vf_f0.45"] = flt(r3["s_Vf"])
            other["Tf_f0.45"] = flt(r3["Tf"])

        rec = {
            "cat": "guidorzi2025",
            "name": "GRB " + grb,
            "name_alt": [],
            "trigger_time": None,
            "ra": flt(row["_RA"]),
            "dec": flt(row["_DE"]),
            "params": params,
            "other": other,
        }
        records.append(rec)

    with open(OUT, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    p = [r["params"] for r in records]
    print("records:", len(records))
    for key in ("variability", "lp_iso", "redshift"):
        print("with params.%s:" % key, sum(1 for x in p if key in x))
    print("with name:", sum(1 for r in records if r["name"]))
    print("with ra/dec:", sum(1 for r in records if r["ra"] is not None),
          sum(1 for r in records if r["dec"] is not None))
    print("merger candidates:", sum(1 for r in records
                                    if r["other"].get("long_merger_candidate")))
    print("with f=0.45 variability:", sum(1 for r in records
                                            if "Vf_f0.45" in r["other"]))


if __name__ == "__main__":
    main()
