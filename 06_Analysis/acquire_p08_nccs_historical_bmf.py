#!/usr/bin/env python3
"""Acquire/aggregate Putnam P08 from NCCS harmonized historical BMF snapshots.
Downloads one selected snapshot per observed year, filters 501(c)(3), counts
unique EIN by 50 states. No interpolation; snapshot month is always retained.
Large raw BMF files are not committed to GitHub by this script.
"""
from pathlib import Path
import hashlib,json,requests
import pandas as pd

# Prefer a mid/late-year vintage when available; only catalog-verified vintages.
VINTAGES={
2000:"2000_05",2001:"2001_07",2002:"2002_07",2003:"2003_07",
2004:"2004_04",2005:"2005_07",2006:"2006_05",2007:"2007_04",
2008:"2008_06",2009:"2009_07",2010:"2010_07",2011:"2011_07",
2012:"2012_07",2013:"2013_07",2014:"2014_06",2015:"2015_07",
2016:"2016_08",2017:"2017_09",2018:"2018_12",2019:"2019_08",
2020:"2020_04",2022:"2022_08"}
# 2021 and 2023 require catalog verification before insertion.

BASE="https://nccsdata.s3.us-east-1.amazonaws.com/processed/bmf-legacy/{v}/"
OUT=Path("04_Raw_Data/S_Social_Capital/STRICT/P08_501C3_BMF")
OUT.mkdir(parents=True,exist_ok=True)
AGG=Path("02_Putnam_14_Variables/P08"); AGG.mkdir(parents=True,exist_ok=True)

STATES=set("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY".split())

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

rows=[]; manifest=[]
for year,v in VINTAGES.items():
    fn=f"bmf_{v}_processed.csv"
    url=BASE.format(v=v)+fn
    p=OUT/fn
    if not p.exists():
        with requests.get(url,stream=True,timeout=180) as r:
            r.raise_for_status()
            with p.open("wb") as f:
                for chunk in r.iter_content(1024*1024):
                    if chunk: f.write(chunk)
    # Schema is harmonized, but discover actual names fail-closed.
    hdr=pd.read_csv(p,nrows=0).columns.tolist()
    low={c.lower():c for c in hdr}
    ein=low.get("ein"); state=low.get("state") or low.get("state_abbr")
    subsection=low.get("subsection") or low.get("subsection_code")
    if not all([ein,state,subsection]):
        raise RuntimeError(f"{v}: required columns absent; {hdr}")
    counts={s:set() for s in STATES}
    for ch in pd.read_csv(p,usecols=[ein,state,subsection],dtype=str,chunksize=250000):
        ch[state]=ch[state].str.strip().str.upper()
        # Normalize subsection values such as 3, 03, 003.
        ss=pd.to_numeric(ch[subsection],errors="coerce")
        z=ch[(ss==3)&ch[state].isin(STATES)&ch[ein].notna()]
        for s,g in z.groupby(state):
            counts[s].update(g[ein].str.strip())
    if set(counts)!=STATES: raise RuntimeError("state whitelist failure")
    for s in sorted(STATES):
        rows.append({"year":year,"snapshot":v,"state":s,"P08_501c3_unique_ein_count":len(counts[s])})
    manifest.append({"year":year,"snapshot":v,"source_url":url,"raw_sha256":sha(p),"raw_bytes":p.stat().st_size})

out=pd.DataFrame(rows)
if out.duplicated(["year","state"]).any(): raise RuntimeError("duplicate state-year")
outp=AGG/"S1_P08_501c3_BMF_state_counts_observed_snapshots.csv"
out.to_csv(outp,index=False)
m={"source":"NCCS harmonized legacy IRS BMF","rule":"Observed snapshots only; no interpolation",
   "years":sorted(VINTAGES),"missing_study_years":[2021,2023],
   "rows":len(out),"processed_sha256":sha(outp),"snapshots":manifest}
(AGG/"S1_P08_BMF_manifest.json").write_text(json.dumps(m,indent=2),encoding="utf-8")
print(json.dumps({"rows":len(out),"years":len(VINTAGES),"missing":[2021,2023]},indent=2))
