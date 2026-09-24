#!/usr/bin/env python3
"""Acquire and extract canonical national P13 generalized trust from official GSS cumulative Stata bundle.

Official source: NORC GSS 1972-2024 cumulative cross-sectional data, Release 3a (July 2026).
Strict output is observed survey waves only; NEVER interpolate non-survey years.
Raw ZIP is preserved immutable and SHA-256 hashed before extraction.
"""
import hashlib, json, zipfile, io
from pathlib import Path
import requests, pandas as pd

URL="https://gss.norc.org/content/dam/gss/get-the-data/documents/stata/GSS_stata.zip"
OUT=Path("04_Raw_Data/S_Social_Capital/STRICT/P13_GSS/NATIONAL")
OUT.mkdir(parents=True,exist_ok=True)
RAW=OUT/"GSS_stata_release3a_2026-07.zip"

r=requests.get(URL,timeout=180)
r.raise_for_status()
RAW.write_bytes(r.content)
raw_sha=hashlib.sha256(RAW.read_bytes()).hexdigest()

with zipfile.ZipFile(RAW) as z:
    dta=[n for n in z.namelist() if n.lower().endswith(".dta")]
    if len(dta)!=1:
        raise RuntimeError(f"Expected one cumulative .dta, found {dta}")
    with z.open(dta[0]) as f:
        df=pd.read_stata(io.BytesIO(f.read()),convert_categoricals=False)

cols={c.lower():c for c in df.columns}
for required in ("year","trust"):
    if required not in cols:
        raise RuntimeError(f"Required variable {required} missing")
year=cols["year"]; trust=cols["trust"]

# Candidate weights are preserved/audited rather than silently guessed.
weight_candidates=[c for c in df.columns if c.lower() in
                   {"wtssall","wtssnr","wtssps","wtss"}]
if not weight_candidates:
    raise RuntimeError("No recognized GSS weight found; inspect release documentation")
weight=weight_candidates[0]

study=df[(df[year]>=2000)&(df[year]<=2023)].copy()
# GSS canonical TRUST coding historically: 1=can trust, 2=cannot be too careful, 3=depends.
# Fail closed if unexpected positive codes appear; negative codes are standardized missing.
positive=set(pd.to_numeric(study[trust],errors="coerce").dropna().astype(int))
valid_codes={1,2,3}
unexpected={x for x in positive if x>0 and x not in valid_codes}
if unexpected:
    raise RuntimeError(f"Unexpected TRUST codes {unexpected}; inspect codebook before extraction")

study["_trust"]=pd.to_numeric(study[trust],errors="coerce")
study["_w"]=pd.to_numeric(study[weight],errors="coerce")
study=study[(study["_trust"].isin([1,2,3]))&(study["_w"]>0)]

rows=[]
for y,g in study.groupby(year):
    denom=g["_w"].sum()
    est=100*(g.loc[g["_trust"]==1,"_w"].sum()/denom)
    rows.append({"year":int(y),"S1_P13_GSS_TRUST_pct":est,
                 "unweighted_valid_n":int(len(g)),"weight":weight,
                 "trust_variable":trust})
out=pd.DataFrame(rows).sort_values("year")
csv=OUT/"S1_P13_GSS_NATIONAL_observed_waves_2000_2023.csv"
out.to_csv(csv,index=False)

manifest={"source":"NORC General Social Survey",
 "release":"GSS 1972-2024 Cross-Sectional Cumulative Data, Release 3a, July 2026",
 "official_url":URL,"raw_file":RAW.name,"raw_sha256":raw_sha,
 "embedded_dta":dta[0],"study_period":"2000-2023","observed_years":out.year.tolist(),
 "trust_variable":trust,"weight_used":weight,
 "strict_rule":"Observed survey waves only; no interpolation; state geography not inferred.",
 "csv_sha256":hashlib.sha256(csv.read_bytes()).hexdigest()}
(OUT/"S1_P13_GSS_NATIONAL_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
print(out.to_string(index=False))
print(json.dumps(manifest,indent=2))
