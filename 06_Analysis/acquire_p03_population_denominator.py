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
U00="https://www2.census.gov/programs-surveys/popest/datasets/2000-2010/intercensal/state/st-est00int-alldata.csv"
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
    d=pd.read_csv(io.BytesIO(b),encoding="latin1",low_memory=False)
    sc=fipscol(d); d[sc]=d[sc].astype(str).str.replace(r"\.0$","",regex=True).str.zfill(2); d=d[d[sc].isin(FIPS)]
    # all-data is long by YEAR; total resident population is AGE=0 and SEX=0.
    cols={str(c).upper():c for c in d.columns}
    if not {"YEAR","AGE","SEX","TOT_POP"}.issubset(cols): raise RuntimeError(f"2000 schema unexpected: {list(d.columns)}")
    x=d[(pd.to_numeric(d[cols["AGE"]],errors="coerce")==0)&(pd.to_numeric(d[cols["SEX"]],errors="coerce")==0)].copy()
    # Census YEAR coding: 1=4/1/2000, 2=7/1/2000 ... 12=7/1/2010.
    x["year"]=pd.to_numeric(x[cols["YEAR"]],errors="raise").astype(int)+1998
    x=x[x.year.between(2000,2009)]
    return pd.DataFrame({"state":x[sc],"year":x.year,"population":pd.to_numeric(x[cols["TOT_POP"]],errors="raise")})

def parse10(b):
    d=pd.read_excel(io.BytesIO(b),header=None)
    # Locate row containing Geography and use it as header.
    hr=next((i for i,row in d.iterrows() if row.astype(str).str.contains("Geographic|Geography",case=False,regex=True).any()),None)
    if hr is None: raise RuntimeError("2010 header row not found")
    d=pd.read_excel(io.BytesIO(b),header=hr)
    # Table is name-based; map exact 50 state names to FIPS.
    names=["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
    mp=dict(zip(names,sorted(FIPS,key=int)))
    namecol=d.columns[0]; d["_state"]=d[namecol].astype(str).str.strip().str.lstrip(".").map(mp); d=d[d._state.notna()]
    rows=[]
    for y in range(2010,2020):
        cand=[c for c in d.columns if re.search(fr"July 1,?\s*{y}|{y}",str(c),re.I)]
        # prefer July-1 estimate over census endpoint
        cand=[c for c in cand if "census" not in str(c).lower() and "april" not in str(c).lower()] or cand
        if len(cand)!=1: raise RuntimeError(f"2010-2020 column resolution failed {y}: {cand}")
        for _,r in d.iterrows(): rows.append((r._state,y,pd.to_numeric(r[cand[0]],errors="raise")))
    return pd.DataFrame(rows,columns=["state","year","population"])

def parse20(b):
    d=pd.read_csv(io.BytesIO(b),encoding="latin1")
    sc=fipscol(d); d[sc]=d[sc].astype(str).str.replace(r"\.0$","",regex=True).str.zfill(2); d=d[d[sc].isin(FIPS)]
    rows=[]
    for y in range(2020,2024):
        c=f"POPESTIMATE{y}"
        if c not in d: raise RuntimeError(f"{c} absent")
        for _,r in d.iterrows(): rows.append((r[sc],y,pd.to_numeric(r[c],errors="raise")))
    return pd.DataFrame(rows,columns=["state","year","population"])

raw00,raw10,raw20=get(U00),get(U10),get(U20)
frames=[parse00(raw00),parse10(raw10),parse20(raw20)]
x=pd.concat(frames,ignore_index=True).sort_values(["state","year"])
if len(x)!=1200 or x.state.nunique()!=50 or x.year.nunique()!=24: raise RuntimeError(f"grid failure rows={len(x)} states={x.state.nunique()} years={x.year.nunique()}")
if x.duplicated(["state","year"]).any() or (x.population<=0).any(): raise RuntimeError("key/population validation failure")
x["reference_date"]="July 1"
p=OUT/"P03_population_denominator_2000_2023.csv"; x.to_csv(p,index=False)
m={"rows":len(x),"states":50,"years":[2000,2023],"reference_date":"July 1","no_interpolation":True,
"sources":[{"url":U00,"sha256":sha(raw00)},{"url":U10,"sha256":sha(raw10)},{"url":U20,"sha256":sha(raw20)}],
"output_sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
(OUT/"manifest.json").write_text(json.dumps(m,indent=2),encoding="utf-8")
print(json.dumps(m,indent=2))
