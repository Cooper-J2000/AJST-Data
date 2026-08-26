#!/usr/bin/env python
"""Spot-check normalized.jsonl against the raw tdat rows."""
import gzip
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

def raw_row(path, trig):
    with gzip.open(path, "rt") as f:
        for line in f:
            if line and line[0].isdigit() and line.split("|")[0] == str(trig):
                return line.rstrip("\n")
    return None

recs = {}
with open(os.path.join(HERE, "normalized.jsonl")) as f:
    for line in f:
        r = json.loads(line)
        trig = int(r["name_alt"][0].split()[1])
        recs[trig] = r

MAIN = os.path.join(HERE, "heasarc_batsegrb.tdat.gz")
SPEC = os.path.join(HERE, "heasarc_batsegrbsp.tdat.gz")

for trig in (7980, 2052, 6404):
    print("=" * 100)
    print(f"trigger {trig}")
    print("RAW main:", raw_row(MAIN, trig))
    print("RAW spec:", raw_row(SPEC, trig))
    print("PARSED  :", json.dumps(recs[trig], indent=2, ensure_ascii=False))
    print()

print("=" * 100)
print("FAMOUS BURST: GRB 990123 (BATSE trigger 7343)")
print("RAW main:", raw_row(MAIN, 7343))
print("RAW spec:", raw_row(SPEC, 7343))
print(json.dumps(recs[7343], indent=2, ensure_ascii=False))
