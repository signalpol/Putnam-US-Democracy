#!/usr/bin/env python3
"""Acquire P06 from UF Election Lab 1980-2022 turnout v1.2.
Preserve published VEP turnout and construct highest-office/VEP alternative.
No interpolation or missing-ballot imputation.
"""
import hashlib,json,requests
from pathlib import Path
import pandas as pd
URL="https://election.lab.ufl.edu/data-downloads/turnoutdata/Turnout_1980_2022_v1.2.csv"
DOC="https://election.lab.ufl.edu/data-downloads/turnoutdata/Turnout_1980_2022_v1.2_doc.txt"
WAVES={2000,2004,2008,2012,2016,2020}
OUT=Path("04_Raw_Data/S_Social_Capital/STRICT/P06_TURNOUT/UF_ELECTION_LAB"); OUT.mkdir(parents=True,exist_ok=True)
raw=requests.get(URL,timeout=120); raw.raise_for_status()
doc=requests.get(DOC,timeout=60); doc.raise_for_status()
rp=OUT/"Turnout_1980_2022_v1.2.csv"; rp.write_bytes(raw.content)
dp=OUT/"Turnout_1980_2022_v1.2_doc.txt"; dp.write_bytes(doc.content)
df=pd.read_csv(rp)
need={"YEAR","STATE","VEP","VOTE_FOR_HIGHEST_OFFICE","VEP_TURNOUT_RATE"}
missing=need-set(df.columns)
if missing: raise RuntimeError(f"missing columns {missing}")
x=df[df.YEAR.isin(WAVES)].copy()
# Remove aggregate/DC rows by exact state-name whitelist.
states={"Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"}
x=x[x.STATE.isin(states)].copy()
if len(x)!=300 or x.STATE.nunique()!=50 or x.YEAR.nunique()!=6: raise RuntimeError(f"grid failure {len(x)}")
if x.duplicated(["STATE","YEAR"]).any(): raise RuntimeError("duplicate state-year")
for c in ["VEP","VOTE_FOR_HIGHEST_OFFICE","VEP_TURNOUT_RATE"]:
    x[c]=pd.to_numeric(x[c],errors="coerce")
# Canonical P06 preserves the published UF Election Lab VEP turnout field under an explicit project name.
x["P06_VEP_TURNOUT_PCT"]=x["VEP_TURNOUT_RATE"]
x["P06_HIGHEST_OFFICE_OVER_VEP"]=100*x["VOTE_FOR_HIGHEST_OFFICE"]/x["VEP"]
out=OUT/"S1_P06_UF_VEP_presidential_waves_2000_2020.csv"; x.to_csv(out,index=False)
manifest={"source":"UF Election Lab / Michael McDonald","version":"1.2","license":"CC BY 4.0",
"waves":sorted(WAVES),"expected_rows":300,"actual_rows":len(x),
"published_vep_turnout_missing":int(x.P06_VEP_TURNOUT_PCT.isna().sum()),
"rule":"No imputation. Preserve published VEP turnout; highest-office/VEP is separately named alternative.",
"raw_sha256":hashlib.sha256(rp.read_bytes()).hexdigest(),"doc_sha256":hashlib.sha256(dp.read_bytes()).hexdigest(),
"processed_sha256":hashlib.sha256(out.read_bytes()).hexdigest()}
(OUT/"P06_UF_v1_2_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
print(json.dumps(manifest,indent=2))
