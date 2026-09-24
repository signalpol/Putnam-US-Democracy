#!/usr/bin/env python3
"""One-command fail-closed core pipeline for Putnam U.S. Democracy Project.

Acquisition failures remain explicit. Structural S1 missingness is not imputed.
Master panel may still be built as an unbalanced evidence panel.
"""
from pathlib import Path
import subprocess,sys,json,hashlib,datetime,pandas as pd

ROOT=Path(".")
LOG=ROOT/"05_Audit_Provenance/core_pipeline_manifest.json"
LOG.parent.mkdir(parents=True,exist_ok=True)

steps=[
 ("ECONOMIC_GATE","06_Analysis/validate_economic_block_v1.py"),
 ("D_SDI2","06_Analysis/acquire_d_sdi2_2000_2023.py"),
 ("SOCIAL_GATE","06_Analysis/validate_social_capital_block_v1.py"),
]

def run(script):
    p=ROOT/script
    if not p.exists(): return {"status":"FAIL","reason":"script_missing"}
    cp=subprocess.run([sys.executable,str(p)],text=True,capture_output=True)
    return {"status":"PASS" if cp.returncode==0 else "FAIL","exit_code":cp.returncode,
            "stdout":cp.stdout[-8000:],"stderr":cp.stderr[-8000:]}

m={"run_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
   "status":"RUNNING","steps":{}}
for label,script in steps:
    m["steps"][label]=run(script)

# P03 density: only from validated CBP numerator + July-1 Census denominator.
num=ROOT/"04_Raw_Data/P03_CBP/P03_CBP_813410_establishments_2000_2023.csv"
den=ROOT/"04_Raw_Data/P03_population/P03_population_denominator_2000_2023.csv"
try:
    if not (num.exists() and den.exists()): raise FileNotFoundError("P03 validated numerator/denominator absent")
    n=pd.read_csv(num,dtype={"state":str}); d=pd.read_csv(den,dtype={"state":str})
    n["state"]=n.state.str.zfill(2); d["state"]=d.state.str.zfill(2)
    x=n.merge(d,on=["state","year"],validate="one_to_one")
    if len(x)!=1200: raise RuntimeError(f"P03 expected 1200 rows, got {len(x)}")
    x["P03_civic_social_orgs_per_1000"]=1000*x["ESTAB"]/x["population"]
    out=ROOT/"validated/P03_CBP_density_2000_2023.csv"; out.parent.mkdir(exist_ok=True)
    x[["state","year","P03_civic_social_orgs_per_1000"]].to_csv(out,index=False)
    m["steps"]["P03_DENSITY"]={"status":"PASS","rows":len(x),"sha256":hashlib.sha256(out.read_bytes()).hexdigest()}
except Exception as e:
    m["steps"]["P03_DENSITY"]={"status":"FAIL","reason":str(e)}

# Build evidence panel even with legitimate missing S1 variables.
m["steps"]["MASTER_V020_STRICT"]=run("06_Analysis/build_master_panel_v0_20_STRICT.py")

# PIPELINE_COMPLETE is deliberately stricter than "a master file was written".
required=("PREFLIGHT","ECONOMIC_GATE","D_SDI2","SOCIAL_GATE","P03_DENSITY","MASTER_V020_STRICT")
m["status"]="PASS" if all(m["steps"].get(k,{}).get("status")=="PASS" for k in required) else "PARTIAL"
m["interpretation"]="PARTIAL means at least one acquisition/validation block is not executable or not acquired; it is not evidence failure and triggers no imputation."
LOG.write_text(json.dumps(m,indent=2),encoding="utf-8")
print(json.dumps(m,indent=2))
