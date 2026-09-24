#!/usr/bin/env python3
"""Fail-closed Social Capital S-block gate for Putnam P01-P14.

S1 = strict continuation only. S2 bridge and S3 modern proxy are NEVER promoted
to canonical P01-P14 fields. Missing strict continuations remain missing.
This gate records executable/acquired status without manufacturing annual data.
"""
from pathlib import Path
import subprocess,sys,json,datetime,hashlib

ROOT=Path("."); OUT=ROOT/"05_Audit_Provenance/Social_Capital_Block_Validation_v1.json"
OUT.parent.mkdir(parents=True,exist_ok=True)

# Only scripts that can legitimately create/validate strict inputs are executed.
steps=[
 ("P03_CBP","06_Analysis/acquire_p03_cbp_2000_2023.py"),
 ("P03_POP","06_Analysis/acquire_p03_population_denominator.py"),
 ("P06_UF","06_Analysis/acquire_p06_uf_electionlab_v1_2.py"),
 ("P08_BMF","06_Analysis/acquire_p08_nccs_historical_bmf.py"),
 ("P08_DENSITY","06_Analysis/build_p08_density.py"),
]
def run(script):
    p=ROOT/script
    if not p.exists(): return {"status":"MISSING_SCRIPT"}
    cp=subprocess.run([sys.executable,str(p)],capture_output=True,text=True)
    return {"status":"PASS" if cp.returncode==0 else "FAIL","exit_code":cp.returncode,
            "stdout":cp.stdout[-5000:],"stderr":cp.stderr[-5000:]}

m={"run_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
   "architecture":{"S0":"historical Putnam baseline","S1":"strict continuation",
     "S2":"bridge only","S3":"modern proxy only"},
   "rules":["No interpolation","No S2/S3 promotion into S1","Missing strict data remain missing",
            "P06 is election-wave only, not annualized","P08 uses observed historical BMF snapshots only"],
   "execution":{}}
for label,script in steps: m["execution"][label]=run(script)

# Variable-level status reflects the present strict-data architecture, not a claim
# that a full 2000-2023 numeric panel exists.
m["variables"]={
 "P01":{"construct":"Committee Service","strict_status":"BLOCKED_SOURCE","source":"Roper exact lineage; separate post-1994 continuation not acquired"},
 "P02":{"construct":"Officer Service","strict_status":"BLOCKED_SOURCE","source":"Roper exact lineage; separate post-1994 continuation not acquired"},
 "P03":{"construct":"Civic & Social Organization Density","strict_status":"COLLECTOR_PRESENT","source":"Census CBP 813410 + Census July-1 population"},
 "P04":{"construct":"Club Meetings","strict_status":"MISSING_STRICT","reason":"binary meeting-attendance proxy is non-equivalent to annual count"},
 "P05":{"construct":"Group Membership","strict_status":"PENDING_SOURCE","reason":"count candidate requires canonical state-weighted acquisition"},
 "P06":{"construct":"Presidential Turnout","strict_status":"ELECTION_WAVE_COLLECTOR_PRESENT","source":"UF Election Lab VEP; equivalence gate remains"},
 "P07":{"construct":"Public Meeting Attendance","strict_status":"PENDING_EQUIVALENCE","reason":"exact town/school wording unresolved"},
 "P08":{"construct":"Nonprofit Organization Density","strict_status":"OBSERVED_SNAPSHOT_COLLECTOR_PRESENT","source":"NCCS/IRS BMF + Census population"},
 "P09":{"construct":"Community Project","strict_status":"MISSING_STRICT","reason":"rate proxy non-equivalent to original annual frequency/count"},
 "P10":{"construct":"Volunteer Work","strict_status":"PENDING_EQUIVALENCE","reason":"annual frequency conversion must be supported without assumptions"},
 "P11":{"construct":"Visiting Friends","strict_status":"BLOCKED_SOURCE","reason":"exact DDB post-1998 public microdata not acquired"},
 "P12":{"construct":"Entertain at Home","strict_status":"BLOCKED_SOURCE","reason":"exact DDB post-1998 public microdata not acquired"},
 "P13":{"construct":"Generalized Trust","strict_status":"NATIONAL_GSS_ONLY_STATE_GEOCODE_RESTRICTED","source":"GSS TRUST"},
 "P14":{"construct":"Perceived Honesty","strict_status":"BLOCKED_SOURCE","reason":"exact DDB post-1998 public microdata not acquired"},
}
# Overall PASS is intentionally impossible unless all P01-P14 have validated S1
# data; PARTIAL is the correct state during acquisition.
complete=all(v["strict_status"]=="VALIDATED" for v in m["variables"].values())
m["status"]="PASS" if complete else "PARTIAL"
OUT.write_text(json.dumps(m,indent=2),encoding="utf-8")
print(json.dumps(m,indent=2))
