#!/usr/bin/env python3
"""Acquire canonical E4 state Gini from Census ACS 1-year B19083.
Coverage is intentionally 2006-2023 only. No interpolation/backfill.
2020 ACS 1-year standard estimates were not released; collector records failure/missing
rather than substituting 5-year data silently.
"""
import hashlib,json,requests,os
from pathlib import Path
import pandas as pd

YEARS=[y for y in range(2006,2024) if y != 2020]
API="https://api.census.gov/data/{year}/acs/acs1"
OUT=Path("04_Raw_Data/E_Economic/Census_ACS_Gini"); OUT.mkdir(parents=True,exist_ok=True)
key=os.getenv("CENSUS_API_KEY")
if not key: raise RuntimeError("CENSUS_API_KEY required by current Census Data API")
rows=[]; raw={}; failures={"2020":"STRUCTURAL_MISSING: Census did not release standard ACS 1-year estimates; experimental estimates are not comparable to standard ACS series."}
for y in YEARS:
    url=API.format(year=y)
    params={"get":"NAME,B19083_001E,B19083_001M","for":"state:*","key":key}
    try:
        r=requests.get(url,params=params,timeout=60); r.raise_for_status()
        data=r.json(); raw[str(y)]=data
        hdr=data[0]
        for x in data[1:]:
            d=dict(zip(hdr,x)); fips=d["state"]
            if fips in {"11","60","66","69","72","78"}: continue
            # only 50 states; DC/territories excluded
            rows.append({"state":d["NAME"],"state_fips":fips,"year":y,
              "E4_gini":float(d["B19083_001E"]),
              "E4_gini_moe":None if d.get("B19083_001M") in (None,"","null") else float(d["B19083_001M"]),
              "source_table":"ACS1 B19083"})
    except Exception as e:
        failures[str(y)]=repr(e)

raw_path=OUT/"E4_ACS1_B19083_raw_2006_2023.json"
raw_path.write_text(json.dumps({"responses":raw,"failures":failures},indent=2),encoding="utf-8")
df=pd.DataFrame(rows)
if not df.empty:
    if df.duplicated(["state_fips","year"]).any(): raise RuntimeError("duplicate state-year")
    csv=OUT/"E4_ACS1_Gini_50states_2006_2023.csv"; df.to_csv(csv,index=False)
    csv_hash=hashlib.sha256(csv.read_bytes()).hexdigest()
else: csv_hash=None
coverage=df.groupby("year").state_fips.nunique().to_dict() if not df.empty else {}
for y,n in coverage.items():
    if n!=50: raise RuntimeError(f"{y}: expected 50 states, got {n}")
expected_years=set(YEARS)
if set(coverage)!=expected_years: raise RuntimeError(f"available-year coverage failure: {sorted(expected_years-set(coverage))}")
manifest={"source":"U.S. Census Bureau ACS 1-year B19083",
 "canonical_period":"2006-2023 excluding structurally missing 2020","earliest_acs_gini":2006,
 "expected_states_per_available_year":50,"coverage_by_year":coverage,
 "failures":failures,"no_interpolation":True,
 "note_2020":"Structural missing year. Census says 2020 experimental 1-year estimates should NOT be compared with standard ACS estimates; do not substitute experimental or 5-year data into canonical E4.",
 "raw_sha256":hashlib.sha256(raw_path.read_bytes()).hexdigest(),"csv_sha256":csv_hash}
(OUT/"E4_ACS_Gini_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
print(json.dumps(manifest,indent=2))
