#!/usr/bin/env python3
"""Build Putnam P08 density from observed NCCS historical BMF counts and the
canonical Census July-1 state resident-population denominator.
No interpolation; only exact state-year joins are accepted.
"""
from pathlib import Path
import hashlib,json
import pandas as pd

BMF=Path("02_Putnam_14_Variables/P08/S1_P08_501c3_BMF_state_counts_observed_snapshots.csv")
# Shared denominator produced by acquire_p03_population_denominator.py
POP_CANDIDATES=[
 Path("04_Raw_Data/P03_population/P03_population_denominator_2000_2023.csv"),
 Path("04_Raw_Data/S_Social_Capital/COMMON_DENOMINATORS/state_population_2000_2023.csv")
]
OUT=Path("02_Putnam_14_Variables/P08"); OUT.mkdir(parents=True,exist_ok=True)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
if not BMF.exists(): raise FileNotFoundError(BMF)
pop=next((p for p in POP_CANDIDATES if p.exists()),None)
if pop is None: raise FileNotFoundError("canonical Census population denominator not found")

b=pd.read_csv(BMF,dtype={"state":str})
p=pd.read_csv(pop,dtype={"state":str})
# Accept explicit population column only; never guess among several measures.
pc=[c for c in p.columns if c.lower() in {"population","resident_population","popestimate","pop"}]
if len(pc)!=1: raise RuntimeError(f"Need exactly one explicit population column, found {pc}")
pc=pc[0]
need_b={"year","state","P08_501c3_unique_ein_count"}
need_p={"year","state",pc}
if not need_b.issubset(b.columns) or not need_p.issubset(p.columns): raise RuntimeError("schema mismatch")
if b.duplicated(["year","state"]).any() or p.duplicated(["year","state"]).any(): raise RuntimeError("duplicate keys")
x=b.merge(p[["year","state",pc]],on=["year","state"],how="left",validate="one_to_one")
if x[pc].isna().any():
    miss=x.loc[x[pc].isna(),["year","state"]].to_dict("records")
    raise RuntimeError(f"population missing for observed BMF keys: {miss[:10]}")
x["P08_501c3_per_1000"]=1000*x["P08_501c3_unique_ein_count"]/pd.to_numeric(x[pc],errors="raise")
if (x["P08_501c3_per_1000"]<0).any(): raise RuntimeError("negative density")
out=OUT/"S1_P08_501c3_density_observed_snapshots.csv"; x.to_csv(out,index=False)
m={"construct":"501(c)(3) organizations per 1,000 state residents",
   "numerator":"unique EIN count in observed NCCS harmonized/transformed IRS BMF snapshot",
   "denominator":"canonical Census July-1 state resident population shared with P03",
   "no_interpolation":True,"rows":len(x),"years":sorted(map(int,x.year.unique())),
   "bmf_sha256":sha(BMF),"population_sha256":sha(pop),"output_sha256":sha(out)}
(OUT/"S1_P08_density_manifest.json").write_text(json.dumps(m,indent=2),encoding="utf-8")
print(json.dumps({"rows":len(x),"years":len(m["years"]),"output":str(out)},indent=2))
