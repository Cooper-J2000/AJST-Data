#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
mpe_greiner 解析器：Greiner GRB 定位总表 (grbgen.html) -> normalized.jsonl

输出契约见 ../SCHEMA.md。本目录无 T90/Epeak/fluence/Eiso，
params 只放 redshift；定位/仪器/余辉标志等放入 other（键名=原列名）。
"""
import re
import json
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "grbgen.html")
OUT = os.path.join(HERE, "normalized.jsonl")

CELL_RE = re.compile(r"<TD[^>]*>(.*?)</TD>", re.S)
TAG_RE = re.compile(r"<[^>]+>")
POS_RE = re.compile(r"^(\d{1,2})h(\d{1,2})m([\d.]+)s([+-]?)(\d{1,3})°([\d.]+)'?$")
Z_RE = re.compile(r"^(<?)([\d.]+)(phh|ph|ul|h|\?)?$")
ZRANGE_RE = re.compile(r"^[\d.]+-[\d.]+$")


def cell_text(c):
    """去标签、反转义实体、&nbsp;->空"""
    t = TAG_RE.sub("", c)
    t = html.unescape(t).replace("\xa0", " ").strip()
    return t


def parse_pos(raw):
    """'12h52m14s +01° 28'' -> (ra_deg, dec_deg)；Dec 缺符号返回 dec=None"""
    compact = re.sub(r"\s+", "", raw)
    m = POS_RE.match(compact)
    if not m:
        return None, None
    h, mi, s, sign, d, dm = m.groups()
    ra = 15.0 * (int(h) + int(mi) / 60.0 + float(s) / 3600.0)
    if sign == "":
        return ra, None  # 原始数据缺符号（190810AS 一行）
    dec = int(d) + float(dm) / 60.0
    if sign == "-":
        dec = -dec
    return ra, dec


def parse_name(raw):
    """'260527AS' -> (name='GRB 260527A', short=True, alt='GRB 260527AS')"""
    short = raw.endswith("S")
    base = raw[:-1] if short else raw
    return "GRB " + base, short, ("GRB " + raw) if short else None


def obs_date(yymmdd):
    yy = int(yymmdd[:2])
    year = 1900 + yy if yy > 50 else 2000 + yy
    return "%04d-%s-%s" % (year, yymmdd[2:4], yymmdd[4:6])


def main():
    raw = open(SRC, encoding="latin-1").read()
    # 1) 切掉文末年度统计小表；2) 剔除 HTML 注释（内含模板占位行）
    main_html = raw.split("GRB and afterglow")[0]
    main_html = re.sub(r"<!--.*?-->", "", main_html, flags=re.S)

    records = []
    n_z = 0
    for chunk in main_html.split("<TR")[1:]:
        cells = CELL_RE.findall(chunk)
        if len(cells) != 10:
            continue
        vals = [cell_text(c) for c in cells]
        if not re.match(r"^\d{6}[A-Z]*$", vals[0]):
            continue  # 表头行

        name_raw = vals[0]
        name, short, alt = parse_name(name_raw)
        ra, dec = parse_pos(vals[1])

        other = {}
        other["obs_date"] = obs_date(name_raw[:6])
        if short:
            other["short_grb"] = True
        other["GRB X-ray position"] = re.sub(r"\s+", " ", vals[1])
        for key, v in zip(["Error", "Instrument", "IPN", "XA", "OT", "RA", "IAUC"],
                          vals[2:9]):
            if v:
                other[key] = v

        params = {}
        z = vals[9]
        if z:
            n_z += 1
            m = Z_RE.match(z)
            if m:
                lt, val, flag = m.groups()
                params["redshift"] = {"v": float(val)}
                flags = []
                if lt:
                    flags.append("ul")
                if flag:
                    flags.append(flag)
                if flags:
                    other["z_flag"] = ",".join(flags)
            elif ZRANGE_RE.match(z):
                other["z_range"] = z  # 范围红移无法转单一 float
            else:
                other["z_raw"] = z  # 兜底：未识别格式原样保留

        rec = {
            "cat": "mpe_greiner",
            "name": name,
            "name_alt": [alt] if alt else [],
            "trigger_time": None,
            "ra": ra,
            "dec": dec,
            "params": params,
            "other": other,
        }
        records.append(rec)

    with open(OUT, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print("records:", len(records))
    print("with redshift cell:", n_z)
    print("with params.redshift:", sum(1 for r in records if "redshift" in r["params"]))
    print("z_range:", sum(1 for r in records if "z_range" in r["other"]))
    print("z_flag:", sum(1 for r in records if "z_flag" in r["other"]))
    print("short:", sum(1 for r in records if r["other"].get("short_grb")))
    print("ra/dec missing:", sum(1 for r in records if r["ra"] is None),
          sum(1 for r in records if r["dec"] is None))


if __name__ == "__main__":
    main()
