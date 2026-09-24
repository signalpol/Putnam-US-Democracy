"""
Fail-closed extractor scaffold for Putnam P01/P02 from openICPSR Roper.sav.
Run only after the official Roper.sav bytes are lawfully downloaded.
It NEVER guesses variable names: it inventories labels and stops unless unique
committee/officer/year/state/weight candidates are found.
"""
from pathlib import Path
import json, hashlib, re, sys

SRC=Path("04_Raw_Data/Roper/Roper.sav")
OUT=Path("04_Raw_Data/Roper")
OUT.mkdir(parents=True,exist_ok=True)

if not SRC.exists():
    raise SystemExit("FAIL: official Roper.sav not present; no data fabricated.")

try:
    import pyreadstat
except ImportError:
    raise SystemExit("FAIL: install pyreadstat before inspection.")

df, meta = pyreadstat.read_sav(str(SRC), metadataonly=False)
labels=dict(zip(meta.column_names, meta.column_labels or [""]*len(meta.column_names)))

patterns={
 "P01_committee":[r"committee",r"local organ"],
 "P02_officer":[r"officer",r"club",r"organization"],
 "year":[r"year",r"survey date"],
 "state":[r"state"],
 "weight":[r"weight",r"wt"]
}
def hits(words):
    out=[]
    for v,l in labels.items():
        s=(v+" "+(l or "")).lower()
        if all(re.search(w,s) for w in words):
            out.append({"variable":v,"label":l})
    return out

inventory={k:hits(v) for k,v in patterns.items()}
manifest={
 "source":str(SRC),
 "sha256":hashlib.sha256(SRC.read_bytes()).hexdigest(),
 "rows":len(df),"columns":len(df.columns),
 "candidates":inventory
}
(OUT/"Roper_sav_inventory.json").write_text(json.dumps(manifest,indent=2))

# Fail closed: no automatic state estimates until exact variables/codes are reviewed.
required=["P01_committee","P02_officer","year","state"]
missing=[k for k in required if len(inventory[k])==0]
if missing:
    raise SystemExit("FAIL: candidate(s) absent: "+", ".join(missing))

print(json.dumps(manifest,indent=2))
print("INSPECTION PASS: candidate fields found. MANUAL CODING REVIEW REQUIRED before extraction.")
