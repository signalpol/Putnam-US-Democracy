#!/usr/bin/env python3
"""Acquire and validate Berkeley State Democracy Index 2.0.

Canonical D outcome: democracy_mcmc.
Coverage required: 50 U.S. states x 2000-2023 = 1,200 state-years.
Preserve posterior uncertainty columns when distributed and democracy_additive
as a robustness outcome. Never substitute SDI 1.0 or another democracy index.
"""
import hashlib,io,json,requests
from pathlib import Path
import pandas as pd

URL="https://democracypolicylab.berkeley.edu/wp-content/uploads/2024/12/SDI_2.0.csv"
YEARS=set(range(2000,2024))
OUT=Path("04_Raw_Data/D_Democracy/Berkeley_SDI2"); OUT.mkdir(parents=True,exist_ok=True)
r=requests.get(URL,timeout=90); r.raise_for_status()
raw=r.content
raw_path=OUT/"SDI_2.0.csv"; raw_path.write_bytes(raw)
df=pd.read_csv(io.BytesIO(raw))
required={"year","democracy_mcmc"}
missing=required-set(df.columns)
if missing: raise RuntimeError(f"required columns absent: {sorted(missing)}")
state_col=next((c for c in ("state","State","state_name","statename") if c in df.columns),None)
if not state_col: raise RuntimeError(f"state column not identified; columns={list(df.columns)}")
x=df[df["year"].isin(YEARS)].copy()
# SDI 2.0 is defined for the 50 states; enforce exactly 50 state labels and 1200 keys.
if x[state_col].nunique()!=50: raise RuntimeError(f"expected 50 states, got {x[state_col].nunique()}")
if len(x)!=1200: raise RuntimeError(f"expected 1200 state-years, got {len(x)}")
if x.duplicated([state_col,"year"]).any(): raise RuntimeError("duplicate state-year keys")
if x["democracy_mcmc"].isna().any(): raise RuntimeError("missing canonical democracy_mcmc")
keep=[state_col,"year","democracy_mcmc"]
for c in ("democracy_mcmc_sd","democracy_mcmc_se","democracy_additive"):
    if c in x.columns: keep.append(c)
out=OUT/"D_SDI2_50states_2000_2023.csv"; x[keep].to_csv(out,index=False)
manifest={"source":"UC Berkeley Democracy Policy Lab, State Democracy Index 2.0",
 "source_url":URL,"canonical_outcome":"democracy_mcmc",
 "robustness_outcome":"democracy_additive" if "democracy_additive" in x.columns else None,
 "uncertainty_columns":[c for c in ("democracy_mcmc_sd","democracy_mcmc_se") if c in x.columns],
 "coverage":"50 states x 2000-2023","rows":len(x),
 "raw_sha256":hashlib.sha256(raw).hexdigest(),
 "validated_sha256":hashlib.sha256(out.read_bytes()).hexdigest(),
 "no_substitution":True}
(OUT/"D_SDI2_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
print(json.dumps(manifest,indent=2))
