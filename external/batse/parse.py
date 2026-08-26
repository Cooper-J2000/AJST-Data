#!/usr/bin/env python
"""Parse HEASARC BATSE GRB catalog (batsegrb + batsegrbsp) into normalized.jsonl.

Input (same directory):
  heasarc_batsegrb.tdat.gz   - main catalog, 2702 rows, pipe-separated tdat
  heasarc_batsegrbsp.tdat.gz - bright-burst spectral catalog, 350 rows (Epeak)

Output: normalized.jsonl, one record per BATSE trigger (2702 lines).

See README.md in this directory for the per-column documentation and
SCHEMA.md in the parent directory for the output contract.
"""
import gzip
import json
import os
import re
import sys

from astropy.time import Time

HERE = os.path.dirname(os.path.abspath(__file__))
MAIN_TDAT = os.path.join(HERE, "heasarc_batsegrb.tdat.gz")
SPEC_TDAT = os.path.join(HERE, "heasarc_batsegrbsp.tdat.gz")
OUT_JSONL = os.path.join(HERE, "normalized.jsonl")

MAIN_COLS = [
    "trigger_num", "name", "ra", "dec", "lii", "bii", "day_trigger", "time",
    "seconds_trigger", "error_radius", "earth_angle", "overwrite", "overwritten",
    "max_cts_64", "threshold_64", "flux_64", "flux_64_error", "flux_64_time",
    "max_cts_256", "threshold_256", "flux_256", "flux_256_error", "flux_256_time",
    "max_cts_1024", "threshold_1024", "flux_1024", "flux_1024_error", "flux_1024_time",
    "t50", "t50_error", "t50_start", "t90", "t90_error", "t90_start",
    "fluence_1", "fluence_1_error", "fluence_2", "fluence_2_error",
    "fluence_3", "fluence_3_error", "fluence_4", "fluence_4_error",
    "comments_quality", "comments_otherobs", "comments_general",
    "comments_position", "comments_duration",
]

SPEC_COLS = [
    "trigger_num", "name", "grb_flag", "ra", "dec", "lii", "bii",
    "error_radius", "time", "seconds_trigger", "lad_data_type", "lad_number",
    "start_spectrum", "end_spectrum", "lower_energy", "upper_energy",
    "num_spectra", "spectral_model", "amplitude", "amplitude_error",
    "peak_energy", "peak_energy_error", "low_pl_index", "low_pl_index_error",
    "high_pl_index", "high_pl_index_error", "break_energy", "break_energy_error",
    "sbpl_break_scale", "chi_squared", "fit_dof",
]

# T50/T90 are computed from the summed counts of the four LAD discriminator
# channels (i.e. roughly the full LAD range >20 keV), not only 50-300 keV.
DURATION_BAND = ">20 keV (sum of 4 LAD channels)"
FLUX_BAND = "50-300 keV"
FLUENCE_BANDS = {
    "fluence_1": "20-50 keV",
    "fluence_2": "50-100 keV",
    "fluence_3": "100-300 keV",
    "fluence_4": ">300 keV",
}

MODEL_MAP = {"BAND": "BAND", "SBPL": "SBPL", "COMP": "COMP", "PWRL": "PL"}


def read_tdat(path, cols):
    rows = []
    with gzip.open(path, "rt") as f:
        for line in f:
            if not line or not line[0].isdigit():
                continue  # skips <HEADER> block and <END>
            fields = line.rstrip("\n").split("|")
            if fields and fields[-1] == "":
                fields = fields[:-1]  # trailing pipe
            if len(fields) != len(cols):
                raise ValueError(f"{path}: {len(fields)} fields, expected {len(cols)}: {line!r}")
            rows.append(dict(zip(cols, fields)))
    return rows


def fnum(s):
    """Parse float; empty/unparseable -> None."""
    if s is None:
        return None
    s = s.strip()
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def mjd_to_iso(mjd_str):
    v = fnum(mjd_str)
    if v is None:
        return None
    return Time(v, format="mjd", scale="utc").isot + "Z"


def normalize_name(raw):
    """Return (standard_name, orig_name).

    '4B yymmddX' / 'GRB yymmddX' -> 'GRB yymmddX'; a trailing '-' means the
    same-day sequence letter was never assigned, so the standardized name is
    undetermined -> None (SCHEMA rule 4).
    """
    raw = raw.strip()
    m = re.match(r"^(?:4B|GRB)\s+(\d{6})([A-Za-z]?)(-?)$", raw)
    if not m:
        return None, raw
    date, letter, dash = m.groups()
    if dash:
        return None, raw
    return "GRB " + date + letter, raw


def main():
    main_rows = read_tdat(MAIN_TDAT, MAIN_COLS)
    spec_rows = read_tdat(SPEC_TDAT, SPEC_COLS)

    spec_by_trig = {}
    for r in spec_rows:
        trig = int(r["trigger_num"])
        if trig in spec_by_trig:
            raise ValueError(f"duplicate trigger_num {trig} in spectral table")
        spec_by_trig[trig] = r

    main_trigs = set()
    for r in main_rows:
        t = int(r["trigger_num"])
        if t in main_trigs:
            raise ValueError(f"duplicate trigger_num {t} in main table")
        main_trigs.add(t)
    missing = [t for t in spec_by_trig if t not in main_trigs]
    if missing:
        raise ValueError(f"spectral trigger_nums missing from main table: {missing}")

    n_name_date_mismatch = 0
    out = []
    for r in main_rows:
        trig = int(r["trigger_num"])
        name, orig_name = normalize_name(r["name"])
        trigger_time = mjd_to_iso(r["time"])

        # sanity: name date should match trigger date
        if name is not None and trigger_time is not None:
            yy, mm, dd = name[4:6], name[6:8], name[8:10]
            yyyy = ("19" if int(yy) >= 91 else "20") + yy
            if trigger_time[:10] != f"{yyyy}-{mm}-{dd}":
                n_name_date_mismatch += 1
                print(f"WARN date mismatch trig {trig}: name {name} vs {trigger_time}",
                      file=sys.stderr)

        name_alt = [f"BATSE {trig}"]
        if orig_name and orig_name != name:
            name_alt.append(orig_name)

        params = {}

        t90, t90e = fnum(r["t90"]), fnum(r["t90_error"])
        if t90 is not None:
            params["t90"] = {"v": t90, "err": t90e, "band": DURATION_BAND}
        t50, t50e = fnum(r["t50"]), fnum(r["t50_error"])
        if t50 is not None:
            params["t50"] = {"v": t50, "err": t50e, "band": DURATION_BAND}

        for ch, band in FLUENCE_BANDS.items():
            v, e = fnum(r[ch]), fnum(r[ch + "_error"])
            if v is not None:
                params[ch] = {"v": v, "err": e, "band": band}

        for ms in ("64", "256", "1024"):
            v, e = fnum(r[f"flux_{ms}"]), fnum(r[f"flux_{ms}_error"])
            if v is not None:
                params[f"peak_flux_{ms}ms"] = {
                    "v": v, "err": e, "band": FLUX_BAND,
                    "dt": {"64": "64ms", "256": "256ms", "1024": "1024ms"}[ms],
                }

        other = {}
        for k in ("error_radius", "earth_angle"):
            v = fnum(r[k])
            if v is not None:
                other[k] = v
        for k in ("overwrite", "overwritten"):
            if r[k].strip():
                other[k] = r[k].strip()
        for k in ("comments_quality", "comments_otherobs", "comments_general",
                  "comments_position", "comments_duration"):
            if r[k].strip():
                other[k] = r[k].strip()

        sp = spec_by_trig.get(trig)
        if sp is not None:
            sp_name = sp["name"].strip()
            if sp_name and sp_name != name and sp_name not in name_alt:
                name_alt.append(sp_name)
            model_raw = sp["spectral_model"].strip()
            model = MODEL_MAP.get(model_raw)
            ep, epe = fnum(sp["peak_energy"]), fnum(sp["peak_energy_error"])
            if ep is not None:
                params["epeak"] = {"v": ep, "err": epe, "model": model, "frame": "obs"}
            lo, loe = fnum(sp["low_pl_index"]), fnum(sp["low_pl_index_error"])
            if lo is not None:
                key = "spectral_index" if model_raw == "PWRL" else "alpha"
                params[key] = {"v": lo, "err": loe}
            hi, hie = fnum(sp["high_pl_index"]), fnum(sp["high_pl_index_error"])
            if hi is not None:
                params["beta"] = {"v": hi, "err": hie}
            # catalog-specific spectral fit extras, kept raw
            for k in ("spectral_model", "grb_flag", "lad_data_type", "lad_number"):
                if sp[k].strip():
                    other[k] = sp[k].strip()
            for k in ("start_spectrum", "end_spectrum", "lower_energy",
                      "upper_energy", "amplitude", "amplitude_error",
                      "break_energy", "break_energy_error", "sbpl_break_scale",
                      "chi_squared", "fit_dof"):
                v = fnum(sp[k])
                if v is not None:
                    other[k] = v
            ns = fnum(sp["num_spectra"])
            if ns is not None:
                other["num_spectra"] = int(ns)

        rec = {
            "cat": "batse",
            "name": name,
            "name_alt": name_alt,
            "trigger_time": trigger_time,
            "ra": fnum(r["ra"]),
            "dec": fnum(r["dec"]),
            "params": params,
            "other": other,
        }
        out.append(rec)

    out.sort(key=lambda x: int(x["name_alt"][0].split()[1]))
    with open(OUT_JSONL, "w") as f:
        for rec in out:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # ---- summary ----
    def cnt(key):
        return sum(1 for rec in out if key in rec["params"])

    print(f"wrote {len(out)} records -> {OUT_JSONL}")
    print(f"name resolved: {sum(1 for r in out if r['name'])}; "
          f"name null (unresolved same-day letter etc.): {sum(1 for r in out if r['name'] is None)}")
    print(f"name/trigger date mismatches: {n_name_date_mismatch}")
    print(f"t90: {cnt('t90')}  t50: {cnt('t50')}")
    for ch in FLUENCE_BANDS:
        print(f"{ch}: {cnt(ch)}", end="  ")
    print()
    print(f"peak_flux_64ms: {cnt('peak_flux_64ms')}  "
          f"peak_flux_256ms: {cnt('peak_flux_256ms')}  "
          f"peak_flux_1024ms: {cnt('peak_flux_1024ms')}")
    print(f"epeak: {cnt('epeak')} (spectral table rows: {len(spec_rows)})  "
          f"alpha: {cnt('alpha')}  beta: {cnt('beta')}  "
          f"spectral_index: {cnt('spectral_index')}")
    print(f"eiso: {cnt('eiso')}  redshift: {cnt('redshift')}")


if __name__ == "__main__":
    main()
