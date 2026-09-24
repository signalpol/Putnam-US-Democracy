#!/usr/bin/env python3
"""Build canonical E1/E2 state-year file from validated BEA long output."""
from pathlib import Path
import pandas as pd, hashlib, json

SRC=Path("04_Raw_Data/E_Economic/BEA/BEA_E1_E2_long_50states_2000_2023.csv")
OUT=Path("04_Raw_Data/E_Economic/BEA/E1_E2_canonical_50states_2000_2023.csv")
MAN=Path("05_Audit_Provenance/E1_E2_canonical_build_manifest.json")
if not SRC.exists(): raise FileNotFoundError(SRC)
d=pd.read_csv(SRC,dtype={"state_fips":str,"line_code":str})
d["state_fips"]=d.state_fips.str.zfill(2)
e1=d[(d.table=="SAGDP9N")&(d.line_code=="2")][["state_fips","year","value","description"]].copy()
e2=d[(d.table=="SAINC1")&(d.line_code=="3")][["state_fips","year","value","description"]].copy()
for name,x,needle in [("E1",e1,"real"),("E2",e2,"per capita")]:
    if len(x)!=1200 or x.duplicated(["state_fips","year"]).any():
        raise RuntimeError(f"{name} coverage/key failure rows={len(x)}")
    desc=" ".join(x.description.dropna().astype(str).unique()).lower()
    if needle not in desc: raise RuntimeError(f"{name} description mismatch: {desc}")
e1=e1.rename(columns={"value":"E1_REAL_GDP"})[["state_fips","year","E1_REAL_GDP"]]
e2=e2.rename(columns={"value":"E2_PC_PERSONAL_INCOME_NOMINAL"})[["state_fips","year","E2_PC_PERSONAL_INCOME_NOMINAL"]]
x=e1.merge(e2,on=["state_fips","year"],validate="one_to_one")
if len(x)!=1200: raise RuntimeError("E1/E2 merge coverage failure")
OUT.parent.mkdir(parents=True,exist_ok=True); x.to_csv(OUT,index=False)
MAN.parent.mkdir(parents=True,exist_ok=True)
m={"source":str(SRC),"rows":len(x),"rules":["No interpolation","E1 SAGDP9N line 2","E2 SAINC1 line 3; nominal PCPI retained until documented deflation step"],"sha256":hashlib.sha256(OUT.read_bytes()).hexdigest()}
MAN.write_text(json.dumps(m,indent=2),encoding="utf-8")
print(json.dumps(m,indent=2))
