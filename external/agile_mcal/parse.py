#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Parse the Second AGILE-MCAL GRB catalog (Ursi et al. 2022, ApJ 925, 152)
into normalized.jsonl following ../SCHEMA.md.

Primary source: mcal2grbcat.html (503 embedded JS `catEntry` rows, complete
catalog).  cds_table2.dat is only used to recover the T50/T90 lower-limit
(`>=`) and incomplete-acquisition (`*`) flags, which the web table lacks.

Key decisions (see README.md "坑"):
- Ep is taken from the WEB table (col. Ep), whose mean matches the paper's
  <Ep>=640 keV; CDS table4 Ep is inconsistent and not used.
- PL/Band flux & fluence bands are per-row (0.4-10MeV or 0.4-50MeV); the band
  string is stored with each value.
- Fluence prefers the Band fit when present, else the PL fit.
- Energy flux (erg/cm2/s, T90-averaged) is NOT peak photon flux, so it goes
  to `other`, not params.peak_flux.
- PL_BETA / BAND_ALPHA / BAND_BETA have separate lower/upper errors
  (emin/emax); stored as err=[abs(emax), abs(emin)] = [pos, neg].
- T50/T90 are measured on MCAL (sensitive band 0.4-100 MeV).
"""

import csv
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CAT = "agile_mcal"

ENTRY_RE = re.compile(r"new catEntry \((.*)\)\s*;")


def f(x):
    """Parse float; '' / None -> None."""
    if x is None:
        return None
    x = x.strip()
    if x == "":
        return None
    try:
        return float(x)
    except ValueError:
        return None


def band_from_range(rng):
    """'0.4-10MeV' -> '0.4-10 MeV' (None if empty)."""
    if not rng:
        return None
    return rng.replace("MeV", " MeV")


def read_cds_table2_flags(path):
    """name -> dict of limit/incomplete flags from cds_table2.dat."""
    flags = {}
    with open(path) as fh:
        for line in fh:
            line = line.rstrip("\n")
            if len(line) < 90:
                continue
            name = (line[0:3] + line[3:10]).strip()
            d = {}
            if ">=" in line[49:53]:
                d["l_T50"] = ">="
            if line[68:69].strip() == "*":
                d["f_T50"] = "*"
            if ">=" in line[70:74]:
                d["l_T90"] = ">="
            if line[89:90].strip() == "*":
                d["f_T90"] = "*"
            flags[name] = d
    return flags


def read_web_table(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    rows = []
    for m in ENTRY_RE.finditer(text):
        fields = next(csv.reader(io.StringIO(m.group(1))))
        rows.append(fields)
    return rows


def main():
    flags = read_cds_table2_flags(os.path.join(HERE, "cds_table2.dat"))
    rows = read_web_table(os.path.join(HERE, "mcal2grbcat.html"))

    out = []
    for fields in rows:
        assert len(fields) == 44, f"bad row ({len(fields)} fields): {fields[:2]}"
        (name_raw, ra, dec, lii, bii, t0, met, orbit,
         rm_sa, rm_ac, rm_mcal, mcal, bkg,
         t50, err_t50, cts_t50, t90, err_t90, cts_t90,
         loc, theta, phi,
         pl_range, pl_beta, pl_beta_emin, pl_beta_emax,
         pl_chi2, pl_dof, pl_flux, pl_fluence,
         band_range, b_alpha, b_alpha_emin, b_alpha_emax,
         b_beta, b_beta_emin, b_beta_emax,
         ec, ep, eb, band_chi2, band_dof, band_flux, band_fluence) = fields

        rec = {"cat": CAT}

        # ---- name -------------------------------------------------------
        if name_raw.startswith("GRB"):
            rec["name"] = "GRB " + name_raw[3:]
            rec["name_alt"] = [name_raw]
        else:  # 27 unconfirmed candidates, bare YYMMDD
            rec["name"] = None
            rec["name_alt"] = ["AGILE-MCAL " + name_raw]

        # ---- trigger time / position ------------------------------------
        rec["trigger_time"] = t0.strip() + "Z" if t0.strip() else None
        rec["ra"] = f(ra)
        rec["dec"] = f(dec)

        fl = flags.get(name_raw, {})
        params = {}

        # ---- durations (MCAL band 0.4-100 MeV) ---------------------------
        v, e = f(t50), f(err_t50)
        if v is not None:
            d = {"v": v, "err": e, "band": "0.4-100 MeV"}
            if fl.get("l_T50"):
                d["limit"] = ">="
            params["t50"] = d
        v, e = f(t90), f(err_t90)
        if v is not None:
            d = {"v": v, "err": e, "band": "0.4-100 MeV"}
            if fl.get("l_T90"):
                d["limit"] = ">="
            params["t90"] = d

        # ---- spectral fits ------------------------------------------------
        pl_band = band_from_range(pl_range.strip())
        bd_band = band_from_range(band_range.strip())

        # PL photon index -> spectral_index
        vb = f(pl_beta)
        if vb is not None:
            emin, emax = f(pl_beta_emin), f(pl_beta_emax)
            err = None
            if emin is not None and emax is not None:
                err = [abs(emax), abs(emin)]
            params["spectral_index"] = {"v": vb, "err": err, "model": "PL"}

        # Band alpha / beta
        va = f(b_alpha)
        if va is not None:
            emin, emax = f(b_alpha_emin), f(b_alpha_emax)
            err = [abs(emax), abs(emin)] if (emin is not None and emax is not None) else None
            params["alpha"] = {"v": va, "err": err, "model": "BAND"}
        vbb = f(b_beta)
        if vbb is not None:
            emin, emax = f(b_beta_emin), f(b_beta_emax)
            err = [abs(emax), abs(emin)] if (emin is not None and emax is not None) else None
            params["beta"] = {"v": vbb, "err": err, "model": "BAND"}

        # Epeak: WEB table Ep (no uncertainty published on the web table)
        vep = f(ep)
        if vep is not None:
            params["epeak"] = {"v": vep, "err": None, "model": "BAND", "frame": "obs"}

        # Fluence: prefer Band fit, else PL; keep the per-row band
        vfb, vfp = f(band_fluence), f(pl_fluence)
        if vfb is not None:
            params["fluence"] = {"v": vfb, "err": None, "band": bd_band, "model": "BAND"}
        elif vfp is not None:
            params["fluence"] = {"v": vfp, "err": None, "band": pl_band, "model": "PL"}

        rec["params"] = params

        # ---- catalog-specific raw columns ---------------------------------
        other = {}
        for key, val in [
            ("MET", f(met)), ("Orbit", f(orbit)),
            ("RM_SA", rm_sa), ("RM_AC", rm_ac), ("RM_MCAL", rm_mcal),
            ("MCAL", mcal), ("BKG", f(bkg)),
            ("BKGSUB_CTS_T50", f(cts_t50)), ("BKGSUB_CTS_T90", f(cts_t90)),
            ("LOC", loc.strip() or None), ("THETA", f(theta)), ("PHI", f(phi)),
            ("PL_RED_CHI_SQ", f(pl_chi2)), ("PL_DOF", f(pl_dof)),
            ("PL_FLUX", f(pl_flux)),
            ("BAND_RED_CHI_SQ", f(band_chi2)), ("BAND_DOF", f(band_dof)),
            ("BAND_FLUX", f(band_flux)),
            ("Ec", f(ec)), ("Eb", f(eb)),
        ]:
            if val is not None and val != "":
                other[key] = val
        # T50/T90 limit / incomplete-acquisition flags from CDS table2
        for k in ("l_T50", "f_T50", "l_T90", "f_T90"):
            if k in fl:
                other[k] = fl[k]
        rec["other"] = other

        out.append(rec)

    outpath = os.path.join(HERE, "normalized.jsonl")
    with open(outpath, "w") as fh:
        for rec in out:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # ---- summary ---------------------------------------------------------
    n = len(out)
    cnt = lambda k: sum(1 for r in out if k in r["params"])
    print(f"rows written: {n}")
    for k in ("t90", "t50", "epeak", "fluence", "spectral_index", "alpha", "beta"):
        print(f"  {k}: {cnt(k)}")
    print(f"  eiso: 0  redshift: 0 (catalog has neither)")
    print(f"  named GRBs: {sum(1 for r in out if r['name'])}; "
          f"candidates (name=null): {sum(1 for r in out if r['name'] is None)}")
    print(f"  fluence from BAND: {sum(1 for r in out if r['params'].get('fluence', {}).get('model') == 'BAND')}; "
          f"from PL: {sum(1 for r in out if r['params'].get('fluence', {}).get('model') == 'PL')}")
    print(f"  T90 lower limits: {sum(1 for r in out if r['params'].get('t90', {}).get('limit'))}")


if __name__ == "__main__":
    main()
