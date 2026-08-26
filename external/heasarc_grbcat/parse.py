#!/usr/bin/env python
"""Parse HEASARC GRBCAT (main + flux + afterglow tdat files) into normalized.jsonl.

Aggregation: one record per unique `id` (the cross-table join key).
  - t90/t50    : from main table, row with a value (prefer row carrying emin/emax)
  - fluence    : from flux table, fluence_units=='ergs' AND fluence_emin/emax present
                 (band annotation is mandatory); widest band wins on ties
  - peak_flux  : from flux table, flux_units=='photons' AND flux_emin/emax present
  - redshift   : from afterglow table (only ~22 rows have one)
  - time (MJD) -> UTC ISO via astropy
"""
import gzip
import json
import os
import re
import sys
from collections import defaultdict

from astropy.time import Time

HERE = os.path.dirname(os.path.abspath(__file__))
CAT = "heasarc_grbcat"

MAIN_COLS = ("record_number id name alt_names time time_def observatory ra dec "
             "coord_flag region afterglow_flag reference t50_mod t50 t50_error "
             "t50_range t50_emin t50_emax t90_mod t90 t90_error t90_range "
             "t90_emin t90_emax t_other flux_flag notes flux_notes local_notes "
             "class").split()
FLUX_COLS = ("record_number id name observatory flux_mod flux flux_error "
             "flux_units flux_energy flux_emin flux_emax fluence_mod fluence "
             "fluence_error fluence_units fluence_energy fluence_emin "
             "fluence_emax flux_notes").split()
AG_COLS = ("record_number id name alt_names telescope observatory band "
           "energy_range obs_time ra dec coord_flag local_notes detected "
           "intensity_mod intensity intensity_error intensity_error_min "
           "intensity_error_max intensity_units redshift_mod redshift "
           "redshift_error redshift_min redshift_max reference notes").split()

NAME_RE = re.compile(r"^GRB \d{6}[A-Z]?$")


def read_tdat(fname, cols):
    """Yield dict rows from the <DATA>..<END> section of a gzipped tdat file."""
    with gzip.open(os.path.join(HERE, fname), "rt", encoding="utf-8",
                   errors="replace") as fh:
        in_data = False
        for line in fh:
            line = line.rstrip("\n")
            if line == "<DATA>":
                in_data = True
                continue
            if line == "<END>":
                break
            if not in_data or not line:
                continue
            fields = line.split("|")
            if fields and fields[-1] == "":
                fields = fields[:-1]  # trailing pipe
            if len(fields) != len(cols):
                raise ValueError(f"{fname}: {len(fields)} fields != "
                                 f"{len(cols)} cols: {line[:120]}")
            yield dict(zip(cols, fields))


def fnum(s):
    """Parse float; missing markers ('', N/A, -99-style) -> None."""
    s = (s or "").strip()
    if not s or s.upper() in ("N/A", "NA", "NULL", "NONE"):
        return None
    try:
        v = float(s)
    except ValueError:
        return None
    if v in (-99.0, -99.99, -1.0e-07):
        return None
    return v


def band_str(emin, emax, fallback):
    lo, hi = fnum(emin), fnum(emax)
    if lo is not None and hi is not None:
        return f"{lo:g}-{hi:g} keV"
    s = (fallback or "").strip()
    return s if s else None


def mjd_to_iso(mjd):
    t = Time(mjd, format="mjd", scale="utc")
    t.format = "isot"
    t.precision = 3
    return t.value + "Z"


def main():
    # ---------------- main table ----------------
    bursts = {}          # id -> aggregated dict of raw-ish info
    n_main = 0
    for row in read_tdat("heasarc_grbcat.tdat.gz", MAIN_COLS):
        n_main += 1
        gid = int(row["id"])
        b = bursts.setdefault(gid, {
            "id": gid, "name": None, "alt": [], "times": [],
            "time_def": None, "coords": [], "observatories": [],
            "afterglow_flag": None, "flux_flag": None, "regions": set(),
            "t50": [], "t90": [], "t_other": None, "notes": [],
        })
        nm = row["name"].strip()
        if b["name"] is None and nm:
            b["name"] = nm
        if row["alt_names"].strip():
            b["alt"].append(row["alt_names"].strip())
        t = fnum(row["time"])
        if t is not None:
            b["times"].append(t)
            if b["time_def"] is None and row["time_def"].strip():
                b["time_def"] = row["time_def"].strip()
        ra, dec = fnum(row["ra"]), fnum(row["dec"])
        if ra is not None and dec is not None:
            try:
                cf = float(row["coord_flag"])
            except ValueError:
                cf = -1.0
            b["coords"].append((cf, ra, dec))
        obs = row["observatory"].strip()
        if obs and obs not in b["observatories"]:
            b["observatories"].append(obs)
        if row["afterglow_flag"].strip():
            b["afterglow_flag"] = row["afterglow_flag"].strip()
        if row["flux_flag"].strip():
            b["flux_flag"] = row["flux_flag"].strip()
        if row["region"].strip():
            b["regions"].add(row["region"].strip())
        for key in ("t50", "t90"):
            v = fnum(row[key])
            if v is not None:
                b[key].append({
                    "v": v, "err": fnum(row[f"{key}_error"]),
                    "mod": row[f"{key}_mod"].strip(),
                    "band": band_str(row[f"{key}_emin"], row[f"{key}_emax"],
                                     row[f"{key}_range"]),
                    "has_band_num": bool(row[f"{key}_emin"].strip()
                                         and row[f"{key}_emax"].strip()),
                })
        if b["t_other"] is None:
            b["t_other"] = fnum(row["t_other"])

    # ---------------- flux table ----------------
    fl_by_id = defaultdict(list)
    n_flux = 0
    for row in read_tdat("heasarc_grbcatflux.tdat.gz", FLUX_COLS):
        n_flux += 1
        fl_by_id[int(row["id"])].append(row)

    # ---------------- afterglow table (redshift) ----------------
    ag_by_id = defaultdict(list)
    n_ag = 0
    for row in read_tdat("heasarc_grbcatag.tdat.gz", AG_COLS):
        n_ag += 1
        if row["redshift"].strip():
            ag_by_id[int(row["id"])].append(row)

    # ---------------- emit ----------------
    out_path = os.path.join(HERE, "normalized.jsonl")
    stats = defaultdict(int)
    n_out = 0
    with open(out_path, "w", encoding="utf-8") as out:
        for gid in sorted(bursts):
            b = bursts[gid]
            rec = {"cat": CAT}

            nm = b["name"]
            rec["name"] = nm if (nm and NAME_RE.match(nm)) else None
            alts = []
            for a in b["alt"]:
                for piece in a.split(","):
                    piece = piece.strip()
                    if piece and piece not in alts:
                        alts.append(piece)
            if nm and not NAME_RE.match(nm):
                alts.insert(0, nm)
            rec["name_alt"] = alts

            if b["times"]:
                # rows of the same GRB can carry discrepant times (e.g. a
                # trigger-summary row hours off); take the most common value
                best_t = max(b["times"], key=b["times"].count)
                rec["trigger_time"] = mjd_to_iso(best_t)
            else:
                rec["trigger_time"] = None
            if b["coords"]:
                # coord_flag 0 = unique position; else highest confidence
                uniq = [c for c in b["coords"] if c[0] == 0.0]
                pick = uniq[0] if uniq else max(b["coords"],
                                                key=lambda c: c[0])
                rec["ra"], rec["dec"] = pick[1], pick[2]
            else:
                rec["ra"] = rec["dec"] = None

            params = {}
            for key in ("t90", "t50"):
                cands = b[key]
                if not cands:
                    continue
                # prefer a row that carries numeric band limits
                cands = sorted(cands,
                               key=lambda c: not c["has_band_num"])
                c = cands[0]
                obj = {"v": float(c["v"]), "err": c["err"],
                       "band": c["band"]}
                if c["mod"]:
                    obj["mod"] = c["mod"]
                params[key] = obj
                stats[key] += 1

            # fluence: ergs only, band limits mandatory
            flu_cands = []
            pf_cands = []
            for r in fl_by_id.get(gid, []):
                fv, fu = fnum(r["fluence"]), r["fluence_units"].strip().lower()
                lo, hi = fnum(r["fluence_emin"]), fnum(r["fluence_emax"])
                if fv is not None and fu == "ergs" and lo is not None \
                        and hi is not None:
                    flu_cands.append((hi - lo, fv, fnum(r["fluence_error"]),
                                      f"{lo:g}-{hi:g} keV",
                                      r["fluence_mod"].strip()))
                xv, xu = fnum(r["flux"]), r["flux_units"].strip().lower()
                xlo, xhi = fnum(r["flux_emin"]), fnum(r["flux_emax"])
                if xv is not None and xu == "photons" and xlo is not None \
                        and xhi is not None:
                    pf_cands.append((xhi - xlo, xv, fnum(r["flux_error"]),
                                     f"{xlo:g}-{xhi:g} keV",
                                     r["flux_mod"].strip()))
            if flu_cands:
                flu_cands.sort(key=lambda c: -c[0])  # widest band
                _, v, err, band, mod = flu_cands[0]
                obj = {"v": float(v), "err": err, "band": band}
                if mod:
                    obj["mod"] = mod
                params["fluence"] = obj
                stats["fluence"] += 1
            if pf_cands:
                pf_cands.sort(key=lambda c: -c[0])
                _, v, err, band, mod = pf_cands[0]
                obj = {"v": float(v), "err": err, "band": band}
                if mod:
                    obj["mod"] = mod
                params["peak_flux"] = obj
                stats["peak_flux"] += 1

            # redshift from afterglow table
            zrows = ag_by_id.get(gid, [])
            if zrows:
                # prefer a plain/~ measurement over a limit; among those
                # prefer rows with a stated error, then the latest catalog
                # entry (early GCN redshifts were sometimes later revised)
                def zrank(r):
                    limit = 0 if r["redshift_mod"].strip() in ("", "~") else 1
                    noerr = 0 if fnum(r["redshift_error"]) is not None else 1
                    return (limit, noerr, -int(r["record_number"]))
                zrows = sorted(zrows, key=zrank)
                z = fnum(zrows[0]["redshift"])
                if z is not None:
                    obj = {"v": z}
                    ze = fnum(zrows[0]["redshift_error"])
                    if ze is not None:
                        obj["err"] = ze
                    zm = zrows[0]["redshift_mod"].strip()
                    if zm:
                        obj["mod"] = zm
                    params["redshift"] = obj
                    stats["redshift"] += 1

            rec["params"] = params

            other = {"grbcat_id": gid,
                     "observatories": b["observatories"]}
            if b["time_def"]:
                other["time_def"] = b["time_def"]
            if b["regions"]:
                other["region"] = sorted(b["regions"])
            if b["afterglow_flag"]:
                other["afterglow_flag"] = b["afterglow_flag"]
            if b["flux_flag"]:
                other["flux_flag"] = b["flux_flag"]
            if b["t_other"] is not None:
                other["t_other"] = b["t_other"]
            rec["other"] = other

            out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n_out += 1

    print(f"raw rows: main={n_main} flux={n_flux} ag={n_ag}")
    print(f"unique GRBs (ids) in main table: {len(bursts)}")
    print(f"records written: {n_out} -> {out_path}")
    for k in ("t90", "t50", "fluence", "peak_flux", "redshift"):
        print(f"  {k}: {stats[k]}")
    print("  epeak: 0 (GRBCAT has no spectral params)")
    print("  eiso: 0 (not given; would need fluence + z)")


if __name__ == "__main__":
    sys.exit(main())
