"""
Acquire Putnam P03 modern continuation from official Census CBP API.
Target: NAICS 813410 Civic and Social Organizations, state establishments,
2000-2023. Fail closed on schema/coding changes. No interpolation.
"""
import requests, os, pandas as pd, hashlib, json
from pathlib import Path

YEARS=range(2000,2024)\nCENSUS_API_KEY=os.getenv("CENSUS_API_KEY")\nif not CENSUS_API_KEY: raise RuntimeError("CENSUS_API_KEY required by current Census Data API")
NAICS="813410"
OUT=Path("04_Raw_Data/P03_CBP")
OUT.mkdir(parents=True,exist_ok=True)

# Census CBP API patterns differ by vintage:
# 2012+ commonly use NAICS2012/2017/2022 and ESTAB.
# Earlier vintages require schema discovery. We query groups/variables first
# rather than silently assuming one variable name for all years.

def api_json(url, params=None):
    r=requests.get(url,params=params,timeout=60)
    r.raise_for_status()
    return r.json(), r.url

def variables(year):
    url=f"https://api.census.gov/data/{year}/cbp/variables.json"
    j,u=api_json(url)
    return j["variables"],u

def pick_naics_var(v):
    # explicit preference; exact availability validated per year
    candidates=["NAICS2022","NAICS2017","NAICS2012","NAICS2007","NAICS2002","NAICS1997","NAICS"]
    for x in candidates:
        if x in v: return x
    raise KeyError("No NAICS variable found")

def acquire_year(year):
    v,meta_url=variables(year)
    nvar=pick_naics_var(v)
    if "ESTAB" not in v: raise KeyError(f"{year}: ESTAB missing")
    params={"get":f"NAME,{nvar},ESTAB","for":"state:*",nvar:NAICS,"key":CENSUS_API_KEY}
    data,url=api_json(f"https://api.census.gov/data/{year}/cbp",params)
    df=pd.DataFrame(data[1:],columns=data[0])
    df["year"]=year
    df["ESTAB"]=pd.to_numeric(df["ESTAB"],errors="raise")
    label_var=nvar+"_LABEL"
    label=None
    if label_var in v:
        try:
            ld,_=api_json(f"https://api.census.gov/data/{year}/cbp",{"get":f"{label_var}","for":"state:01",nvar:NAICS,"key":CENSUS_API_KEY})
            if len(ld)>1: label=ld[1][0]
        except Exception: pass
    return df,{"year":year,"naics_variable":nvar,"naics_code":NAICS,"naics_label":label,
               "query_url":url,"metadata_url":meta_url,
               "comparability_note":"Preserve NAICS vintage; cross-vintage continuity must be audited before canonical density use."}

def validate_counts(df):
    # Census API may include DC/PR/territories; canonical panel retains only 50 states.
    # State FIPS exclusions are explicit.
    exclude={"11","60","66","69","72","78"}
    x=df[~df["state"].isin(exclude)].copy()
    if x["state"].nunique()!=50:
        raise ValueError(f"Expected 50 states, got {x['state'].nunique()}")
    if x.duplicated(["state","year"]).any():
        raise ValueError("Duplicate state-year")
    return x

if __name__=="__main__":
    frames=[]; manifest=[]
    for y in YEARS:
        d,m=acquire_year(y)
        frames.append(validate_counts(d)); manifest.append(m)
    out=pd.concat(frames,ignore_index=True)
    if len(out)!=1200 or out["year"].nunique()!=24 or out["state"].nunique()!=50:
        raise ValueError("Canonical 50x24 grid failed")
    csv=OUT/"P03_CBP_813410_establishments_2000_2023.csv"
    out.to_csv(csv,index=False)
    sha=hashlib.sha256(csv.read_bytes()).hexdigest()
    (OUT/"P03_CBP_manifest.json").write_text(json.dumps({"sha256":sha,"queries":manifest},indent=2))
    print(csv,sha,len(out))
