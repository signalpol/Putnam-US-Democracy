#!/usr/bin/env python3
"""
P03 Civic & Social Organization Density collector
Canonical definition: CBP NAICS 813410 establishments / Census resident population * 1,000.
Coverage target: 50 states x 2000-2023. DC/territories excluded.
Classification: PUTNAM-COMPATIBLE ADMINISTRATIVE REPLICATION (PROXY), not original Putnam/DDB data.
No interpolation.
"""
from __future__ import annotations
import io, re, zipfile, urllib.request
import pandas as pd

YEARS=range(2000,2024)
STATE_FIPS={"01","02","04","05","06","08","09","10","12","13","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","44","45","46","47","48","49","50","51","53","54","55","56"}

def get_bytes(url):
    with urllib.request.urlopen(url, timeout=90) as r: return r.read()

def normcols(df):
    df.columns=[str(c).strip().lower() for c in df.columns]
    return df

def cbp_year(y):
    yy=str(y)[-2:]
    url=f"https://www2.census.gov/programs-surveys/cbp/datasets/{y}/cbp{yy}st.zip"
    z=zipfile.ZipFile(io.BytesIO(get_bytes(url)))
    member=next(n for n in z.namelist() if n.lower().endswith((".txt",".csv")))
    df=normcols(pd.read_csv(z.open(member),dtype=str,low_memory=False))
    naics=next(c for c in df if c.startswith("naics"))
    st=next(c for c in df if c in ("fipstate","state","fips"))
    est=next(c for c in df if c in ("est","estab"))
    x=df[df[naics].astype(str).str.replace("-","",regex=False).eq("813410")].copy()
    if "lfo" in x: x=x[x.lfo.astype(str).str.zfill(3).eq("001")]
    if "empszes" in x: x=x[x.empszes.astype(str).str.zfill(3).eq("001")]
    x["state_fips"]=x[st].astype(str).str.zfill(2)
    x=x[x.state_fips.isin(STATE_FIPS)]
    x["establishments"]=pd.to_numeric(x[est],errors="coerce")
    # State file should resolve to exactly one total row per state after total LFO/size filters.
    out=x.groupby("state_fips",as_index=False)["establishments"].sum(min_count=1)
    if len(out)!=50: raise RuntimeError(f"{y}: expected 50 states, got {len(out)}")
    out["year"]=y; out["cbp_source_url"]=url
    return out

def pop_2000_2009():
    url="https://www2.census.gov/programs-surveys/popest/datasets/2000-2010/intercensal/state/st-est00int-alldata.csv"
    d=normcols(pd.read_csv(io.BytesIO(get_bytes(url)),encoding_errors="ignore",low_memory=False))
    st=next(c for c in d if c in ("state","state_fips"))
    name=next((c for c in d if c=="name"),None)
    # total resident population records only; file layout uses SEX=0, AGE=0, ORIGIN=0, RACE=0 where present.
    for c in ("sex","age","origin","race"):
        if c in d: d=d[pd.to_numeric(d[c],errors="coerce").fillna(0).eq(0)]
    d["state_fips"]=d[st].astype(str).str.zfill(2); d=d[d.state_fips.isin(STATE_FIPS)]
    rows=[]
    for y in range(2000,2010):
        candidates=[c for c in d if re.fullmatch(fr"popestimate{y}|pop{y}|population{y}",c)]
        if not candidates: raise RuntimeError(f"population column missing for {y}")
        c=candidates[0]
        q=d[["state_fips",c]+([name] if name else [])].drop_duplicates("state_fips")
        q["population"]=pd.to_numeric(q[c],errors="coerce"); q["year"]=y
        if name: q=q.rename(columns={name:"state_name"})
        rows.append(q.drop(columns=[c]))
    out=pd.concat(rows,ignore_index=True); out["population_source_url"]=url
    return out

def pop_2010_2020():
    url="https://www2.census.gov/programs-surveys/popest/datasets/2010-2020/state/totals/nst-est2020-alldata.csv"
    d=normcols(pd.read_csv(io.BytesIO(get_bytes(url)),encoding_errors="ignore"))
    d["state_fips"]=d["state"].astype(str).str.zfill(2); d=d[d.state_fips.isin(STATE_FIPS)]
    rows=[]
    for y in range(2010,2021):
        c=f"popestimate{y}"; q=d[["state_fips","name",c]].copy()
        q["population"]=pd.to_numeric(q[c],errors="coerce"); q["year"]=y
        rows.append(q.rename(columns={"name":"state_name"}).drop(columns=[c]))
    out=pd.concat(rows,ignore_index=True); out["population_source_url"]=url
    return out

def pop_2021_2023():
    url="https://www2.census.gov/programs-surveys/popest/datasets/2020-2023/state/totals/NST-EST2023-ALLDATA.csv"
    d=normcols(pd.read_csv(io.BytesIO(get_bytes(url)),encoding_errors="ignore"))
    d["state_fips"]=d["state"].astype(str).str.zfill(2); d=d[d.state_fips.isin(STATE_FIPS)]
    rows=[]
    for y in range(2021,2024):
        c=f"popestimate{y}"; q=d[["state_fips","name",c]].copy()
        q["population"]=pd.to_numeric(q[c],errors="coerce"); q["year"]=y
        rows.append(q.rename(columns={"name":"state_name"}).drop(columns=[c]))
    out=pd.concat(rows,ignore_index=True); out["population_source_url"]=url
    return out

def main():
    cbp=pd.concat([cbp_year(y) for y in YEARS],ignore_index=True)
    pop=pd.concat([pop_2000_2009(),pop_2010_2020(),pop_2021_2023()],ignore_index=True)
    z=cbp.merge(pop,on=["state_fips","year"],how="left",validate="one_to_one")
    z["P03_civic_social_org_density_per_1000"]=z["establishments"]/z["population"]*1000
    z["variable_id"]="P03"; z["proxy_flag"]="PROXY"
    z["measurement"]="Putnam-compatible administrative replication: NAICS 813410 establishments per 1,000 resident population"
    z["missing_rule"]="No interpolation; missing source observations remain missing"
    cols=["variable_id","state_fips","state_name","year","establishments","population","P03_civic_social_org_density_per_1000","proxy_flag","measurement","missing_rule","cbp_source_url","population_source_url"]
    z=z[cols].sort_values(["state_fips","year"])
    assert len(z)==1200 and z[["state_fips","year"]].drop_duplicates().shape[0]==1200
    z.to_csv("P03_Civic_Social_Organization_Density_2000_2023.csv",index=False)
    print("rows",len(z),"states",z.state_fips.nunique(),"years",z.year.nunique(),"missing_density",z.P03_civic_social_org_density_per_1000.isna().sum())

if __name__=="__main__": main()
