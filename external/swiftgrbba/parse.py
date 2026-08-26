#!/usr/bin/env python
"""Parse HEASARC Swift GRB Burst Advocate compilation (swiftgrbba) into normalized.jsonl.

Input (same directory):
  heasarc_swiftgrbba.tdat.gz  - 2036 rows, pipe-separated tdat, 49 columns

Output: normalized.jsonl, one record per GRB (2036 lines).

Key quirks handled here (see README.md for full documentation):
  - the `trigger_time` column is time-of-day only; full UTC timestamp is
    rebuilt from the MJD column `time`. 11 rows have an integer MJD (day
    precision only) -> trigger_time = None.
  - 362 rows carry the official suffix-less name "GRB yymmdd"; per SCHEMA
    rule 4 we do not invent a letter -> name = None, raw name in name_alt.
  - BAT errors are 90% confidence -> "cl": 90 on t90/fluence/peak_flux/
    spectral_index value objects.

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
TDAT = os.path.join(HERE, "heasarc_swiftgrbba.tdat.gz")
OUT_JSONL = os.path.join(HERE, "normalized.jsonl")

COLS = [
    "name", "trigger_time", "time", "trigger_obs", "target_id",
    "ra", "dec", "lii", "bii", "error_radius",
    "bat_t90", "bat_fluence", "bat_fluence_error",
    "bat_1s_peak_flux", "bat_1s_peak_flux_error",
    "bat_spectral_model", "bat_photon_index", "bat_photon_index_error",
    "xrt_ra", "xrt_dec", "xrt_error_radius", "xrt_first_obs", "xrt_early_flux",
    "xrt_11hr_flux", "xrt_24hr_flux", "xrt_lc_index", "xrt_gamma", "xrt_nh",
    "uvot_ra", "uvot_dec", "uvot_error_radius", "uvot_first_obs",
    "uvot_vmag_flag", "uvot_vmag", "uvot_mag",
    "other_obs", "redshift", "redshift_comment", "other_redshift",
    "host_galaxy", "comment",
    "ref_bat", "ref_xrt", "ref_uvot", "ref_radio", "ref_redshift",
    "ref_host", "ref_other", "advocate",
]

BAT_BAND = "15-150 keV"


def read_tdat(path):
    rows = []
    with gzip.open(path, "rt") as f:
        for line in f:
            if not line.startswith("GRB "):
                continue  # skips <HEADER> block and <END>
            fields = line.rstrip("\n").split("|")
            if fields and fields[-1] == "":
                fields = fields[:-1]  # trailing pipe
            if len(fields) != len(COLS):
                raise ValueError(f"{path}: {len(fields)} fields, expected {len(COLS)}: {line!r}")
            rows.append(dict(zip(COLS, fields)))
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
    """Full ISO timestamp from MJD; None when only day precision (integer MJD)."""
    if mjd_str is None:
        return None
    s = mjd_str.strip()
    if s == "" or "." not in s:
        return None  # integer MJD: time-of-day unknown (11 rows)
    v = fnum(s)
    if v is None:
        return None
    return Time(v, format="mjd", scale="utc").isot + "Z"


def normalize_name(raw):
    """Return (standard_name, orig_name).

    'GRB yymmddX' -> as-is; 'GRB yymmdd' (official suffix-less designation,
    362 rows) -> None, per SCHEMA rule 4 (letter suffix undetermined).
    """
    raw = raw.strip()
    m = re.match(r"^GRB\s+(\d{6})([A-Z])$", raw)
    if m:
        return "GRB " + m.group(1) + m.group(2), raw
    return None, raw


def main():
    rows = read_tdat(TDAT)

    names = set()
    for r in rows:
        n = r["name"].strip()
        if n in names:
            raise ValueError(f"duplicate name {n}")
        names.add(n)

    n_name_date_mismatch = 0
    out = []
    for r in rows:
        name, orig_name = normalize_name(r["name"])
        trigger_time = mjd_to_iso(r["time"])

        # sanity: name date should match trigger date (Swift era -> 20xx)
        if name is not None and trigger_time is not None:
            yy, mm, dd = name[4:6], name[6:8], name[8:10]
            if trigger_time[:10] != f"20{yy}-{mm}-{dd}":
                n_name_date_mismatch += 1
                print(f"WARN date mismatch {orig_name}: vs {trigger_time}",
                      file=sys.stderr)

        # coordinates: prefer BAT, fall back to XRT, then UVOT
        ra, dec = fnum(r["ra"]), fnum(r["dec"])
        if ra is None or dec is None:
            ra, dec = fnum(r["xrt_ra"]), fnum(r["xrt_dec"])
        if ra is None or dec is None:
            ra, dec = fnum(r["uvot_ra"]), fnum(r["uvot_dec"])

        params = {}

        t90 = fnum(r["bat_t90"])
        if t90 is not None:
            params["t90"] = {"v": t90, "err": None, "band": BAT_BAND}

        fl, fle = fnum(r["bat_fluence"]), fnum(r["bat_fluence_error"])
        if fl is not None:
            params["fluence"] = {"v": fl, "err": fle, "band": BAT_BAND, "cl": 90}

        pf, pfe = fnum(r["bat_1s_peak_flux"]), fnum(r["bat_1s_peak_flux_error"])
        if pf is not None:
            params["peak_flux"] = {"v": pf, "err": pfe, "band": BAT_BAND,
                                   "dt": "1s", "cl": 90}

        gi, gie = fnum(r["bat_photon_index"]), fnum(r["bat_photon_index_error"])
        if gi is not None:
            params["spectral_index"] = {"v": gi, "err": gie, "cl": 90}

        z = fnum(r["redshift"])
        if z is not None:
            params["redshift"] = {"v": z}

        other = {}
        for k in ("trigger_obs", "bat_spectral_model", "uvot_mag", "other_obs",
                  "redshift_comment", "other_redshift", "host_galaxy",
                  "comment", "ref_bat", "ref_xrt", "ref_uvot", "ref_radio",
                  "ref_redshift", "ref_host", "ref_other", "advocate"):
            if r[k].strip():
                other[k] = r[k].strip()
        tid = fnum(r["target_id"])
        if tid is not None:
            other["target_id"] = int(tid)
        for k in ("error_radius", "xrt_ra", "xrt_dec", "xrt_error_radius",
                  "xrt_first_obs", "xrt_early_flux", "xrt_11hr_flux",
                  "xrt_24hr_flux", "xrt_lc_index", "xrt_gamma", "xrt_nh",
                  "uvot_ra", "uvot_dec", "uvot_error_radius", "uvot_first_obs",
                  "uvot_vmag"):
            v = fnum(r[k])
            if v is not None:
                other[k] = v
        vflag = fnum(r["uvot_vmag_flag"])
        if vflag is not None:
            other["uvot_vmag_flag"] = int(vflag)

        name_alt = []
        if orig_name and orig_name != name:
            name_alt.append(orig_name)

        rec = {
            "cat": "swiftgrbba",
            "name": name,
            "name_alt": name_alt,
            "trigger_time": trigger_time,
            "ra": ra,
            "dec": dec,
            "params": params,
            "other": other,
        }
        out.append(rec)

    out.sort(key=lambda x: (x["trigger_time"] is None, x["trigger_time"] or "",
                            x["name"] or ""))
    with open(OUT_JSONL, "w") as f:
        for rec in out:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # ---- summary ----
    def cnt(key):
        return sum(1 for rec in out if key in rec["params"])

    print(f"wrote {len(out)} records -> {OUT_JSONL}")
    print(f"name resolved: {sum(1 for r in out if r['name'])}; "
          f"name null (official suffix-less name): {sum(1 for r in out if r['name'] is None)}")
    print(f"trigger_time present: {sum(1 for r in out if r['trigger_time'])}; "
          f"null (day-precision MJD): {sum(1 for r in out if r['trigger_time'] is None)}")
    print(f"ra/dec present: {sum(1 for r in out if r['ra'] is not None)}")
    print(f"name/trigger date mismatches: {n_name_date_mismatch}")
    print(f"t90: {cnt('t90')}  fluence: {cnt('fluence')}  "
          f"peak_flux: {cnt('peak_flux')}  spectral_index: {cnt('spectral_index')}  "
          f"redshift: {cnt('redshift')}")
    print(f"epeak: {cnt('epeak')} (table has no Epeak column)  "
          f"eiso: {cnt('eiso')}")


if __name__ == "__main__":
    main()
