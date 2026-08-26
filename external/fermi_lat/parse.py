#!/usr/bin/env python
"""Parse fermilgrb_w3browse_full.txt (HEASARC BatchDisplay ASCII, 231 rows x 107 cols)
into normalized.jsonl following catadata/external/SCHEMA.md.

Notes (see README.md):
- Missing markers: empty fields; 0 means missing/undetected for redshift, eiso,
  lle_t90, gbm_cat_t05/t90 and like_* fit results.
- W3Browse ASCII like_best_eiso_rf is ALREADY in erg (scale factor applied by
  HEASARC; FITS stores units of 1e52 erg). Verified against gll_2flgc_dr1.fits:
  GRB210826293 FITS 0.0053310185 x 1e52 = 5.33102e+49 == ASCII value.
- ra/dec are sexagesimal strings; time is UTC 'YYYY-MM-DD HH:MM:SS.mmm'.
"""
import json
import os
import re

from astropy.coordinates import Angle
import astropy.units as u

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "fermilgrb_w3browse_full.txt")
OUT = os.path.join(HERE, "normalized.jsonl")


def f(x, zero_missing=True):
    """Parse float; empty/unparseable -> None; 0 -> None when zero_missing."""
    x = x.strip()
    if not x:
        return None
    try:
        v = float(x)
    except ValueError:
        return None
    if zero_missing and v == 0.0:
        return None
    return v


def obj(v, err=None, **kw):
    """Build a param object, dropping it entirely when v is None."""
    if v is None:
        return None
    d = {"v": v, "err": err}
    d.update(kw)
    return d


def main():
    with open(SRC) as fh:
        lines = [l.rstrip("\n") for l in fh]

    header = [c.strip() for c in lines[1].split("|")]
    data = [l for l in lines if l.startswith("|GRB")]
    recs = []
    for line in data:
        cells = line.split("|")
        # cells[0] is '' (before leading '|'); align with header which also
        # starts with an empty first element
        row = dict(zip(header, cells))

        # --- name -------------------------------------------------------
        raw_name = row["name"].strip()               # GRByymmddfff
        ymd, frac = raw_name[3:9], raw_name[9:12]
        gcn = row["gcn_name"].strip()                # e.g. GRB140323A or ''
        name = None
        if gcn:
            m = re.match(r"GRB\s*(\d{6}[A-Za-z]?)$", gcn)
            name = "GRB " + m.group(1) if m else gcn
        name_alt = ["GRB %s.%s" % (ymd, frac)]
        gbm_name = row["gbm_cat_name"].strip()
        if gbm_name and gbm_name != raw_name:
            name_alt.append(gbm_name)

        # --- trigger time ------------------------------------------------
        t = row["time"].strip()
        trigger_time = t.replace(" ", "T") + "Z" if t else None

        # --- coordinates -------------------------------------------------
        ra_s, dec_s = row["ra"].strip(), row["dec"].strip()
        ra = float(Angle(ra_s.replace(" ", ":"), unit=u.hourangle).deg) if ra_s else None
        dec = float(Angle(dec_s.replace(" ", ":"), unit=u.deg).deg) if dec_s else None

        # --- params ------------------------------------------------------
        params = {}
        gbm_t90 = f(row["gbm_cat_t90"])
        gbm_t90e = f(row["gbm_cat_t90_error"], zero_missing=False)
        o = obj(gbm_t90, gbm_t90e, band="50-300 keV")
        if o:
            params["t90"] = o

        gbm_flu = f(row["gbm_cat_fluence"])
        gbm_flue = f(row["gbm_cat_fluence_error"], zero_missing=False)
        o = obj(gbm_flu, gbm_flue, band="10-1000 keV")
        if o:
            params["fluence"] = o

        eiso = f(row["like_best_eiso_rf"])           # already erg (see header)
        eisoe = f(row["like_best_eiso_rf_error"], zero_missing=False)
        o = obj(eiso, eisoe, band="100 MeV-10 GeV", frame="rest")
        if o:
            params["eiso"] = o

        z = f(row["redshift"])
        if z is not None:
            params["redshift"] = {"v": z}

        # --- other (catalog-specific, raw column names) -------------------
        other = {}
        other_src = [
            "trigger_met", "error_radius",
            "lle_t90", "tl100", "tl100_error",
            "like_best_ts", "like_best_grbindex", "like_best_grbindex_error",
            "like_best_fluence", "like_best_fluence_error",
            "ext_emission_max_ene", "ext_emission_max_ene_t",
        ]
        for c in other_src:
            v = f(row[c])
            if v is not None:
                other[c] = v

        rec = {
            "cat": "fermi_lat",
            "name": name,
            "name_alt": name_alt,
            "trigger_time": trigger_time,
            "ra": ra,
            "dec": dec,
            "params": params,
            "other": other,
        }
        recs.append(rec)

    with open(OUT, "w") as fh:
        for r in recs:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    # summary
    n = len(recs)
    cnt = lambda k: sum(1 for r in recs if k in r["params"])
    print("rows written:", n, "->", OUT)
    print("t90:", cnt("t90"), " fluence:", cnt("fluence"),
          " eiso:", cnt("eiso"), " redshift:", cnt("redshift"))
    print("lle_t90 in other:", sum(1 for r in recs if "lle_t90" in r["other"]),
          " tl100 in other:", sum(1 for r in recs if "tl100" in r["other"]))
    print("name null:", sum(1 for r in recs if r["name"] is None))


if __name__ == "__main__":
    main()
