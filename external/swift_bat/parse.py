#!/usr/bin/env python
"""Parse the Swift/BAT GRB catalog (swift_bat) into normalized.jsonl.

Input tables (all pipe-separated ASCII, '#' comment headers):
  - summary_general_info/summary_general.txt      : main table, T90/T50 (15-350 keV)
  - summary_T100/best_model.txt                   : best-fit model PL/CPL/N/A (T100 interval)
  - summary_T100/summary_cutpow_parameters.txt    : CPL fit params (Epeak, alpha; 90% CL)
  - summary_T100/summary_pow_parameters.txt       : PL fit params (alpha; 90% CL)
  - summary_T100/summary_{pow,cutpow}_energy_fluence.txt : fluence in 7 bands (90% CL)
  - summary_general_info/GRBlist_redshift_BAT.txt : redshift list

Decisions (see README.md pitfalls):
  * Missing-value token is the string 'N/A'; '-inf'/'inf' also treated as missing.
  * All spectral-fit _low/_hi columns are 90% confidence *bounds*; stored as
    err=[hi-v, v-low] with cl:90.
  * Epeak only emitted when best_model == 'CPL' and Epeak < 9990 keV
    (Epeak ~9999-10000 or low/hi==0 means unconstrained at the boundary).
  * fluence/alpha are taken from the table matching best_model
    (CPL -> cutpow, PL -> pow); when best_model is N/A the pow table is used
    as fallback (a PL fit exists for nearly all bursts). The source model is
    recorded in other['fluence_model'].
  * fluence value == 1.0 is an XSPEC log10(flux)=0.0 placeholder -> missing.
  * 15-150 keV fluence goes to params['fluence']; the other 6 bands are kept
    in `other` under their original column names (raw strings).
  * Join key is GRBname (Trig_ID can be N/A, e.g. GRB 041219A).
  * Base table is summary_general.txt (1668 rows); redshift rows not in the
    main table are ignored.
"""

import json
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

MISSING = {"", "N/A", "n/a", "NaN", "nan", "inf", "-inf", "Inf", "-Inf"}

FLUENCE_BANDS = ["15_25kev", "25_50kev", "50_100kev", "100_150kev",
                 "100_350kev", "15_150kev", "15_350kev"]


def read_table(relpath):
    """Return list of rows; each row is a list of stripped fields."""
    rows = []
    with open(os.path.join(HERE, relpath)) as f:
        for line in f:
            line = line.rstrip("\n")
            if line.lstrip().startswith("#") or not line.strip():
                continue
            fields = [c.strip() for c in line.split("|")]
            while fields and fields[-1] == "":
                fields.pop()
            rows.append(fields)
    return rows


def fnum(s):
    """Parse float; missing tokens -> None."""
    if s is None:
        return None
    s = s.strip()
    if s in MISSING:
        return None
    try:
        v = float(s)
    except ValueError:
        return None
    if not math.isfinite(v):
        return None
    return v


def err_bounds(v, low, hi):
    """90% bounds -> [pos, neg] = [hi-v, v-low]; 0/None bound -> None."""
    if v is None or low is None or hi is None:
        return None
    if low == 0.0 or hi == 0.0:
        return None
    return [hi - v, v - low]


def norm_name(raw):
    """'GRB250605A' -> 'GRB 250605A'; split entries like 'GRB140716A-1'
    normalize to 'GRB 140716A' (raw name kept in name_alt by caller)."""
    m = re.match(r"GRB\s?(\d{6})([A-Za-z]?)(-\d+)?$", raw.strip())
    if m:
        return "GRB " + m.group(1) + m.group(2).upper()
    return None


def main():
    general = read_table("summary_general_info/summary_general.txt")
    best_model = {r[0]: r[2] for r in read_table("summary_T100/best_model.txt")}
    # dedupe: cutpow params has 2 identical duplicated rows (GRB171020A/GRB171027A)
    cpl_rows = read_table("summary_T100/summary_cutpow_parameters.txt")
    cpl = {}
    for r in cpl_rows:
        cpl.setdefault(r[0], r)
    pl = {r[0]: r for r in read_table("summary_T100/summary_pow_parameters.txt")}
    fl_pow = {r[0]: r for r in read_table("summary_T100/summary_pow_energy_fluence.txt")}
    fl_cpl = {r[0]: r for r in read_table("summary_T100/summary_cutpow_energy_fluence.txt")}
    zrows = {r[0]: r for r in read_table("summary_general_info/GRBlist_redshift_BAT.txt")}

    out = []
    for g in general:
        raw_name = g[0]
        name = norm_name(raw_name)
        trig_id = g[1] if g[1] not in MISSING else None
        utc = g[3] if g[3] not in MISSING else None

        rec = {"cat": "swift_bat", "name": name, "name_alt": [],
               "trigger_time": (utc + "Z") if utc else None,
               "ra": fnum(g[4]), "dec": fnum(g[5]),
               "params": {}, "other": {}}
        if trig_id:
            rec["name_alt"].append("BAT " + trig_id)
        if raw_name.replace(" ", "") != (name or "").replace(" ", ""):
            rec["name_alt"].append(raw_name)  # e.g. GRB140716A-1 split entry

        # --- T90 / T50 (15-350 keV mask-weighted light curve) ---
        t90, t90e = fnum(g[8]), fnum(g[9])
        if t90 is not None:
            rec["params"]["t90"] = {"v": t90, "err": t90e, "band": "15-350 keV"}
        t50, t50e = fnum(g[10]), fnum(g[11])
        if t50 is not None:
            rec["params"]["t50"] = {"v": t50, "err": t50e, "band": "15-350 keV"}

        # --- spectral params (T100 interval) ---
        bm = best_model.get(raw_name, "N/A")
        if bm not in MISSING:
            rec["other"]["T100_best_model"] = bm
        use_cpl = bm == "CPL"
        spec = cpl.get(raw_name) if use_cpl else pl.get(raw_name)
        if spec is not None:
            alpha, alo, ahi = fnum(spec[2]), fnum(spec[3]), fnum(spec[4])
            if alpha is not None:
                rec["params"]["alpha"] = {"v": alpha,
                                          "err": err_bounds(alpha, alo, ahi),
                                          "cl": 90}
        if use_cpl and spec is not None:
            ep, eplo, ephi = fnum(spec[5]), fnum(spec[6]), fnum(spec[7])
            if ep is not None and ep < 9990.0:  # boundary ~9999-10000 = unconstrained
                rec["params"]["epeak"] = {"v": ep,
                                          "err": err_bounds(ep, eplo, ephi),
                                          "model": "CPL", "frame": "obs", "cl": 90}

        # --- fluence (7 bands; main = 15-150 keV) ---
        fl = fl_cpl.get(raw_name) if use_cpl else fl_pow.get(raw_name)
        fl_model = "CPL" if use_cpl else "PL"
        if fl is None and not use_cpl:
            fl = fl_cpl.get(raw_name)
            fl_model = "CPL"
        if fl is not None:
            rec["other"]["fluence_model"] = fl_model
            for i, band in enumerate(FLUENCE_BANDS):
                v = fnum(fl[2 + 3 * i])
                lo = fnum(fl[3 + 3 * i])
                hi = fnum(fl[4 + 3 * i])
                if v is not None and v == 1.0:  # log10(flux)=0 placeholder
                    v = None
                if band == "15_150kev":
                    if v is not None:
                        rec["params"]["fluence"] = {
                            "v": v, "err": err_bounds(v, lo, hi),
                            "band": "15-150 keV", "cl": 90}
                else:
                    for suffix, val in (("", v), ("_low", lo), ("_hi", hi)):
                        if val is not None:
                            rec["other"][band + suffix] = val

        # --- redshift ---
        zr = zrows.get(raw_name)
        if zr is not None:
            z = fnum(zr[1])
            if z is not None:
                rec["params"]["redshift"] = {"v": z}
            if len(zr) > 2 and zr[2] not in MISSING:
                rec["other"]["z_method"] = zr[2]
            if len(zr) > 3 and zr[3] not in MISSING:
                rec["other"]["z_uncertainty"] = zr[3]
            if len(zr) > 4 and zr[4] not in MISSING:
                rec["other"]["z_ref"] = zr[4]

        # --- a few important raw columns from the main table ---
        for idx, col in ((6, "Image_position_err"), (7, "Image_SNR"),
                         (14, "pcode"), (15, "Trigger_method")):
            if g[idx] not in MISSING:
                rec["other"][col] = g[idx]

        out.append(rec)

    with open(os.path.join(HERE, "normalized.jsonl"), "w") as f:
        for rec in out:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # summary stats
    n = len(out)
    stats = {"rows": n}
    for k in ("t90", "t50", "epeak", "fluence", "alpha", "redshift"):
        stats[k] = sum(1 for r in out if k in r["params"])
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
