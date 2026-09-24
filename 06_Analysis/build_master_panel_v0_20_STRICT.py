#!/usr/bin/env python3
"""Build Master Panel v0.20 STRICT: 50 states x 2000-2023.
Only actually present canonical artifacts are merged. Missing inputs remain missing.
No interpolation and no S2/S3 substitution.
"""
from pathlib import Path
import pandas as pd, json, hashlib

YEARS=range(2000,2024)
FIPS=[f"{x:02d}" for x in [1,2,4,5,6,8,9,10,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56]]
STATE_TO_FIPS=dict(zip(["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"],FIPS))
ROOT=Path(".")
OLD=ROOT/"03_Master_Panel/Putnam_US_Democracy_Master_Panel_v0_19.csv"
OUT=ROOT/"03_Master_Panel/Putnam_US_Democracy_Master_Panel_v0_20_STRICT.csv"
AUD=ROOT/"05_Audit_Provenance/Master_Panel_v0_20_STRICT_manifest.json"

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def norm(d):
    d=d.copy()
    # Prefer an explicit FIPS key when supplied; otherwise map state names.
    fips_col=next((c for c in d.columns if c.lower() in ("state_fips","statefips","fips")),None)
    state_col=next((c for c in d.columns if c.lower()=="state"),None)
    year_col=next((c for c in d.columns if c.lower()=="year"),None)
    if year_col is None: raise ValueError("year key absent")
    if year_col!="year": d=d.rename(columns={year_col:"year"})
    if fips_col is not None:
        if state_col is not None and state_col!=fips_col:
            d=d.rename(columns={state_col:"source_state_name"})
        d=d.rename(columns={fips_col:"state"})
        d["state"]=pd.to_numeric(d["state"],errors="raise").astype(int).astype(str).str.zfill(2)
    elif state_col is not None:
        if state_col!="state": d=d.rename(columns={state_col:"state"})
        s=d["state"].astype(str).str.strip()
        numeric=s.str.fullmatch(r"\d+(\.0)?")
        if numeric.all():
            d["state"]=pd.to_numeric(s,errors="raise").astype(int).astype(str).str.zfill(2)
        else:
            d["state"]=s.map(STATE_TO_FIPS)
            if d["state"].isna().any(): raise ValueError("unrecognized state-name key")
    else:
        raise ValueError("state key absent")
    d["year"]=pd.to_numeric(d["year"],errors="raise").astype(int)
    return d

def validate_full(x,label):
    if len(x)!=1200 or x.state.nunique()!=50 or x.year.nunique()!=24: raise ValueError(f"{label}: full-grid failure")
    if x.duplicated(["state","year"]).any(): raise ValueError(f"{label}: duplicate keys")
    if set(x.state)!=set(FIPS) or set(x.year)!=set(YEARS): raise ValueError(f"{label}: key-set failure")

def validate_sparse(x,label):
    if x.duplicated(["state","year"]).any(): raise ValueError(f"{label}: duplicate keys")
    if not set(x.state).issubset(set(FIPS)) or not set(x.year).issubset(set(YEARS)):
        raise ValueError(f"{label}: sparse keys outside canonical grid")

panel=pd.MultiIndex.from_product([FIPS,YEARS],names=["state","year"]).to_frame(index=False)
manifest={"version":"v0.20_STRICT",
 "rules":["No interpolation","No S2/S3 promotion into S1","Missing canonical inputs remain missing","All merges one-to-one"],
 "inputs":[],"missing_inputs":[]}

if OLD.exists():
    old=norm(pd.read_csv(OLD))
    old=old.rename(columns={k:v for k,v in {"P05":"R_P05_legacy","P07":"R_P07_legacy","P09":"R_P09_legacy","P10":"R_P10_legacy"}.items() if k in old.columns})
    # Never let legacy analytical D/E/P/S/T fields populate the strict panel.
    cols=[c for c in old.columns if c not in ("state","year") and (c.startswith("R_") or not c.startswith(("P","E","D","S","T")))]
    panel=panel.merge(old[["state","year"]+cols],on=["state","year"],how="left",validate="one_to_one")
    manifest["inputs"].append({"label":"legacy_quarantined","file":str(OLD),"sha256":sha(OLD)})

inputs=[
 ("04_Raw_Data/E_Economic/BEA/E1_E2_canonical_50states_2000_2023.csv","E1_E2","full"),
 ("04_Raw_Data/D_Democracy/Berkeley_SDI2/D_SDI2_50states_2000_2023.csv","D_SDI2","full"),
 ("04_Raw_Data/E_Economic/BLS_LAUS/E3_BLS_LAUS_50states_2000_2023.csv","E3","full"),
 ("04_Raw_Data/E_Economic/Census_ACS_Gini/E4_ACS1_Gini_50states_2006_2023.csv","E4","sparse"),
 ("04_Raw_Data/E_Economic/BEA_Industry/E5_BEA_manufacturing_value_added_share_50states_2000_2023.csv","E5","full"),
 ("02_Putnam_14_Variables/P03/S1_P03_CBP_813410_density_2000_2023.csv","P03","full"),
 ("04_Raw_Data/S_Social_Capital/STRICT/P06_TURNOUT/UF_ELECTION_LAB/S1_P06_UF_VEP_presidential_waves_2000_2020.csv","P06","sparse"),
 ("02_Putnam_14_Variables/P08/S1_P08_501c3_density_observed_snapshots.csv","P08","sparse"),
]

for rel,label,kind in inputs:
    p=ROOT/rel
    if not p.exists():
        manifest["missing_inputs"].append({"label":label,"file":rel})
        continue
    x=norm(pd.read_csv(p))
    validate_full(x,label) if kind=="full" else validate_sparse(x,label)
    data_cols=[c for c in x.columns if c not in ("state","year","source_state_name")]
    collisions=sorted(set(data_cols)&set(panel.columns))
    if collisions: raise ValueError(f"{label}: column collision {collisions}")
    panel=panel.merge(x[["state","year"]+data_cols],on=["state","year"],how="left",validate="one_to_one")
    manifest["inputs"].append({"label":label,"file":rel,"kind":kind,"rows":len(x),"sha256":sha(p)})

validate_full(panel[["state","year"]],"MASTER_KEYS")
OUT.parent.mkdir(parents=True,exist_ok=True)
panel.to_csv(OUT,index=False)
manifest.update({"rows":len(panel),"states":panel.state.nunique(),"years":panel.year.nunique(),
                 "columns":list(panel.columns),"output_sha256":sha(OUT),
                 "status":"BUILT_WITH_AVAILABLE_CANONICAL_INPUTS"})
AUD.parent.mkdir(parents=True,exist_ok=True)
AUD.write_text(json.dumps(manifest,indent=2),encoding="utf-8")
print(json.dumps({"rows":len(panel),"columns":len(panel.columns),"missing_inputs":manifest["missing_inputs"],"sha256":manifest["output_sha256"]},indent=2))
