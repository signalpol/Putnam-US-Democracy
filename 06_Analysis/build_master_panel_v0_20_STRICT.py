"""Build Master Panel v0.20 STRICT: 50 states x 2000-2023."""
from pathlib import Path
import pandas as pd,json,hashlib

YEARS=range(2000,2024)
FIPS=[f"{x:02d}" for x in [1,2,4,5,6,8,9,10,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56]]
NAMES=dict(zip(["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"],FIPS))
ROOT=Path("."); OLD=ROOT/"03_Master_Panel/Putnam_US_Democracy_Master_Panel_v0_19.csv"
OUT=ROOT/"03_Master_Panel/Putnam_US_Democracy_Master_Panel_v0_20_STRICT.csv"
AUD=ROOT/"05_Audit_Provenance/Master_Panel_v0_20_STRICT_manifest.json"

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(d):
    d=d.copy(); ren={}
    for c in d.columns:
        lc=c.lower()
        if lc in ("state","state_fips","statefips","fips") and c!="state": ren[c]="state"
        if lc=="year" and c!="year": ren[c]="year"
    d=d.rename(columns=ren)
    if not {"state","year"}.issubset(d.columns): raise ValueError("state/year keys absent")
    s=d.state.astype(str).str.strip()
    if s.str.fullmatch(r"\d+(\.0)?").all():
        d["state"]=pd.to_numeric(s).astype(int).astype(str).str.zfill(2)
    else:
        d["state"]=s.map(NAMES)
        if d.state.isna().any(): raise ValueError("unrecognized state-name key")
    d["year"]=pd.to_numeric(d.year,errors="raise").astype(int)
    return d

def validate_full(x,label):
    if len(x)!=1200 or x.state.nunique()!=50 or x.year.nunique()!=24: raise ValueError(f"{label}: full-grid failure")
    if x.duplicated(["state","year"]).any(): raise ValueError(f"{label}: duplicate keys")
    if set(x.state)!=set(FIPS) or set(x.year)!=set(YEARS): raise ValueError(f"{label}: key-set failure")

panel=pd.MultiIndex.from_product([FIPS,YEARS],names=["state","year"]).to_frame(index=False)
manifest={"version":"v0.20_STRICT","rules":["No interpolation","No S2/S3 promotion into S1","Missing canonical inputs remain missing","All merges one-to-one"],"inputs":[]}

if OLD.exists():
    old=norm(pd.read_csv(OLD))
    old=old.rename(columns={k:v for k,v in {"P05":"R_P05_legacy","P07":"R_P07_legacy","P09":"R_P09_legacy","P10":"R_P10_legacy"}.items() if k in old.columns})
    cols=[c for c in old.columns if c not in ("state","year")]
    panel=panel.merge(old[["state","year"]+cols],on=["state","year"],how="left",validate="one_to_one")
    manifest["inputs"].append({"label":"legacy_quarantined","file":str(OLD),"sha256":sha(OLD)})

inputs=[
 ("04_Raw_Data/E_Economic/BEA/E1_E2_canonical_50states_2000_2023.csv","E1_E2","full"),
 ("04_Raw_Data/D_Democracy/Berkeley_SDI2/D_SDI2_50states_2000_2023.csv","D_SDI2","full"),
 ("04_Raw_Data/E_Economic/BLS_LAUS/E3_BLS_LAUS_50states_2000_2023.csv","E3","full"),
 ("04_Raw_Data/E_Economic/Census_ACS_Gini/E4_ACS1_Gini_50states_2006_2023.csv","E4","sparse"),
 ("04_Raw_Data/E_Economic/BEA_Industry/E5_BEA_manufacturing_value_added_share_50states_2000_2023.csv","E5","full"),
 ("validated/P03_CBP_density_2000_2023.csv","P03","full"),\n ("04_Raw_Data/S_Social_Capital/STRICT/P06_TURNOUT/UF_ELECTION_LAB/S1_P06_UF_VEP_presidential_waves_2000_2020.csv","P06","sparse"),\n ("02_Putnam_14_Variables/P08/S1_P08_501c3_density_observed_snapshots.csv","P08","sparse"),
 ("02_Putnam_14_Variables/P08/S1_P08_501c3_density_observed_snapshots.csv","P08","sparse"),
 ("04_Raw_Data/S_Social_Capital/STRICT/P06_TURNOUT/UF_ELECTION_LAB/S1_P06_UF_VEP_presidential_waves_2000_2020.csv","P06","sparse"),
]
for fn,label,coverage in inputs:
    p=ROOT/fn
    if not p.exists(): continue
    x=norm(pd.read_csv(p))
    if coverage=="full": validate_full(x,label)
    else:
        if x.duplicated(["state","year"]).any(): raise ValueError(f"{label}: duplicate sparse keys")
        if not set(x.state).issubset(FIPS) or not set(x.year).issubset(set(YEARS)): raise ValueError(f"{label}: keys outside master grid")
    cols=[c for c in x.columns if c not in ("state","year")]
    overlap=set(cols)&set(panel.columns)
    if overlap: raise ValueError(f"{label}: overwrite collision {sorted(overlap)}")
    panel=panel.merge(x[["state","year"]+cols],on=["state","year"],how="left",validate="one_to_one")
    manifest["inputs"].append({"label":label,"coverage":coverage,"file":str(p),"sha256":sha(p)})

validate_full(panel,"MASTER")
OUT.parent.mkdir(parents=True,exist_ok=True); AUD.parent.mkdir(parents=True,exist_ok=True)
panel.to_csv(OUT,index=False)
manifest["rows"]=len(panel); manifest["columns"]=list(panel.columns)
manifest["missing_by_column"]={c:int(panel[c].isna().sum()) for c in panel.columns}
manifest["output_sha256"]=sha(OUT)
AUD.write_text(json.dumps(manifest,indent=2),encoding="utf-8")
print(f"WROTE {OUT} rows={len(panel)} sha256={manifest['output_sha256']}")
