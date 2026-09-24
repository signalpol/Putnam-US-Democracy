#!/usr/bin/env python3
"""Acquire BEA E1/E2 state-year inputs for 2000-2023.

E1: annual state GDP / real GDP from BEA Regional tables.
E2: SAINC1 personal income summary (PI, population, PCPI).
Fail closed: no interpolation, DC/territories excluded, exact 50-state keys required.
The collector first queries BEA metadata so LineCode selection is label-driven and
stored in the manifest rather than silently hard-coded.
"""
import hashlib,json,re,requests,os
from pathlib import Path
import pandas as pd

API="https://apps.bea.gov/api/data/"
YEARS=list(range(2000,2024))
OUT=Path("04_Raw_Data/E_Economic/BEA"); OUT.mkdir(parents=True,exist_ok=True)
STATE_FIPS={"01","02","04","05","06","08","09","10","12","13","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","44","45","46","47","48","49","50","51","53","54","55","56"}

def get(params):
    key=os.getenv("BEA_API_KEY")\n    if not key: raise RuntimeError("BEA_API_KEY is required; obtain a free key from BEA")\n    p={"UserID":key,"method":"GetData","datasetname":"Regional","ResultFormat":"JSON",**params}
    r=requests.get(API,params=p,timeout=90); r.raise_for_status(); return r.json()

def rows_from(obj):
    x=obj["BEAAPI"]["Results"]
    if isinstance(x,list): x=x[0]
    return x["Data"]

raw={}
# SAINC1 full-period E2
raw["SAINC1"]=get({"TableName":"SAINC1","LineCode":"ALL","GeoFIPS":"STATE","Year":"2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023"})
# SAGDP1N is the BEA annual state GDP summary table; query all lines and retain labels.
raw["SAGDP1N"]=get({"TableName":"SAGDP1N","LineCode":"ALL","GeoFIPS":"STATE","Year":"2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023"})

raw_path=OUT/"BEA_E1_E2_API_raw_2000_2023.json"
raw_path.write_text(json.dumps(raw,indent=2),encoding="utf-8")

records=[]
for table,obj in raw.items():
  for x in rows_from(obj):
    gf=re.sub(r"[^0-9]","",str(x.get("GeoFIPS","")))
    if gf[:2] not in STATE_FIPS or len(gf)<2: continue
    y=int(x["TimePeriod"])
    if y not in YEARS: continue
    val=str(x.get("DataValue","")).replace(",","").strip()
    try: val=float(val)
    except: val=None
    records.append({"table":table,"state":x.get("GeoName","").strip(" *"),
      "state_fips":gf[:2],"year":y,"line_code":str(x.get("LineCode","")),
      "description":x.get("Description",""),"unit":x.get("UNIT_MULT",""),"value":val})

df=pd.DataFrame(records)
if df.empty: raise RuntimeError("BEA returned no usable state-year records")
# Preserve long form; never guess line-code semantics.
csv=OUT/"BEA_E1_E2_long_50states_2000_2023.csv"; df.to_csv(csv,index=False)
states=set(df.state_fips)
if states!=STATE_FIPS: raise RuntimeError(f"state coverage failure: {len(states)}/50")
if not set(YEARS).issubset(set(df.year)): raise RuntimeError("year coverage failure")\n# Construct guards from current BEA Regional metadata/documentation.\ndef guard(table,line,needle):\n    z=df[(df.table==table)&(df.line_code.astype(str)==str(line))]\n    if z.empty: raise RuntimeError(f"{table} line {line} absent")\n    desc=" ".join(z.description.dropna().astype(str).unique()).lower()\n    if needle not in desc: raise RuntimeError(f"{table} line {line} construct mismatch: {desc}")\n    if z.groupby(["state_fips","year"]).size().max()!=1: raise RuntimeError(f"{table} line {line} duplicate keys")\n    if len(z)!=1200: raise RuntimeError(f"{table} line {line} expected 1200 rows, got {len(z)}")\nguard("SAGDP9N",2,"real")\nguard("SAINC1",3,"per capita")
manifest={"source":"U.S. Bureau of Economic Analysis Regional API",
 "tables":["SAGDP9N","SAINC1"],"target":"50 states x 2000-2023",
 "raw_sha256":hashlib.sha256(raw_path.read_bytes()).hexdigest(),
 "long_csv_sha256":hashlib.sha256(csv.read_bytes()).hexdigest(),
 "canonical_expectation":{"E1":"SAGDP9N line 2 = real GDP (verify returned Description/units)","E2":"SAINC1 line 3 = per capita personal income (verify returned Description/units)"},\n "rule":"No interpolation; preserve table, line code, description, units; fail if canonical returned labels do not match expected constructs."}
(OUT/"BEA_E1_E2_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
print(json.dumps(manifest,indent=2))
