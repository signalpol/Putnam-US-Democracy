"""
One-command core pipeline.
Runs independent acquisition/validation blocks, records PASS/FAIL per block,
and builds Master Panel v0.20 STRICT from PASS outputs only.

Expected working tree: repository root.
No interpolation. No silent proxy substitution. No block is marked PASS unless
its canonical validation succeeds.
"""
from pathlib import Path
import subprocess, sys, json, hashlib, datetime

ROOT=Path(".")
LOG=ROOT/"05_Audit_Provenance/core_pipeline_manifest.json"
LOG.parent.mkdir(parents=True,exist_ok=True)

steps=[
 ("P03_CBP","06_Analysis/acquire_p03_cbp_2000_2023.py"),
 ("P03_POP","06_Analysis/acquire_p03_population_denominator.py"),
 ("CORE_D_E","06_Analysis/run_core_acquisition_colab_v1.py"),
]

manifest={
 "run_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
 "status":"RUNNING","steps":{}
}

def run(label,script):
    p=Path(script)
    if not p.exists():
        return {"status":"FAIL","reason":"script_missing"}
    cp=subprocess.run([sys.executable,str(p)],text=True,capture_output=True)
    return {"status":"PASS" if cp.returncode==0 else "FAIL",
            "exit_code":cp.returncode,
            "stdout":cp.stdout[-8000:],
            "stderr":cp.stderr[-8000:]}

for label,script in steps:
    manifest["steps"][label]=run(label,script)

# Build P03 density only when numerator and denominator validated files exist.
num=ROOT/"04_Raw_Data/P03_CBP/P03_CBP_813410_establishments_2000_2023.csv"
den=ROOT/"04_Raw_Data/P03_population/P03_population_denominator_2000_2023.csv"
try:
    if not (num.exists() and den.exists()):
        raise FileNotFoundError("validated numerator/denominator files absent")
    import pandas as pd
    n=pd.read_csv(num,dtype={"state":str}); d=pd.read_csv(den,dtype={"state":str})
    n["state"]=n["state"].str.zfill(2); d["state"]=d["state"].str.zfill(2)
    x=n.merge(d,on=["state","year"],how="inner",validate="one_to_one")
    if len(x)!=1200: raise ValueError(f"P03 merge rows={len(x)}")
    x["P03_civic_social_orgs_per_1000"]=x["ESTAB"]/x["population"]*1000
    out=ROOT/"validated/P03_CBP_density_2000_2023.csv"
    out.parent.mkdir(parents=True,exist_ok=True)
    x[["state","year","P03_civic_social_orgs_per_1000"]].to_csv(out,index=False)
    manifest["steps"]["P03_DENSITY"]={"status":"PASS","rows":len(x),
      "sha256":hashlib.sha256(out.read_bytes()).hexdigest()}
except Exception as e:
    manifest["steps"]["P03_DENSITY"]={"status":"FAIL","reason":str(e)}

# STRICT builder is allowed to run even when some inputs failed: missing canonical
# blocks remain missing and are never synthesized.
manifest["steps"]["MASTER_V020_STRICT"]=run(
 "MASTER_V020_STRICT","06_Analysis/build_master_panel_v0_20_STRICT.py")

required=["P03_CBP","P03_POP","CORE_D_E","P03_DENSITY","MASTER_V020_STRICT"]
manifest["status"]="PASS" if all(manifest["steps"].get(k,{}).get("status")=="PASS" for k in required) else "PARTIAL"
LOG.write_text(json.dumps(manifest,indent=2))
print(json.dumps(manifest,indent=2))
