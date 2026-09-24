#!/usr/bin/env python3
"""Build strict Putnam P03 density from observed Census CBP NAICS 813410
establishments and the canonical Census July-1 resident-population denominator.
No interpolation and no proxy substitution.
"""
from pathlib import Path
import pandas as pd, hashlib, json

CBP=Path("04_Raw_Data/P03_CBP/P03_CBP_813410_establishments_2000_2023.csv")
POP=Path("04_Raw_Data/P03_population/P03_population_denominator_2000_2023.csv")
OUT=Path("02_Putnam_14_Variables/P03")
OUT.mkdir(parents=True,exist_ok=True)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

if not CBP.exists(): raise FileNotFoundError(CBP)
if not POP.exists(): raise FileNotFoundError(POP)

e=pd.read_csv(CBP,dtype={"state":str})
p=pd.read_csv(POP,dtype={"state":str})
e["state"]=e["state"].astype(str).str.zfill(2)
p["state"]=p["state"].astype(str).str.zfill(2)

if "ESTAB" not in e.columns: raise RuntimeError("CBP ESTAB column missing")
if not {"state","year","population"}.issubset(p.columns): raise RuntimeError("population schema mismatch")
if e.duplicated(["state","year"]).any() or p.duplicated(["state","year"]).any():
    raise RuntimeError("duplicate state-year keys")

x=e.merge(p[["state","year","population"]],on=["state","year"],how="left",validate="one_to_one")
if len(x)!=1200 or x["state"].nunique()!=50 or x["year"].nunique()!=24:
    raise RuntimeError(f"P03 grid failure: rows={len(x)} states={x['state'].nunique()} years={x['year'].nunique()}")
if x["population"].isna().any(): raise RuntimeError("population denominator missing")
x["P03_civic_social_orgs_per_1000"]=1000*pd.to_numeric(x["ESTAB"],errors="raise")/pd.to_numeric(x["population"],errors="raise")
if x["P03_civic_social_orgs_per_1000"].isna().any() or (x["P03_civic_social_orgs_per_1000"]<0).any():
    raise RuntimeError("invalid P03 density")

out=OUT/"S1_P03_CBP_813410_density_2000_2023.csv"
x.to_csv(out,index=False)
m={"construct":"NAICS 813410 Civic and Social Organizations establishments per 1,000 July-1 residents",
   "coverage":"50 states x 2000-2023","rows":len(x),"no_interpolation":True,
   "cbp_sha256":sha(CBP),"population_sha256":sha(POP),"output_sha256":sha(out)}
(OUT/"S1_P03_density_manifest.json").write_text(json.dumps(m,indent=2),encoding="utf-8")
print(json.dumps(m,indent=2))
