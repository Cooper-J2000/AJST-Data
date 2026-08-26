#!/usr/bin/env python
"""Parse HEASARC BeppoSAX/GRBM GRB catalog (saxgrbmgrb) into normalized.jsonl.

Input (same directory):
  heasarc_saxgrbmgrb.tdat.gz   - GRBM GRB catalog, 1082 rows, pipe-separated tdat

Output: normalized.jsonl, one record per GRBM burst (1082 lines).

Notes:
  - The catalog's peak_flux is an *energy* flux (erg/cm^2/s, 40-700 keV),
    NOT a photon flux, so it is kept in `other` (SCHEMA's params.peak_flux
    is photon flux) to avoid unit confusion.
  - Missing values are empty strings; such keys are omitted (SCHEMA rule 1).

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
TDAT = os.path.join(HERE, "heasarc_saxgrbmgrb.tdat.gz")
OUT_JSONL = os.path.join(HERE, "normalized.jsonl")

COLS = [
    "name", "ra", "dec", "lii", "bii", "error_radius",
    "earth_limb_elevation", "ref_position", "time", "high_res_flag",
    "t_other", "t_other_error", "t_above_fraction", "t_above_fraction_error",
    "t_above_num_intervals", "t90", "t90_error", "fluence", "fluence_error",
    "peak_flux", "peak_flux_error", "photon_index", "photon_index_error",
    "detection_unit_1", "detection_unit_2", "detection_unit_3",
    "rebinning_factor",
]

BAND = "40-700 keV"  # GRBM band; durations, fluence, peak flux all use it

NAME_RE = re.compile(r"^GRB (\d{6})([A-Z]?)$")


def read_tdat(path):
    rows = []
    with gzip.open(path, "rt") as f:
        for line in f:
            if not line.startswith("GRB"):
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
    v = fnum(mjd_str)
    if v is None:
        return None
    return Time(v, format="mjd", scale="utc").isot + "Z"


def main():
    rows = read_tdat(TDAT)

    seen = set()
    n_name_date_mismatch = 0
    out = []
    for r in rows:
        raw_name = r["name"].strip()
        m = NAME_RE.match(raw_name)
        name = raw_name if m else None
        if raw_name in seen:
            raise ValueError(f"duplicate name {raw_name}")
        seen.add(raw_name)

        trigger_time = mjd_to_iso(r["time"])

        # sanity: name date should match trigger date
        if name is not None and trigger_time is not None:
            yy, mm, dd = name[4:6], name[6:8], name[8:10]
            yyyy = ("19" if int(yy) >= 91 else "20") + yy
            if trigger_time[:10] != f"{yyyy}-{mm}-{dd}":
                n_name_date_mismatch += 1
                print(f"WARN date mismatch {raw_name} vs {trigger_time}", file=sys.stderr)

        params = {}
        t90, t90e = fnum(r["t90"]), fnum(r["t90_error"])
        if t90 is not None:
            params["t90"] = {"v": t90, "err": t90e, "band": BAND}
        flu, flue = fnum(r["fluence"]), fnum(r["fluence_error"])
        if flu is not None:
            params["fluence"] = {"v": flu, "err": flue, "band": BAND}
        # power-law photon index fitted to 2-channel (40-700 keV, >100 keV) data
        gi, gie = fnum(r["photon_index"]), fnum(r["photon_index_error"])
        if gi is not None:
            params["spectral_index"] = {"v": gi, "err": gie, "model": "PL"}

        other = {}
        for k in ("lii", "bii", "error_radius", "earth_limb_elevation",
                  "t_other", "t_other_error", "t_above_fraction",
                  "t_above_fraction_error", "peak_flux", "peak_flux_error"):
            v = fnum(r[k])
            if v is not None:
                other[k] = v
        for k in ("t_above_num_intervals", "detection_unit_1", "detection_unit_2",
                  "detection_unit_3", "rebinning_factor"):
            v = fnum(r[k])
            if v is not None:
                other[k] = int(v)
        for k in ("ref_position", "high_res_flag"):
            if r[k].strip():
                other[k] = r[k].strip()

        rec = {
            "cat": "saxgrbmgrb",
            "name": name,
            "name_alt": [] if name == raw_name else [raw_name],
            "trigger_time": trigger_time,
            "ra": fnum(r["ra"]),
            "dec": fnum(r["dec"]),
            "params": params,
            "other": other,
        }
        out.append(rec)

    out.sort(key=lambda x: (x["trigger_time"] or "", x["name"] or ""))
    with open(OUT_JSONL, "w") as f:
        for rec in out:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    def cnt(key):
        return sum(1 for rec in out if key in rec["params"])

    print(f"wrote {len(out)} records -> {OUT_JSONL}")
    print(f"name resolved: {sum(1 for r in out if r['name'])}; "
          f"name null: {sum(1 for r in out if r['name'] is None)}")
    print(f"name/trigger date mismatches: {n_name_date_mismatch}")
    print(f"trigger_time: {sum(1 for r in out if r['trigger_time'])}  "
          f"ra/dec: {sum(1 for r in out if r['ra'] is not None)}")
    print(f"t90: {cnt('t90')}  fluence: {cnt('fluence')}  "
          f"spectral_index: {cnt('spectral_index')}")
    print(f"peak_flux (energy, in other): "
          f"{sum(1 for r in out if 'peak_flux' in r['other'])}")


if __name__ == "__main__":
    main()
