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

