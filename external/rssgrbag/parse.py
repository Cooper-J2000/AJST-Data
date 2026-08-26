#!/usr/bin/env python
"""Parse HEASARC rssgrbag (Radio-Selected GRB Afterglow Catalog, Chandra & Frail 2012).

Outputs (in this directory):
  - normalized.jsonl : one record per GRB (304 rows), per ../SCHEMA.md
  - lightcurve.jsonl : one record per radio peak-flux point (140 rows);
                       fields: name, ra, dec, time [s after burst], time_err [s],
                       band (e.g. '8.46GHz'), flux_mJy, flux_err_mJy, upperlimit,
                       reference, telescope, method ('fit'/'data')

NOTE: the published machine-readable tables (HEASARC tdat == CDS J/ApJ/746/156
table1+table4) contain only the *peak* flux density per radio frequency band,
not the full 2,995 individual flux-density measurements (those exist only in
the printed paper). lightcurve.jsonl is therefore built from the peak points:
time = observer-frame peak time t_m (days -> seconds), flux = peak flux density
(uJy -> mJy). Points with a flux error come from forward-shock light-curve
fits (method='fit'); points without error were taken directly from the data
(method='data'). All peaks are detections -> upperlimit=false.
"""
import gzip
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CAT = "rssgrbag"
REF = "Chandra & Frail 2012 (2012ApJ...746..156C)"

COLS = ("name source_flag instrument_code ra dec lii bii xray_ag_flag opt_ag_flag "
        "radio_ag_flag radio_telescope radio_telescope_flag t90 redshift_limit "
        "redshift redshift_max fluence_15_150_kev iso_bol_energy xray_flux_11h_limit "
        "xray_flux_11h opt_flux_11h_limit opt_flux_11h jet_break_time_limit "
        "jet_break_time jet_break_time_flag cbm_number_density "
        "cbm_number_density_flag coll_angle_limit coll_angle true_bol_energy_limit "
        "true_bol_energy ref_codes "
        "radio_freq_1 peak_flux_freq_1 peak_flux_freq_1_error peak_time_1 "
        "peak_time_1_error rf_peak_time_1 rf_peak_time_1_error "
        "radio_freq_2 peak_flux_freq_2 peak_flux_freq_2_error peak_time_2 "
        "peak_time_2_error rf_peak_time_2 rf_peak_time_2_error "
        "radio_freq_3 peak_flux_freq_3 peak_flux_freq_3_error peak_time_3 "
        "peak_time_3_error rf_peak_time_3 rf_peak_time_3_error "
        "radio_freq_4 peak_flux_freq_4 peak_flux_freq_4_error peak_time_4 "
        "peak_time_4_error rf_peak_time_4 rf_peak_time_4_error "
        "radio_freq_5 peak_flux_freq_5 peak_flux_freq_5_error peak_time_5 "
        "peak_time_5_error rf_peak_time_5 rf_peak_time_5_error "
        "radio_freq_6 peak_flux_freq_6 peak_flux_freq_6_error peak_time_6 "
        "peak_time_6_error rf_peak_time_6 rf_peak_time_6_error").split()

NAME_RE = re.compile(r"^GRB \d{6}[A-Z]?$")


def read_tdat(fname):
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
                fields = fields[:-1]
            if len(fields) != len(COLS):
                raise ValueError(f"{fname}: {len(fields)} fields != {len(COLS)}")
            yield dict(zip(COLS, fields))


def f(row, key):
    """Parse a float column; empty string -> None."""
    v = row[key].strip()
    return float(v) if v else None


def s(row, key):
    """Parse a string column; empty string -> None."""
    v = row[key].strip()
    return v if v else None


def limit_obj(row, value_key, limit_key):
    """Value with optional '<' / '>' limit flag folded into the object."""
    v = f(row, value_key)
    if v is None:
        return None
    obj = {"v": v}
    lim = s(row, limit_key)
    if lim:
        obj["limit"] = lim
    return obj


def main():
    rows = list(read_tdat("heasarc_rssgrbag.tdat.gz"))
    norm_out = open(os.path.join(HERE, "normalized.jsonl"), "w")
    lc_out = open(os.path.join(HERE, "lightcurve.jsonl"), "w")
    n_lc = 0
    for row in rows:
        name = s(row, "name")
        if not NAME_RE.match(name):
            name = None  # all 304 match in practice; guard per SCHEMA rule 4
        rec = {"cat": CAT, "name": name, "name_alt": [],
               "ra": f(row, "ra"), "dec": f(row, "dec"), "params": {}, "other": {}}
        p, o = rec["params"], rec["other"]

        t90 = f(row, "t90")
        if t90 is not None:
            # T90 is measured in the energy band of the discovering detector
            # (e.g. Swift: 15-350 keV); the band is not tabulated per row.
            p["t90"] = {"v": t90, "err": None, "band": None}
        z = f(row, "redshift")
        if z is not None:
            zobj = {"v": z}
            if s(row, "redshift_limit"):
                zobj["limit"] = s(row, "redshift_limit")
            zmax = f(row, "redshift_max")
            if zmax is not None:
                zobj["v_max"] = zmax  # z is then the *lower* bound of a range
            p["redshift"] = zobj
        flu = f(row, "fluence_15_150_kev")
        if flu is not None:
            p["fluence"] = {"v": flu, "err": None, "band": "15-150 keV"}
        eiso = f(row, "iso_bol_energy")
        if eiso is not None:
            p["eiso"] = {"v": eiso, "err": None,
                         "band": "1-10000 keV", "frame": "rest"}
        eg = limit_obj(row, "true_bol_energy", "true_bol_energy_limit")
        if eg is not None:
            eg.update({"err": None, "frame": "rest"})
            p["e_gamma"] = eg

        for k in ("source_flag", "instrument_code", "xray_ag_flag", "opt_ag_flag",
                  "radio_ag_flag", "radio_telescope", "radio_telescope_flag",
                  "ref_codes"):
            v = s(row, k)
            if v is not None:
                o[k] = v
        fx = limit_obj(row, "xray_flux_11h", "xray_flux_11h_limit")
        if fx is not None:
            fx["unit"] = "erg/s/cm^2"
            fx["band"] = ("1.6-10 keV" if s(row, "instrument_code") == "B"
                          else "0.3-10 keV")
            o["xray_flux_11h"] = fx
        fr = limit_obj(row, "opt_flux_11h", "opt_flux_11h_limit")
        if fr is not None:
            fr["unit"] = "microJy"
            fr["band"] = "R (0.7 micron)"
            o["opt_flux_11h"] = fr
        tj = limit_obj(row, "jet_break_time", "jet_break_time_limit")
        if tj is not None:
            tj["unit"] = "d"
            if s(row, "jet_break_time_flag"):
                tj["uncertain"] = True
            o["jet_break_time"] = tj
        n = f(row, "cbm_number_density")
        if n is not None:
            nobj = {"v": n, "unit": "cm^-3"}
            if s(row, "cbm_number_density_flag") == "i":
                nobj["assumed"] = True  # n not measured, assumed 1 cm^-3
            o["cbm_number_density"] = nobj
        th = limit_obj(row, "coll_angle", "coll_angle_limit")
        if th is not None:
            th["unit"] = "deg"
            o["coll_angle"] = th

        # Radio peak points (up to 6 frequency slots, ascending frequency)
        peaks = []
        for k in range(1, 7):
            flux = f(row, f"peak_flux_freq_{k}")
            if flux is None:
                continue
            peak = {"freq_GHz": f(row, f"radio_freq_{k}"),
                    "peak_flux_uJy": flux,
                    "peak_flux_uJy_err": f(row, f"peak_flux_freq_{k}_error"),
                    "peak_time_d": f(row, f"peak_time_{k}"),
                    "peak_time_d_err": f(row, f"peak_time_{k}_error"),
                    "rf_peak_time_d": f(row, f"rf_peak_time_{k}"),
                    "rf_peak_time_d_err": f(row, f"rf_peak_time_{k}_error")}
            peaks.append(peak)
            method = "fit" if peak["peak_flux_uJy_err"] is not None else "data"
            lc = {"name": name, "ra": rec["ra"], "dec": rec["dec"],
                  "time": round(peak["peak_time_d"] * 86400.0, 3),
                  "time_err": (round(peak["peak_time_d_err"] * 86400.0, 3)
                               if peak["peak_time_d_err"] is not None else None),
                  "band": f"{peak['freq_GHz']:g}GHz",
                  "flux_mJy": flux / 1000.0,
                  "flux_err_mJy": (peak["peak_flux_uJy_err"] / 1000.0
                                   if peak["peak_flux_uJy_err"] is not None
                                   else None),
                  "upperlimit": False,
                  "reference": REF,
                  "telescope": s(row, "radio_telescope"),
                  "method": method}
            lc_out.write(json.dumps(lc, ensure_ascii=False) + "\n")
            n_lc += 1
        if peaks:
            o["radio_peaks"] = peaks

        if not rec["params"]:
            rec.pop("params")
        norm_out.write(json.dumps(rec, ensure_ascii=False) + "\n")
    norm_out.close()
    lc_out.close()
    print(f"normalized.jsonl: {len(rows)} rows")
    print(f"lightcurve.jsonl: {n_lc} rows")


if __name__ == "__main__":
    main()
