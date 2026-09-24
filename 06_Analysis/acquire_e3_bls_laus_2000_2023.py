#!/usr/bin/env python3
"""Acquire E3 labor-market insecurity data from the official BLS Public Data API.

Canonical coverage: 50 states x 2000-2023.
Raw source: BLS Local Area Unemployment Statistics (LAUS).
Annual state series are NOT seasonally adjusted. No interpolation.
Outputs are written separately from the analytic master panel.

Series:
  LAUST{FIPS}0000000000003A = unemployment rate, annual, percent
  LAUST{FIPS}0000000000005A = employed persons, annual
  LAUST{FIPS}0000000000006A = civilian labor force, annual
Employment-population ratio is NOT inferred from employed/labor force; that would
be an employment rate, not the BLS employment-population ratio. Acquire the
proper population denominator/series separately before adding EPOP.
"""
import json, hashlib, sys, time, os
from pathlib import Path
import requests
import pandas as pd

YEARS=range(2000,2024)
STATE_FIPS={
"Alabama":"01","Alaska":"02","Arizona":"04","Arkansas":"05","California":"06",
"Colorado":"08","Connecticut":"09","Delaware":"10","Florida":"12","Georgia":"13",
"Hawaii":"15","Idaho":"16","Illinois":"17","Indiana":"18","Iowa":"19","Kansas":"20",
"Kentucky":"21","Louisiana":"22","Maine":"23","Maryland":"24","Massachusetts":"25",
"Michigan":"26","Minnesota":"27","Mississippi":"28","Missouri":"29","Montana":"30",
"Nebraska":"31","Nevada":"32","New Hampshire":"33","New Jersey":"34","New Mexico":"35",
"New York":"36","North Carolina":"37","North Dakota":"38","Ohio":"39","Oklahoma":"40",
"Oregon":"41","Pennsylvania":"42","Rhode Island":"44","South Carolina":"45",
"South Dakota":"46","Tennessee":"47","Texas":"48","Utah":"49","Vermont":"50",
"Virginia":"51","Washington":"53","West Virginia":"54","Wisconsin":"55","Wyoming":"56"}

API="https://api.bls.gov/publicAPI/v2/timeseries/data/"
OUT=Path("04_Raw_Data/E_Economic/BLS_LAUS")
OUT.mkdir(parents=True,exist_ok=True)

def sid(fips, measure):
    suffix={"unemployment_rate":"3","employed":"5","labor_force":"6"}[measure]
    return f"LAUST{fips}000000000000{suffix}A"

series_map={}
for state,fips in STATE_FIPS.items():
    for m in ("unemployment_rate","employed","labor_force"):
        series_map[sid(fips,m)]=(state,m)

rows=[]; raw_batches=[]
# BLS API 2.0 supports up to 20 years; use two periods and <=50 series/request.
ids=list(series_map)
for start,end in ((2000,2019),(2020,2023)):
    for i in range(0,len(ids),50):
        batch=ids[i:i+50]
        payload={"seriesid":batch,"startyear":str(start),"endyear":str(end)}
        resp=requests.post(API,json=payload,timeout=60)
        resp.raise_for_status()
        obj=resp.json()
        if obj.get("status")!="REQUEST_SUCCEEDED":
            raise RuntimeError(obj)
        raw_batches.append({"payload":payload,"response":obj})
        for s in obj["Results"]["series"]:
            state,measure=series_map[s["seriesID"]]
            for x in s["data"]:
                if x["period"]=="M13":  # annual average
                    rows.append({"state":state,"year":int(x["year"]),
                                 "measure":measure,"value":float(x["value"]),
                                 "series_id":s["seriesID"]})
        time.sleep(.2)

raw_path=OUT/"E3_BLS_LAUS_API_raw_2000_2023.json"
raw_path.write_text(json.dumps(raw_batches,indent=2),encoding="utf-8")
df=pd.DataFrame(rows)
wide=df.pivot(index=["state","year"],columns="measure",values="value").reset_index()
expected={(s,y) for s in STATE_FIPS for y in YEARS}
observed=set(map(tuple,wide[["state","year"]].itertuples(index=False,name=None)))
if observed!=expected:
    missing=sorted(expected-observed)[:25]
    raise RuntimeError(f"coverage failure: {len(observed)}/1200; sample missing={missing}")
if wide.duplicated(["state","year"]).any():
    raise RuntimeError("duplicate state-year keys")
csv_path=OUT/"E3_BLS_LAUS_50states_2000_2023.csv"
wide.to_csv(csv_path,index=False)
manifest={
 "source":"U.S. Bureau of Labor Statistics, Local Area Unemployment Statistics",
 "api":API,"coverage":"50 states x 2000-2023","rows":len(wide),
 "no_interpolation":True,"api_registration_key_used":bool(key),
 "raw_sha256":hashlib.sha256(raw_path.read_bytes()).hexdigest(),
 "csv_sha256":hashlib.sha256(csv_path.read_bytes()).hexdigest(),
 "note":"DC and territories excluded. Annual averages only. EPOP not fabricated."
}
(OUT/"E3_BLS_LAUS_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
print(json.dumps(manifest,indent=2))
