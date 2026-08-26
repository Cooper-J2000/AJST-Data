#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fermi_gbm 解析器：heasarc_fermigbrst.tdat.gz -> normalized.jsonl

按 ../SCHEMA.md 契约输出。要点：
- tdat 格式：<HEADER> 段用 field[名] 定义列序；<DATA>..<END> 为数据区，
  竖线分隔，行尾多一个 '|'，缺失值为空字符串。
- name 为 GRByymmddfff（小数日，9 位数字）时无法确定字母后缀 -> name=null，
  但保留 trigger_time / ra / dec；GRByymmddX（6 位+字母）-> "GRB yymmddX"。
- epeak：取 flnc_best_fitting_model 对应模型的 epeak 进 params（band/comp），
  另一模型的 epeak 原样留在 other。pos/neg err 同时为 0.0 表示参数被固定
  -> err=null 且加 "fixed": true。
- peak_flux：params 放 64ms（10-1000 keV）；256/1024ms 及 BATSE 带版本留 other。
- fluence：params 放 bcat fluence（能段按 flu_low/flu_high 逐行标注）；
  fluence_batse（50-300 keV）留 other。
- 本目录无红移、无静止系量 -> 无 eiso/redshift。
"""
import gzip
import json
import os
import re
import sys

from astropy.time import Time

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "heasarc_fermigbrst.tdat.gz")
OUT = os.path.join(HERE, "normalized.jsonl")

# params.epeak 的 model 标注（flnc_best_fitting_model 值 -> SCHEMA 模型名）
MODEL_MAP = {"flnc_band": "BAND", "flnc_comp": "CPL", "flnc_plaw": "PL", "flnc_sbpl": "SBPL"}


def to_float(s):
    """空串/无法解析 -> None，否则 float。"""
    if s is None:
        return None
    s = s.strip()
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def mjd_to_iso(mjd):
    if mjd is None:
        return None
    t = Time(mjd, format="mjd", scale="utc")
    return t.to_value("isot", subfmt="date_hms") + "Z"


def norm_name(raw):
    """返回 (name, decimal_grb_name)。

    name: 'GRB yymmddX' / 'GRB yymmdd' / None（小数日格式无法确定后缀）。
    decimal_grb_name: 'GRB yymmdd.fff'，恒可由 yymmddfff 构造，作为 name_alt。
    """
    raw = raw.strip().replace(" ", "")
    m = re.match(r"^GRB(\d{6})(\d{3})$", raw)          # 小数日 GRByymmddfff
    if m:
        return None, "GRB %s.%s" % (m.group(1), m.group(2))
    m = re.match(r"^GRB(\d{6})([A-Z])$", raw)          # GRByymmddX
    if m:
        return "GRB %s%s" % (m.group(1), m.group(2)), None
    m = re.match(r"^GRB(\d{6})$", raw)                 # GRByymmdd
    if m:
        return "GRB %s" % m.group(1), None
    return None, None


def asym_err(pos, neg):
    """非对称误差。均为 0.0 => 参数固定（err=None, fixed=True）；空 => None。"""
    if pos is None and neg is None:
        return None, False
    if pos == 0.0 and neg == 0.0:
        return None, True
    return [pos, neg], False


def main():
    # --- 读 header 取列序 ---
    cols = []
    rows = []
    in_data = False
    with gzip.open(RAW, "rt", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            if not in_data:
                m = re.match(r"^field\[(\w+)\]", line)
                if m:
                    cols.append(m.group(1))
                elif line.strip() == "<DATA>":
                    in_data = True
                continue
            if line.strip() == "<END>":
                break
            if line.strip() == "":
                continue
            fields = line.split("|")
            if fields and fields[-1] == "":     # 行尾多一个 '|'
                fields = fields[:-1]
            if len(fields) != len(cols):
                print("WARN: 字段数 %d != 列数 %d, 行: %s" % (len(fields), len(cols), line[:80]),
                      file=sys.stderr)
                continue
            rows.append(dict(zip(cols, fields)))

    print("列数 %d, 数据行 %d" % (len(cols), len(rows)))

    n_out = 0
    stats = {"t90": 0, "t50": 0, "epeak": 0, "epeak_fixed": 0, "fluence": 0,
             "peak_flux": 0, "name_null": 0}
    with open(OUT, "w", encoding="utf-8") as fo:
        for r in rows:
            g = {k: to_float(v) for k, v in r.items()}

            raw_name = r["name"].strip()
            name, dec_name = norm_name(raw_name)
            trig = r["trigger_name"].strip()
            name_alt = []
            if name != raw_name:
                name_alt.append(raw_name)
            if dec_name:
                name_alt.append(dec_name)
            name_alt.append(trig)
            if name is None:
                stats["name_null"] += 1

            dur_band = None
            if g.get("duration_energy_low") is not None and g.get("duration_energy_high") is not None:
                dur_band = "%g-%g keV" % (g["duration_energy_low"], g["duration_energy_high"])
            flu_band = None
            if g.get("flu_low") is not None and g.get("flu_high") is not None:
                flu_band = "%g-%g keV" % (g["flu_low"], g["flu_high"])

            params = {}
            # t90 / t50（bcat，50-300 keV）
            if g.get("t90") is not None:
                params["t90"] = {"v": g["t90"], "err": g.get("t90_error"), "band": dur_band}
                stats["t90"] += 1
            if g.get("t50") is not None:
                params["t50"] = {"v": g["t50"], "err": g.get("t50_error"), "band": dur_band}
                stats["t50"] += 1
            # fluence（bcat，10-1000 keV 逐行能段）
            if g.get("fluence") is not None:
                params["fluence"] = {"v": g["fluence"], "err": g.get("fluence_error"),
                                     "band": flu_band}
                stats["fluence"] += 1
            # peak_flux：64ms，10-1000 keV
            if g.get("flux_64") is not None:
                params["peak_flux"] = {"v": g["flux_64"], "err": g.get("flux_64_error"),
                                       "band": flu_band, "dt": "64ms"}
                stats["peak_flux"] += 1

            # epeak：按 flnc_best_fitting_model 选 band/comp；否则 band 优先、comp 兜底
            best = r["flnc_best_fitting_model"].strip()
            epeak_src = None
            if best in ("flnc_band", "flnc_comp") and g.get(best + "_epeak") is not None:
                epeak_src = best
            elif g.get("flnc_band_epeak") is not None:
                epeak_src = "flnc_band"
            elif g.get("flnc_comp_epeak") is not None:
                epeak_src = "flnc_comp"
            if epeak_src:
                err, fixed = asym_err(g.get(epeak_src + "_epeak_pos_err"),
                                      g.get(epeak_src + "_epeak_neg_err"))
                ep = {"v": g[epeak_src + "_epeak"], "err": err,
                      "model": MODEL_MAP[epeak_src], "frame": "obs"}
                if fixed:
                    ep["fixed"] = True
                    stats["epeak_fixed"] += 1
                params["epeak"] = ep
                stats["epeak"] += 1

            # other：目录特有的重要原始列（原样键名）
            other = {}
            for k in ("error_radius", "lii", "bii", "t50_start", "t90_start",
                      "fluence_batse", "fluence_batse_error",
                      "flux_256", "flux_256_error", "flux_1024", "flux_1024_error",
                      "flux_batse_64", "flux_batse_64_error",
                      "flux_batse_256", "flux_batse_256_error",
                      "flux_batse_1024", "flux_batse_1024_error",
                      "flnc_best_fitting_model",
                      "flnc_band_epeak", "flnc_band_epeak_pos_err", "flnc_band_epeak_neg_err",
                      "flnc_comp_epeak", "flnc_comp_epeak_pos_err", "flnc_comp_epeak_neg_err"):
                v = r.get(k, "").strip()
                if v == "":
                    continue
                fv = to_float(v)
                other[k] = fv if fv is not None else v

            rec = {
                "cat": "fermi_gbm",
                "name": name,
                "name_alt": name_alt,
                "trigger_time": mjd_to_iso(g.get("trigger_time")),
                "ra": g.get("ra"),
                "dec": g.get("dec"),
                "params": params,
                "other": other,
            }
            fo.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n_out += 1

    print("输出 %d 行 -> %s" % (n_out, OUT))
    print("统计: %s" % json.dumps(stats))


if __name__ == "__main__":
    main()
