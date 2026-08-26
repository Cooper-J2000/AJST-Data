#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
konus_wind 解析器：Konus-Wind 带红移 GRB 目录（Tsvetkova+ 2017 & 2021）-> normalized.jsonl

输出契约见 ../SCHEMA.md。

输入（VizieR TAP 下载的原始 CSV，见 README.md）：
  J_ApJ_850_161_grbs.csv    2017 合并主表（table1+table2+table4：150 个触发模式暴，
                            含 z、T90、谱延迟 tlagG{2,3}G{1,2}、Eiso、Liso）
  J_ApJ_850_161_table3.csv  2017 谱参数（513 行，每暴 i/p 两类谱，取 BEST 模型的 i 谱 Ep）
  J_ApJ_850_161_table5.csv  2017 准直改正能量学（41 行，Egamma）
  J_ApJ_908_83_table1.csv   2021 等待模式 KW+BAT 联合样本（167 暴，BAT 触发时刻、z）
  J_ApJ_908_83_table2.csv   2021 谱参数（365 行，取 i 谱 Ep）
  J_ApJ_908_83_table4.csv   2021 能量学（167 暴，Eiso/Liso 含上下不对称误差）
  J_ApJ_908_83_table5.csv   2021 准直改正能量学（22 行，Egamma 含不对称误差）

同一 GRB 出现在两年目录时合并为一条记录：互补键合并，同键冲突时 2021 优先。

单位换算（VizieR 原始单位 -> 输出）：
  Eiso   : 1e44 J  = 1e51 erg      -> erg
  Liso   : 1e44 W  = 1e51 erg/s    -> erg/s
  Egamma : 1e42 J  = 1e49 erg      -> erg
  Ep     : keV（观测系，原样）
  tlag   : s（观测系，原样）
"""
import csv
import json
import math
import os
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "normalized.jsonl")

CAT = "konus_wind"
BAND_EISO = "1-10000 keV"   # Eiso/Liso 的静止系能段（论文定义）
# KW 三个通道近似能段（Tsvetkova+ 2017 第 2 节；精确边界随探测器增益略变）
BAND_G2G1 = "G2/G1 (70-300/20-70 keV)"
BAND_G3G1 = "G3/G1 (300-1160/20-70 keV)"
BAND_G3G2 = "G3/G2 (300-1160/70-300 keV)"

MODEL_MAP = {"CPL": "CPL", "BAND": "BAND", "BAND ": "BAND", "PL": "PL"}


def read_csv(fname):
    with open(os.path.join(HERE, fname), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def f(x):
    """空串/空白 -> None，否则 float"""
    if x is None:
        return None
    x = x.strip()
    return float(x) if x else None


def s(x):
    """去空白字符串，空 -> None"""
    if x is None:
        return None
    x = x.strip()
    return x if x else None


def pos_num(x):
    """float，<=0 视为缺失（用于 Ep、Eiso 等 0 占位的情况）"""
    v = f(x)
    return v if v and v > 0 else None


def asym(lo, hi):
    """上下误差 -> [正, 负]；只剩一边用单值；全无 -> None。0 视为缺失。"""
    lo = lo if lo and lo > 0 else None
    hi = hi if hi and hi > 0 else None
    if lo and hi:
        return [float(hi), float(lo)]
    return float(hi or lo) if (hi or lo) else None


def sym(e):
    """对称误差；0/缺失 -> None"""
    return float(e) if e and e > 0 else None


def err_obj(v, err, **extra):
    o = {"v": float(v), "err": err}
    o.update(extra)
    return o


def name17(grb):
    """'970228 ' / '030329A' -> 'GRB 970228' / 'GRB 030329A'"""
    return "GRB " + grb.strip()


def name21(gid):
    """'GRB050126 ' -> 'GRB 050126'"""
    return "GRB " + gid.strip().replace("GRB", "").strip()


def date_of(name):
    """'GRB 970228A' -> date(1997,2,28)"""
    d = name.split()[1][:6]
    yy = int(d[:2])
    year = 1900 + yy if yy > 50 else 2000 + yy
    return datetime(year, int(d[2:4]), int(d[4:6]))


def trig17_iso(name, trig_ms):
    """2017 grbs 表 Trig 列 = 当日毫秒数（已对照原始 table1.dat 的 h/m/s 验证）"""
    base = date_of(name)
    t = base + timedelta(milliseconds=trig_ms)
    return t.strftime("%Y-%m-%dT%H:%M:%S.") + "%03dZ" % (t.microsecond // 1000)


def trig21_iso(name, hms):
    """2021 table1 Time 列 'hh:mm:ss.fff'（Swift/BAT 触发时刻 UT）"""
    base = date_of(name)
    h, m, sec = hms.split(":")
    s_int, ms = sec.split(".")
    t = base + timedelta(hours=int(h), minutes=int(m), seconds=int(s_int),
                         milliseconds=int(ms))
    return t.strftime("%Y-%m-%dT%H:%M:%S.") + "%03dZ" % (t.microsecond // 1000)


def new_rec(name):
    return {"cat": CAT, "name": name, "name_alt": [], "trigger_time": None,
            "ra": None, "dec": None, "params": {}, "other": {}}


def put_other(rec, key, val):
    """写 other；None 跳过；键冲突时旧值改名 <key>_2017 保留"""
    if val is None:
        return
    if key in rec["other"] and rec["other"][key] != val:
        rec["other"].setdefault(key + "_2017", rec["other"][key])
    rec["other"][key] = val


def best_i_row(rows, model_col, flag_col=None):
    """取时间积分谱（SType/Type=='i'）行；2017 优先 f_SMod 标记的 BEST 模型行"""
    irows = [r for r in rows if s(r.get("SType") or r.get("Type")) == "i"]
    if flag_col:
        best = [r for r in irows if (s(r.get(flag_col)) or "").lower().startswith("y")]
        if best:
            irows = best
    return irows[0] if irows else None


def add_epeak(rec, row, model_col):
    """从谱参数行提取观测系 Ep（keV），误差 e_Ep(下)/E_Ep(上) 不对称"""
    ep = pos_num(row.get("Ep"))
    if ep is None:
        return
    err = asym(f(row.get("e_Ep")), f(row.get("E_Ep")))
    model = MODEL_MAP.get((s(row.get(model_col)) or "").upper())
    rec["params"]["epeak"] = err_obj(ep, err, model=model, frame="obs")
    for k in ("alpha", "beta", "tstart", "DeltaT", "dT"):
        v = f(row.get(k))
        if v is not None:
            put_other(rec, "spec_" + k, v)


def geomean_group(rows, vcol, locol, hicol, scale):
    """table5 中同一 GRB 可能含 HM/WM 两行（无偏好介质时两个都算）；
    单行直接用，两行按论文做法取几何平均（2021 ReadMe note 1）"""
    vals = [(pos_num(r.get(vcol)), f(r.get(locol)), f(r.get(hicol)))
            for r in rows]
    vals = [t for t in vals if t[0] is not None]
    if not vals:
        return None
    if len(vals) == 1:
        v, lo, hi = vals[0]
        return v * scale, (lo * scale if lo else None), (hi * scale if hi else None)
    v = math.exp(sum(math.log(t[0]) for t in vals) / len(vals)) * scale
    los = [t[1] for t in vals if t[1]]
    his = [t[2] for t in vals if t[2]]
    lo = math.exp(sum(math.log(x) for x in los) / len(los)) * scale if los else None
    hi = math.exp(sum(math.log(x) for x in his) / len(his)) * scale if his else None
    return v, lo, hi


def main():
    recs = {}

    # ---------- 2017 (J/ApJ/850/161) ----------
    grbs = read_csv("J_ApJ_850_161_grbs.csv")
    t3 = {}
    for r in read_csv("J_ApJ_850_161_table3.csv"):
        t3.setdefault(name17(r["GRB"]), []).append(r)
    t5 = {}
    for r in read_csv("J_ApJ_850_161_table5.csv"):
        t5.setdefault(name17(r["GRB"]), []).append(r)

    for r in grbs:
        name = name17(r["GRB"])
        rec = new_rec(name)
        trig = f(r.get("Trig"))
        if trig is not None:
            rec["trigger_time"] = trig17_iso(name, trig)
        rec["ra"] = f(r.get("_RA"))
        rec["dec"] = f(r.get("_DE"))

        p = rec["params"]
        z = f(r.get("z"))
        if z is not None:
            p["redshift"] = {"v": z}
        lag = f(r.get("tlagG2G1"))
        if lag is not None:
            p["tlag"] = err_obj(lag, sym(f(r.get("e_tlagG2G1"))),
                                band=BAND_G2G1, frame="obs")
        eiso = pos_num(r.get("Eiso"))
        if eiso is not None:
            p["eiso"] = err_obj(eiso * 1e51, sym(f(r.get("e_Eiso")) * 1e51
                                if f(r.get("e_Eiso")) else None),
                                band=BAND_EISO, frame="rest")
        liso = pos_num(r.get("Liso"))
        if liso is not None:
            p["lp_iso"] = err_obj(liso * 1e51, sym(f(r.get("e_Liso")) * 1e51
                                  if f(r.get("e_Liso")) else None),
                                  band=BAND_EISO, frame="rest")

        row = best_i_row(t3.get(name, []), "SMod", "f_SMod")
        if row:
            add_epeak(rec, row, "SMod")

        g = geomean_group(t5.get(name, []), "Egamma", "e_Egamma", "e_Egamma", 1e49)
        if g:
            v, lo, hi = g
            rec["params"]["e_gamma"] = err_obj(v, sym(lo), frame="rest")

        # other：重要原始列（原样单位，见 README）
        for k in ("Type", "Inst", "Det", "n_z", "f_z"):
            put_other(rec, k, s(r.get(k)))
        put_other(rec, "z_type", {"s": "spectroscopic", "p": "photometric"}.get(
            s(r.get("n_z")) or "", s(r.get("n_z"))))
        for k in ("T100", "T90", "e_T90", "T50", "e_T50", "Angle",
                  "tlagG3G1", "e_tlagG3G1", "tlagG3G2", "e_tlagG3G2",
                  "S", "e_S", "E_S", "Fp1024", "e_Fp1024", "E_Fp1024",
                  "Fp64", "e_Fp64", "E_Fp64", "Flim", "Zmax"):
            put_other(rec, k, f(r.get(k)))
        rows5 = t5.get(name, [])
        if rows5:
            r5 = rows5[0]
            for k in ("tjet", "theta", "CBM"):
                put_other(rec, k, f(r5.get(k)) if k != "CBM" else s(r5.get(k)))
            if len(rows5) > 1:
                put_other(rec, "CBM", "HM/WM(geomean)")
            lg = geomean_group(rows5, "Lgamma", "e_Lgamma", "e_Lgamma", 1e49)
            if lg:
                put_other(rec, "Lgamma_1e49erg_s", lg[0])

        recs[name] = rec

    # ---------- 2021 (J/ApJ/908/83)，冲突时优先 ----------
    t1 = {name21(r["ID"]): r for r in read_csv("J_ApJ_908_83_table1.csv")}
    t2 = {}
    for r in read_csv("J_ApJ_908_83_table2.csv"):
        t2.setdefault(name21(r["ID"]), []).append(r)
    t4 = {name21(r["ID"]): r for r in read_csv("J_ApJ_908_83_table4.csv")}
    t5b = {}
    for r in read_csv("J_ApJ_908_83_table5.csv"):
        t5b.setdefault(name21(r["ID"]), []).append(r)

    for name in sorted(set(t1) | set(t4) | set(t5b)):
        rec = recs.get(name)
        if rec is None:
            rec = new_rec(name)
            recs[name] = rec
        r1 = t1.get(name)
        r4 = t4.get(name)

        if r1:
            tm = s(r1.get("Time"))
            if tm:
                rec["trigger_time"] = trig21_iso(name, tm)  # 2021 优先
            num = s(r1.get("NumID"))
            if num:
                alt = "BAT " + num
                if alt not in rec["name_alt"]:
                    rec["name_alt"].append(alt)
            ra, de = f(r1.get("_RA")), f(r1.get("_DE"))
            if ra is not None:
                rec["ra"] = ra
            if de is not None:
                rec["dec"] = de
            put_other(rec, "T100", f(r1.get("T100")))
            put_other(rec, "t0_T100_start", f(r1.get("t0")))
            put_other(rec, "z_type", {"s": "spectroscopic",
                                      "p": "photometric",
                                      "s+p": "spectroscopic+photometric"}.get(
                                          s(r1.get("f_z")) or "", s(r1.get("f_z"))))

        p = rec["params"]
        if r4:
            z = f(r4.get("z"))
            if z is not None:
                p["redshift"] = {"v": z}  # 2021 优先
            eiso = pos_num(r4.get("Eiso"))
            if eiso is not None:
                err = asym(f(r4.get("e_Eiso")) and f(r4.get("e_Eiso")) * 1e51,
                           f(r4.get("E_Eiso")) and f(r4.get("E_Eiso")) * 1e51)
                p["eiso"] = err_obj(eiso * 1e51, err,
                                    band=BAND_EISO, frame="rest")
            liso = pos_num(r4.get("Liso"))
            if liso is not None:
                err = asym(f(r4.get("e_Liso")) and f(r4.get("e_Liso")) * 1e51,
                           f(r4.get("E_Liso")) and f(r4.get("E_Liso")) * 1e51)
                p["lp_iso"] = err_obj(liso * 1e51, err,
                                      band=BAND_EISO, frame="rest")
            for k in ("S", "e_S", "E_S", "Fp1024", "e_Fp1024", "E_Fp1024",
                      "Fp64", "e_Fp64", "E_Fp64"):
                put_other(rec, k, f(r4.get(k)))

        row = best_i_row(t2.get(name, []), "Model")
        if row:
            add_epeak(rec, row, "Model")  # 2021 优先

        g = geomean_group(t5b.get(name, []), "Egamma", "e_Egamma", "E_Egamma", 1e49)
        if g:
            v, lo, hi = g
            p["e_gamma"] = err_obj(v, asym(lo, hi), frame="rest")  # 2021 优先
            rows5 = t5b[name]
            r5 = rows5[0]
            put_other(rec, "tjet", f(r5.get("tJet")))
            put_other(rec, "theta", f(r5.get("theta")))
            put_other(rec, "CBM", "HM/WM(geomean)" if len(rows5) > 1
                      else s(r5.get("CBM")))
            lg = geomean_group(rows5, "Lgamma", "e_Lgamma", "E_Lgamma", 1e49)
            if lg:
                put_other(rec, "Lgamma_1e49erg_s", lg[0])

    # ---------- 输出 ----------
    records = sorted(recs.values(), key=lambda r: r["name"])
    with open(OUT, "w", encoding="utf-8") as fo:
        for r in records:
            fo.write(json.dumps(r, ensure_ascii=False) + "\n")

    keys = ("tlag", "eiso", "lp_iso", "epeak", "e_gamma", "redshift")
    print("records:", len(records))
    for k in keys:
        print("params.%-9s: %d" % (k, sum(1 for r in records if k in r["params"])))
    print("trigger_time:", sum(1 for r in records if r["trigger_time"]))
    print("ra/dec:", sum(1 for r in records if r["ra"] is not None),
          sum(1 for r in records if r["dec"] is not None))
    print("name null:", sum(1 for r in records if not r["name"]))
    both = set(t1) & {name17(r["GRB"]) for r in grbs}
    print("in both 2017&2021:", len(both), sorted(both)[:10])


if __name__ == "__main__":
    main()
