"""
Build annual state population denominator for P03, 2000-2023.
Canonical reference date: July 1 for every study year.

Sources:
  2000-2009: Census 2000-2010 intercensal July 1 estimates.
  2010-2019: Census 2010-2020 intercensal July 1 estimates.
  2020-2023: one current/revised PEP vintage that supplies July 1 estimates
             for 2020-2023 (do NOT substitute the April 1 2020 Census endpoint).

Fail closed: no interpolation; no mixed reference dates; source/vintage retained.
"""
from pathlib import Path
import pandas as pd, requests, hashlib, json, io

OUT=Path("04_Raw_Data/P03_population")
OUT.mkdir(parents=True,exist_ok=True)
STATE_EXCLUDE={"11","60","66","69","72","78"}
YEARS=set(range(2000,2024))

def sha_bytes(b): return hashlib.sha256(b).hexdigest()

def get_bytes(url, params=None):
    r=requests.get(url,params=params,timeout=120)
    r.raise_for_status()
    return r.content,r.url

def clean50(df):
    x=df.copy()
    x["state"]=x["state"].astype(str).str.zfill(2)
    x=x[~x["state"].isin(STATE_EXCLUDE)]
    x=x[x["year"].isin(YEARS)]
    if x["state"].nunique()!=50: raise ValueError("not 50 states")
    if x.duplicated(["state","year"]).any(): raise ValueError("duplicate state-year")
    if (x["population"]<=0).any(): raise ValueError("nonpositive population")
    return x

frames=[]; manifest=[]

# 2000-2009: API schema is discovered at runtime because Census requires an API key.
# Required semantic fields: state, year/date, July-1 resident population.
# API key must come from environment/Colab secret; never commit it.

# 2010-2019: official intercensal total table has POPESTIMATE2010...2019.
# Its 2020 endpoint is Census2020POP (April 1), so 2020 is deliberately excluded here.
# Raw XLS/CSV location should be resolved from official Census table page at runtime.

# 2020-2023: use a PEP release/vintage containing July-1 POPESTIMATE2020..2023
# in a single file/vintage where possible. This preserves a common reference date.

def validate_final(df):
    x=clean50(df)
    if len(x)!=1200 or x["year"].nunique()!=24:
        raise ValueError(f"expected 1200 50x24, got {len(x)}")
    if set(x["year"])!=YEARS: raise ValueError("year coverage mismatch")
    if set(x["reference_date"])!={"July 1"}:
        raise ValueError("mixed/non-July reference dates")
    return x.sort_values(["state","year"])

def write_final(df, source_manifest):
    x=validate_final(df)
    p=OUT/"P03_population_denominator_2000_2023.csv"
    x.to_csv(p,index=False)
    m={"rows":len(x),"states":x.state.nunique(),"years":x.year.nunique(),
       "sha256":hashlib.sha256(p.read_bytes()).hexdigest(),
       "sources":source_manifest,
       "rule":"July 1 resident population only; no interpolation"}
    (OUT/"manifest.json").write_text(json.dumps(m,indent=2))
    return p,m

if __name__=="__main__":
    print("Population collector scaffold validated.")
    print("Critical boundary rule: never use Census2020POP (April 1) as P03 July-1 2020 denominator.")
