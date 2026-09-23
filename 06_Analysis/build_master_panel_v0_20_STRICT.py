"""
Build Master Panel v0.20 STRICT.
Purpose:
- preserve 50 states x 2000-2023 = 1,200 keys;
- quarantine non-equivalent legacy Putnam proxies into R_* columns;
- merge only validated canonical D/E/S inputs;
- never interpolate or silently fill missing values.
"""
from pathlib import Path
import pandas as pd, json, hashlib

YEARS=range(2000,2024)
STATE_FIPS=[f"{x:02d}" for x in
[1,2,4,5,6,8,9,10,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,
30,31,32,33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56]]
EXPECTED=1200

ROOT=Path(".")
OLD=ROOT/"03_Master_Panel/Putnam_US_Democracy_Master_Panel_v0_19.csv"
OUT=ROOT/"03_Master_Panel/Putnam_US_Democracy_Master_Panel_v0_20_STRICT.csv"
AUD=ROOT/"05_Audit_Provenance/Master_Panel_v0_20_STRICT_manifest.json"

def canonical_grid():
    return pd.MultiIndex.from_product([STATE_FIPS,YEARS],names=["state","year"]).to_frame(index=False)

def normkeys(d):
    d=d.copy()
    # tolerate known legacy key names only
    ren={}
    for c in d.columns:
        lc=c.lower()
        if lc in ("state_fips","statefips","fips") and "state" not in d.columns: ren[c]="state"
        if lc=="year" and c!="year": ren[c]="year"
    d=d.rename(columns=ren)
    if "state" not in d or "year" not in d: raise ValueError("state/year keys absent")
    d["state"]=d["state"].astype(str).str.extract(r"(\d+)")[0].str.zfill(2)
    d["year"]=pd.to_numeric(d["year"],errors="raise").astype(int)
    return d

def validate_grid(d):
    assert len(d)==EXPECTED
    assert d["state"].nunique()==50 and d["year"].nunique()==24
    assert not d.duplicated(["state","year"]).any()
    assert set(d["state"])==set(STATE_FIPS)
    assert set(d["year"])==set(YEARS)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

panel=canonical_grid()
manifest={"version":"v0.20_STRICT","rows":EXPECTED,"rules":[],"inputs":[]}

# Preserve legacy data, but quarantine variables already adjudicated noncanonical.
if OLD.exists():
    old=normkeys(pd.read_csv(OLD))
    keep=[c for c in old.columns if c not in ("state","year")]
    old=old[["state","year"]+keep]
    quarantine={"P05":"R_P05_legacy","P07":"R_P07_legacy",
                "P09":"R_P09_legacy","P10":"R_P10_legacy"}
    old=old.rename(columns={k:v for k,v in quarantine.items() if k in old.columns})
    panel=panel.merge(old,on=["state","year"],how="left",validate="one_to_one")
    manifest["inputs"].append({"file":str(OLD),"sha256":sha(OLD)})
    manifest["rules"].append("P05/P07/P09/P10 legacy values moved to R_* robustness columns.")

# Optional validated inputs. Merge only if each file itself passes 50x24.
inputs=[
 ("validated/D1_SDI2_2000_2023.csv","D1"),
 ("validated/E3a_unemployment_2000_2023.csv","E3a"),
 ("validated/E3b_employment_population_2000_2023.csv","E3b"),
 ("validated/P03_CBP_density_2000_2023.csv","P03"),
]
for fn,label in inputs:
    p=ROOT/fn
    if not p.exists(): continue
    x=normkeys(pd.read_csv(p))
    validate_grid(x)
    cols=[c for c in x.columns if c not in ("state","year")]
    # protect against accidental overwrites
    overlap=set(cols)&set(panel.columns)
    if overlap: raise ValueError(f"{label}: overwrite collision {overlap}")
    panel=panel.merge(x,on=["state","year"],how="left",validate="one_to_one")
    manifest["inputs"].append({"label":label,"file":str(p),"sha256":sha(p)})

validate_grid(panel)
OUT.parent.mkdir(parents=True,exist_ok=True)
AUD.parent.mkdir(parents=True,exist_ok=True)
panel.to_csv(OUT,index=False)
manifest["output_sha256"]=sha(OUT)
manifest["columns"]=list(panel.columns)
manifest["missing_by_column"]={c:int(panel[c].isna().sum()) for c in panel.columns}
manifest["rules"] += [
 "No interpolation.",
 "No proxy promoted to canonical without equivalence adjudication.",
 "Missing canonical inputs remain missing.",
 "All merges one-to-one on state-year."
]
AUD.write_text(json.dumps(manifest,indent=2))
print(f"WROTE {OUT} rows={len(panel)} sha256={manifest['output_sha256']}")
