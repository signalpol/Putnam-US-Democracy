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
 ("PREFLIGHT","06_Analysis/preflight_acquisition_v1.py"),
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

m["steps"]["P03_DENSITY"]=run("06_Analysis/build_P03_density_population.py")

# Build evidence panel even with legitimate missing S1 variables.
m["steps"]["MASTER_V020_STRICT"]=run("06_Analysis/build_master_panel_v0_20_STRICT.py")

# PIPELINE_COMPLETE is deliberately stricter than "a master file was written".
# SOCIAL_GATE intentionally returns process exit 0 while its internal manifest can be PARTIAL
# because several strict Putnam continuations are structurally unavailable. Pipeline status
# therefore distinguishes executable completion from substantive S1 completeness.
required_exec=("PREFLIGHT","ECONOMIC_GATE","D_SDI2","SOCIAL_GATE","P03_DENSITY","MASTER_V020_STRICT")
m["status"]="EXECUTED" if all(m["steps"].get(k,{}).get("status")=="PASS" for k in required_exec) else "PARTIAL"
m["interpretation"]="EXECUTED means all pipeline programs completed successfully; it does not mean all P01-P14 strict continuations exist. PARTIAL means at least one acquisition/validation program failed or was unavailable. Neither status triggers imputation."
LOG.write_text(json.dumps(m,indent=2),encoding="utf-8")
print(json.dumps(m,indent=2))
