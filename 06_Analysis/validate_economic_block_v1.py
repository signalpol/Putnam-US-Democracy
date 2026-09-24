#!/usr/bin/env python3
"""Run and validate the canonical E1-E5 economic block.

Each collector is independent and receives PASS/FAIL separately.
No interpolation, no proxy substitution, and no block-level PASS when any
required canonical collector fails. E4 has an intentional structural gap in 2020.
"""
from pathlib import Path
import subprocess,sys,json,datetime

ROOT=Path(".")
OUT=ROOT/"05_Audit_Provenance/Economic_Block_Validation_v1.json"
OUT.parent.mkdir(parents=True,exist_ok=True)

steps=[
 ("E1_E2_BEA","06_Analysis/acquire_e1_e2_bea_2000_2023.py"),
 ("E1_E2_BUILD","06_Analysis/build_e1_e2_canonical.py"),
 ("E3_BLS_LAUS","06_Analysis/acquire_e3_bls_laus_2000_2023.py"),
 ("E4_ACS_GINI","06_Analysis/acquire_e4_acs_gini_2006_2023.py"),
 ("E5_BEA_MFG_SHARE","06_Analysis/acquire_e5_bea_manufacturing_share_2000_2023.py"),
]

def run(script):
    p=ROOT/script
    if not p.exists():
        return {"status":"FAIL","reason":"script_missing"}
    cp=subprocess.run([sys.executable,str(p)],capture_output=True,text=True)
    return {"status":"PASS" if cp.returncode==0 else "FAIL",
            "exit_code":cp.returncode,
            "stdout":cp.stdout[-6000:],"stderr":cp.stderr[-6000:]}

m={"run_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
   "rules":{"no_interpolation":True,
            "no_proxy_substitution":True,
            "E4_2020":"STRUCTURAL_MISSING_STANDARD_ACS1"},
   "steps":{}}
for label,script in steps:
    m["steps"][label]=run(script)

m["status"]="PASS" if all(v["status"]=="PASS" for v in m["steps"].values()) else "PARTIAL"
OUT.write_text(json.dumps(m,indent=2),encoding="utf-8")
print(json.dumps(m,indent=2))
