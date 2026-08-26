#!/usr/bin/env python
"""Parse HEASARC SWIFTGRB tdat dump -> normalized.jsonl (schema: ../SCHEMA.md).

Input : heasarc_swiftgrb.tdat.gz  (pipe-delimited, empty string = missing)
Output: normalized.jsonl        (one JSON record per GRB, 872 expected)

Notes specific to this catalog (see README.md):
- BAT band is 15-150 keV for t90/t50/fluence/peak flux.
- bat_epeak is observer-frame keV; catalog gives no error and no model column
  (model -> null).
- bat_eiso / bat_eiso1000 are rest-frame energies in erg (header wrongly says
  erg/s). Kept as params.eiso (15-150 keV) and params.eiso_1000 (1-1000 keV).
- fluence / peak flux with empty error column = upper limit (err -> null).
- `redshift` column (optical, 338 rows) -> params.redshift; `bat_redshift`
  (redshift used for Eiso) is preserved in `other`.
"""
import gzip
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "heasarc_swiftgrb.tdat.gz")
OUT = os.path.join(HERE, "normalized.jsonl")

BAT_BAND = "15-150 keV"


def fnum(s):
    """Parse a float; missing markers -> None."""
    if s is None:
        return None
    s = s.strip()
    if s == "" or s.upper() in ("N/A", "NULL", "NONE"):
        return None
    try:
        v = float(s)
    except ValueError:
        return None
    if v in (-99.0, -99.99):  # defensive: common HEASARC sentinels
        return None
    return v


def txt(s):
    s = (s or "").strip()
    return s if s else None


def iso_utc(s):
    """'2004-12-17T07:28:25.920000' -> '2004-12-17T07:28:25.920000Z'."""
    s = txt(s)
    if s is None:
        return None
    s = s.replace(" ", "T")
    if not s.endswith("Z"):
        s += "Z"
    return s


def main():
    cols = None
    rows = []
    with gzip.open(SRC, "rt") as f:
        for line in f:
            if line.startswith("line[1] ="):
                cols = line.split("=", 1)[1].split()
            elif line.startswith("GRB"):
                vals = line.rstrip("\n").split("|")
                if vals and vals[-1] == "":
                    vals = vals[:-1]  # trailing empty field after last '|'
                assert cols is not None
                if len(vals) != len(cols):
                    raise ValueError(
                        f"column count mismatch: {len(vals)} vs {len(cols)}: {line[:80]}"
                    )
                rows.append(dict(zip(cols, vals)))

    n_out = 0
    with open(OUT, "w") as fo:
        for r in rows:
            name = txt(r.get("name"))
            rec = {
                "cat": "swift_grb",
                "name": name,
                "name_alt": [],
                "trigger_time": iso_utc(r.get("trigger_time")),
                "ra": fnum(r.get("ra")),
                "dec": fnum(r.get("dec")),
                "params": {},
                "other": {},
            }
            tid = txt(r.get("target_id"))
            oid = txt(r.get("other_id"))
            if tid:
                rec["name_alt"].append(f"Swift {tid}")
            if oid:
                rec["name_alt"].append(oid)

            p = rec["params"]

            v = fnum(r.get("bat_t90"))
            if v is not None:
                p["t90"] = {"v": v, "err": fnum(r.get("bat_t90_err")), "band": BAT_BAND}
            v = fnum(r.get("bat_t50"))
            if v is not None:
                p["t50"] = {"v": v, "err": fnum(r.get("bat_t50_err")), "band": BAT_BAND}

            v = fnum(r.get("bat_epeak"))
            if v is not None:
                # no error / model columns in this catalog
                p["epeak"] = {"v": v, "err": None, "model": None, "frame": "obs"}

            v = fnum(r.get("bat_fluence"))
            if v is not None:
                # empty error => upper limit (catalog convention)
                p["fluence"] = {
                    "v": v,
                    "err": fnum(r.get("bat_fluence_err")),
                    "band": BAT_BAND,
                }

            v = fnum(r.get("bat_peakfluxp"))
            if v is not None:
                p["peak_flux"] = {
                    "v": v,
                    "err": fnum(r.get("bat_peakfluxp_err")),
                    "band": BAT_BAND,
                    "dt": "1s",
                }

            v = fnum(r.get("bat_eiso"))
            if v is not None:
                p["eiso"] = {"v": v, "err": None, "band": BAT_BAND, "frame": "rest"}
            v = fnum(r.get("bat_eiso1000"))
            if v is not None:
                p["eiso_1000"] = {
                    "v": v,
                    "err": None,
                    "band": "1-1000 keV",
                    "frame": "rest",
                }

            v = fnum(r.get("redshift"))
            if v is not None:
                p["redshift"] = {"v": v, "err": fnum(r.get("redshift_err"))}

            # catalog-specific raw columns worth keeping (original names)
            for k in (
                "target_id", "other_id", "det_flag", "bat_detection",
                "bat_fluence_model", "bat_peak_model",
                "bat_epeak_ref", "bat_eiso_alpha", "bat_eiso_beta",
                "bat_eiso_norm", "bat_eiso_dur", "bat_eiso_ref",
                "bat_redshift", "bat_plsl", "bat_plsl_err",
                "redshift_type", "redshift_ref", "supernova_flag",
            ):
                val = txt(r.get(k))
                if val is not None:
                    rec["other"][k] = val

            fo.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n_out += 1

    print(f"rows read: {len(rows)}, written: {n_out} -> {OUT}")


if __name__ == "__main__":
    main()
