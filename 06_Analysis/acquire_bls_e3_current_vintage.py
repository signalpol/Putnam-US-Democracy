"""
Acquire E3a/E3b from BLS current revised historical LAUS series.
Canonical period: 2000-2023, 50 states.
Vintage rule: current BLS historical series incorporating 2025 re-estimation back to 1976.

No interpolation. Script fails closed if validation gates are not met.
"""
from pathlib import Path
import io, zipfile, hashlib, requests, pandas as pd

YEARS=range(2000,2024)
EXPECTED=1200
OUT=Path("04_Raw_Data/BLS_E3")
OUT.mkdir(parents=True, exist_ok=True)

# Official BLS LAUS flat-file directory documented at:
# https://download.bls.gov/pub/time.series/la/
LA_BASE="https://download.bls.gov/pub/time.series/la/"
# Official BLS annual-average CNP16+/LFPR/EPOP ZIP is linked from:
# https://www.bls.gov/lau/rdscnp16.htm

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def get(url, dest):
    r=requests.get(url,timeout=60)
    r.raise_for_status()
    dest.write_bytes(r.content)
    return {"path":str(dest),"sha256":sha256(dest),"bytes":dest.stat().st_size}

def validate(df,state="state",year="year",value=None):
    x=df[df[year].between(2000,2023)].copy()
    if x.duplicated([state,year]).any(): raise ValueError("duplicate state-year")
    if x[state].nunique()!=50: raise ValueError(f"expected 50 states, got {x[state].nunique()}")
    if x[year].nunique()!=24: raise ValueError(f"expected 24 years, got {x[year].nunique()}")
    if len(x)!=EXPECTED: raise ValueError(f"expected 1200 rows, got {len(x)}")
    if value and x[value].isna().any(): raise ValueError(f"missing {value}")
    return x

# Implementation note:
# BLS flat files are tab-delimited and require joining series metadata to annual
# values. E3a should select state unemployment-rate series and annual-average
# period M13/current annual field as documented by BLS.
# E3b should use the official annual-average employment-population-ratio file
# linked from rdscnp16.htm. Do not average rounded monthly ratios if the official
# annual-average series is available.

if __name__=="__main__":
    print("Collector specification ready.")
    print("Acquisition is not complete until official raw files are downloaded,")
    print("50-state/24-year/1200-key validation passes, and hashes are recorded.")
