#!/usr/bin/env python3
"""Acquire canonical E4 state Gini from Census ACS 1-year B19083.
Coverage is intentionally 2006-2023 only. No interpolation/backfill.
2020 ACS 1-year standard estimates were not released; collector records failure/missing
rather than substituting 5-year data silently.
"""
import hashlib,json,requests
from pathlib import Path
import pandas as pd

YEARS=range(2006,2024)
API="https://api.census.gov/data/{year}/acs/acs1"
OUT=Path("04_Raw_Data/E_Economic/Census_ACS_Gini"); OUT.mkdir(parents=True,exist_ok=True)
rows=[]; raw={}; failures={}
for y in YEARS:
    url=API.format(year=y)
    params={"get":"NAME,B19083_001E,B19083_001M","for":"state:*"}
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
manifest={"source":"U.S. Census Bureau ACS 1-year B19083",
 "canonical_period":"2006-2023","earliest_acs_gini":2006,
 "expected_states_per_available_year":50,"coverage_by_year":coverage,
 "failures":failures,"no_interpolation":True,
 "note_2020":"Do not silently substitute ACS 5-year for missing/unreleased ACS 1-year standard estimates.",
 "raw_sha256":hashlib.sha256(raw_path.read_bytes()).hexdigest(),"csv_sha256":csv_hash}
(OUT/"E4_ACS_Gini_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
print(json.dumps(manifest,indent=2))
