"""
Core acquisition runner for Colab / ordinary HTTPS environment.
Targets:
 D1 Berkeley SDI 2.0
 E3a BLS LAUS state unemployment
 E3b BLS annual-average employment-population ratio
 P03 Census CBP NAICS 813410 + Census population denominator

This runner is fail-closed: it never labels a block complete unless raw bytes
are read and canonical validation passes.
"""
from pathlib import Path
import hashlib, json, requests, pandas as pd

ROOT=Path("putnam_core_acquisition")
RAW=ROOT/"raw"; OUT=ROOT/"validated"
RAW.mkdir(parents=True,exist_ok=True); OUT.mkdir(parents=True,exist_ok=True)
STATE_EXCLUDE={"11","60","66","69","72","78"}

def get(url,path):
    r=requests.get(url,timeout=120)
    r.raise_for_status()
    path.write_bytes(r.content)
    return {"url":url,"file":str(path),"bytes":len(r.content),
            "sha256":hashlib.sha256(r.content).hexdigest()}

def validate_50x24(df,state="state",year="year"):
    x=df.copy()
    x[state]=x[state].astype(str).str.zfill(2)
    x=x[~x[state].isin(STATE_EXCLUDE)]
    x=x[x[year].between(2000,2023)]
    assert x[state].nunique()==50
    assert x[year].nunique()==24
    assert len(x)==1200
    assert not x.duplicated([state,year]).any()
    return x

manifest={"status":"NOT_COMPLETE","downloads":[]}

# D1 official Berkeley file
SDI="https://democracypolicylab.berkeley.edu/wp-content/uploads/2025/01/SDI_2.0.csv"
try:
    p=RAW/"SDI_2.0.csv"; manifest["downloads"].append(get(SDI,p))
    d=pd.read_csv(p)
    required={"democracy_mcmc","democracy_mcmc_sd","democracy_mcmc_se","democracy_additive"}
    assert required.issubset(d.columns)
    # Detect canonical geography/time columns rather than silently rename unknown schema.
    scol=next((c for c in ["state","state_fips","fips"] if c in d.columns),None)
    ycol=next((c for c in ["year","Year"] if c in d.columns),None)
    assert scol and ycol
    d=d.rename(columns={scol:"state",ycol:"year"})
    d=validate_50x24(d)
    d.to_csv(OUT/"D1_SDI2_2000_2023.csv",index=False)
    manifest["D1"]="VALIDATED_1200"
except Exception as e: manifest["D1"]=f"FAILED: {e}"

# BLS official raw flat-file targets.
# E3a metadata/data endpoints are fixed; parsing follows BLS series metadata.
BLS_BASE="https://download.bls.gov/pub/time.series/la/"
for name in ["la.series","la.data.2.AllStatesU"]:
    try: manifest["downloads"].append(get(BLS_BASE+name,RAW/name))
    except Exception as e: manifest["E3a_download"]=f"FAILED: {e}"

# E3b annual-average ZIP URL is intentionally resolved from official BLS page
# in acquisition environment if the linked filename changes; do not hard-code a guessed filename.

# P03: invoke repository collector after Census API key is available if required.
# Census API now documents API-key requirements; set CENSUS_API_KEY in Colab secrets/env.
manifest["P03"]="RUN acquire_p03_cbp_2000_2023.py WITH OFFICIAL CENSUS API KEY"

(ROOT/"manifest.json").write_text(json.dumps(manifest,indent=2))
print(json.dumps(manifest,indent=2))
