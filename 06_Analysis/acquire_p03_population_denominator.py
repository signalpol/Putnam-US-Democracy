#!/usr/bin/env python3
"""Acquire canonical July-1 resident population denominator, 50 states, 2000-2023.

Official Census sources only:
2000-2009: 2000-2010 intercensal state all-data.
2010-2019: 2010-2020 intercensal state table NST-EST2020INT-POP.
2020-2023: Vintage 2023 NST-EST2023-ALLDATA.
No interpolation; April-1 census endpoints are never substituted for July-1 values.
"""
from pathlib import Path
import pandas as pd,requests,hashlib,json,io,re

OUT=Path("04_Raw_Data/P03_population"); OUT.mkdir(parents=True,exist_ok=True)
U00="https://www2.census.gov/programs-surveys/popest/tables/2000-2010/intercensal/state/st-est00int-01.xls"
U10="https://www2.census.gov/programs-surveys/popest/tables/2010-2020/intercensal/national/nst-est2020int-pop.xlsx"
U20="https://www2.census.gov/programs-surveys/popest/datasets/2020-2023/state/totals/NST-EST2023-ALLDATA.csv"
FIPS={f"{x:02d}" for x in [1,2,4,5,6,8,9,10,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56]}

def get(url):
    r=requests.get(url,timeout=120,headers={"User-Agent":"Putnam-US-Democracy/1.0"}); r.raise_for_status(); return r.content
def sha(b): return hashlib.sha256(b).hexdigest()
def fipscol(d):
    for c in d.columns:
        if str(c).upper() in ("STATE","STATE_FIPS","STATEFIPS"): return c
    raise RuntimeError("state FIPS column absent")

def parse00(b):
    d=pd.read_excel(io.BytesIO(b),header=None)
    hr=next((i for i,row in d.iterrows() if row.astype(str).str.contains("Geographic|Geography",case=False,regex=True).any()),None)
    if hr is None: raise RuntimeError("2000 header row not found")
    d=pd.read_excel(io.BytesIO(b),header=hr)
    names=["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
    mp=dict(zip(names,sorted(FIPS,key=int)))
    namecol=d.columns[0]; d["_state"]=d[namecol].astype(str).str.strip().str.lstrip(".").map(mp); d=d[d._state.notna()]
    rows=[]
    for y in range(2000,2010):
        cand=[col for col in d.columns if re.search(fr"July 1,?\\s*{y}|{y}",str(col),re.I)]
        cand=[col for col in cand if "census" not in str(col).lower() and "april" not in str(col).lower()] or cand
        if len(cand)!=1: raise RuntimeError(f"2000-2010 column resolution failed {y}: {cand}")
        for _,r in d.iterrows(): rows.append((r._state,y,pd.to_numeric(r[cand[0]],errors="raise")))
    return pd.DataFrame(rows,columns=["state","year","population"])



def parse10(b):
    # Intercensal 2010-2020 national/state workbook. Resolve the state-name and
    # July-1 estimate columns by labels rather than fixed Excel coordinates.
    raw=pd.read_excel(io.BytesIO(b),header=None)
    names={"Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"}
    # Find the row containing the geographic-area header and re-read there.
    hr=next((i for i,row in raw.iterrows() if row.astype(str).str.contains("Geographic",case=False,regex=False).any()),None)
    if hr is None: raise RuntimeError("2010-2020 header row not found")
    d=pd.read_excel(io.BytesIO(b),header=hr)
    namecol=next((col for col in d.columns if "geographic" in str(col).lower()),d.columns[0])
    clean=d[namecol].astype(str).str.strip().str.lstrip(".")
    d=d[clean.isin(names)].copy(); d["_name"]=clean[clean.isin(names)]
    mp=dict(zip(sorted(names),[])) if False else None
    state_to_fips={"Alabama":"01","Alaska":"02","Arizona":"04","Arkansas":"05","California":"06","Colorado":"08","Connecticut":"09","Delaware":"10","Florida":"12","Georgia":"13","Hawaii":"15","Idaho":"16","Illinois":"17","Indiana":"18","Iowa":"19","Kansas":"20","Kentucky":"21","Louisiana":"22","Maine":"23","Maryland":"24","Massachusetts":"25","Michigan":"26","Minnesota":"27","Mississippi":"28","Missouri":"29","Montana":"30","Nebraska":"31","Nevada":"32","New Hampshire":"33","New Jersey":"34","New Mexico":"35","New York":"36","North Carolina":"37","North Dakota":"38","Ohio":"39","Oklahoma":"40","Oregon":"41","Pennsylvania":"42","Rhode Island":"44","South Carolina":"45","South Dakota":"46","Tennessee":"47","Texas":"48","Utah":"49","Vermont":"50","Virginia":"51","Washington":"53","West Virginia":"54","Wisconsin":"55","Wyoming":"56"}
    d["_state"]=d["_name"].map(state_to_fips)
    rows=[]
    for y in range(2010,2020):
        cand=[col for col in d.columns if re.fullmatch(fr".*{y}.*",str(col),re.I)]
        cand=[col for col in cand if "census" not in str(col).lower() and "base" not in str(col).lower() and "april" not in str(col).lower()]
        if len(cand)!=1: raise RuntimeError(f"2010-2020 column resolution failed {y}: {cand}")
        for _,r in d.iterrows():
            rows.append((r["_state"],y,pd.to_numeric(r[cand[0]],errors="raise")))
    return pd.DataFrame(rows,columns=["state","year","population"])

def parse20(b):
    d=pd.read_csv(io.BytesIO(b),dtype={"STATE":str})
    need={"STATE","NAME","POPESTIMATE2020","POPESTIMATE2021","POPESTIMATE2022","POPESTIMATE2023"}
    if not need.issubset(d.columns): raise RuntimeError(f"2020-2023 schema mismatch: {sorted(need-set(d.columns))}")
    d["STATE"]=d["STATE"].astype(str).str.zfill(2)
    d=d[d["STATE"].isin(FIPS)].copy()
    if d["STATE"].nunique()!=50: raise RuntimeError(f"2020-2023 expected 50 states, got {d['STATE'].nunique()}")
    rows=[]
    for y in range(2020,2024):
        col=f"POPESTIMATE{y}"
        for _,r in d.iterrows(): rows.append((r["STATE"],y,pd.to_numeric(r[col],errors="raise")))
    return pd.DataFrame(rows,columns=["state","year","population"])

if __name__=="__main__":
    b00=get(U00); b10=get(U10); b20=get(U20)
    rawdir=OUT/"source_files"; rawdir.mkdir(parents=True,exist_ok=True)
    (rawdir/"st-est00int-01.xls").write_bytes(b00)
    (rawdir/"nst-est2020int-pop.xlsx").write_bytes(b10)
    (rawdir/"NST-EST2023-ALLDATA.csv").write_bytes(b20)

    frames=[parse00(b00),parse10(b10),parse20(b20)]
    x=pd.concat(frames,ignore_index=True)
    x["state"]=x["state"].astype(str).str.zfill(2)
    x["year"]=pd.to_numeric(x["year"],errors="raise").astype(int)
    x["population"]=pd.to_numeric(x["population"],errors="raise")
    x=x.sort_values(["state","year"]).reset_index(drop=True)

    expected={(s,y) for s in FIPS for y in range(2000,2024)}
    observed=set(map(tuple,x[["state","year"]].itertuples(index=False,name=None)))
    if observed!=expected:
        raise RuntimeError(f"canonical grid failure: observed={len(observed)} expected=1200 missing={sorted(expected-observed)[:20]} extra={sorted(observed-expected)[:20]}")
    if len(x)!=1200 or x["state"].nunique()!=50 or x["year"].nunique()!=24:
        raise RuntimeError("canonical 50x24 dimensions failed")
    if x.duplicated(["state","year"]).any(): raise RuntimeError("duplicate state-year")
    if x["population"].isna().any() or (x["population"]<=0).any(): raise RuntimeError("invalid population")

    out=OUT/"P03_population_denominator_2000_2023.csv"
    x.to_csv(out,index=False)
    manifest={
      "construct":"July-1 resident population denominator",
      "coverage":"50 states x 2000-2023",
      "rows":len(x),"states":x["state"].nunique(),"years":x["year"].nunique(),
      "no_interpolation":True,
      "sources":[
        {"period":"2000-2009","url":U00,"sha256":sha(b00)},
        {"period":"2010-2019","url":U10,"sha256":sha(b10)},
        {"period":"2020-2023","url":U20,"sha256":sha(b20)}
      ],
      "output_sha256":sha(out.read_bytes())
    }
    (OUT/"P03_population_denominator_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    print(json.dumps(manifest,indent=2))
