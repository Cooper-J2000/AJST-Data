#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
wang2022 解析器：Wang et al. 2022 (MNRAS 516, 2575) Eiso-Ep 校准样本
ms.tex 附录 longtable (221 行长 GRB) -> normalized.jsonl

输出契约见 ../SCHEMA.md。
表中 E_p 已是宇宙学静止系值 -> ep_rest；E_iso 原始单位 1e52 erg，换算成 erg；
红移列无误差 -> redshift 只有 v；数据引用编号 (1)-(5) 原样放入 other["Refs"]。
"""
import re
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "ms.tex")
OUT = os.path.join(HERE, "normalized.jsonl")

# 060218 & 0.034 & 4.90 $\pm$ 0.30 & 0.0054 $\pm$ 0.0003 & (1) \\  \hline
ROW_RE = re.compile(
    r"^\s*(\d{6}[A-Z]?)\s*&\s*([\d.]+)\s*&\s*([\d.]+)\s*\$\\pm\$\s*([\d.]+)"
    r"\s*&\s*([\d.]+)\s*\$\\pm\$\s*([\d.]+)\s*&\s*(\(\d\))\s*\\\\"
)

E52 = 1.0e52  # Eiso 原始单位


def main():
    raw = open(SRC, encoding="utf-8").read()
    # 只取附录 longtable 段（caption 含 "221 GRBs"）
    seg = raw.split(r"\begin{longtable}", 1)[1]
    seg = seg.split(r"\caption{\label{GRBsample}")[0]

    records = []
    skipped = []
    for line in seg.splitlines():
        m = ROW_RE.match(line)
        if not m:
            if "&" in line and "\\hline" in line:
                skipped.append(line.strip())
            continue
        name_raw, z, ep, ep_err, eiso, eiso_err, ref = m.groups()

        params = {
            "ep_rest": {"v": float(ep), "err": float(ep_err), "frame": "rest"},
            "eiso": {"v": float(eiso) * E52, "err": float(eiso_err) * E52,
                     "frame": "rest"},
            "redshift": {"v": float(z)},
        }
        rec = {
            "cat": "wang2022",
            "name": "GRB " + name_raw,
            "name_alt": [],
            "trigger_time": None,
            "ra": None,
            "dec": None,
            "params": params,
            "other": {"Refs": ref},
        }
        records.append(rec)

    with open(OUT, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print("records:", len(records))
    print("skipped non-row lines with '&':", len(skipped))
    for s in skipped:
        print("  SKIP:", s)
    for key in ("ep_rest", "eiso", "redshift"):
        print("with params.%s:" % key,
              sum(1 for r in records if key in r["params"]))
    zs = [r["params"]["redshift"]["v"] for r in records]
    eps = [r["params"]["ep_rest"]["v"] for r in records]
    eisos = [r["params"]["eiso"]["v"] for r in records]
    print("z range: %.3f - %.3f" % (min(zs), max(zs)))
    print("Ep range: %.2f - %.2f keV" % (min(eps), max(eps)))
    print("Eiso range: %.3e - %.3e erg" % (min(eisos), max(eisos)))


if __name__ == "__main__":
    main()
