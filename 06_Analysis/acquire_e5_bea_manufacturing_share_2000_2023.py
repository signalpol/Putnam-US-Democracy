#!/usr/bin/env python3
"""Acquire E5 manufacturing value-added share from BEA Regional GDP-by-state.

Fail-closed design:
- query BEA Regional metadata/data;
- identify all-industry and manufacturing lines from returned descriptions;
- never guess a line code when labels are ambiguous;
- use current-dollar numerator and denominator from the same table/vintage;
- preserve raw response, labels, hashes, coverage and missingness.
"""
import hashlib,json,re,requests,os
from pathlib import Path
import pandas as pd

API="https://apps.bea.gov/api/data/"
YEARS=list(range(2000,2024))
STATE_FIPS={"01","02","04","05","06","08","09","10","12","13","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","44","45","46","47","48","49","50","51","53","54","55","56"}
OUT=Path("04_Raw_Data/E_Economic/BEA_Industry"); OUT.mkdir(parents=True,exist_ok=True)

def req(params):
    key=os.getenv("BEA_API_KEY")\n    if not key: raise RuntimeError("BEA_API_KEY is required; obtain a free key from BEA")\n    p={"UserID":key,"method":"GetData","datasetname":"Regional","ResultFormat":"JSON",**params}
    r=requests.get(API,params=p,timeout=90); r.raise_for_status()
    obj=r.json()
    if "Error" in json.dumps(obj.get("BEAAPI",{}))[:1000]:
        raise RuntimeError(obj)
    return obj

years=",".join(map(str,YEARS))
# SAGDP2N: GDP by state, current dollars, by industry. Query all lines so
# identification is based on returned labels rather than undocumented guesses.
obj=req({"TableName":"SAGDP2N","LineCode":"ALL","GeoFIPS":"STATE","Year":years})
raw_path=OUT/"E5_BEA_SAGDP2N_raw_2000_2023.json"
raw_path.write_text(json.dumps(obj,indent=2),encoding="utf-8")

res=obj["BEAAPI"]["Results"]
if isinstance(res,list): res=res[0]
data=res["Data"]
records=[]
for x in data:
    gf=re.sub(r"[^0-9]","",str(x.get("GeoFIPS","")))
    if len(gf)<2 or gf[:2] not in STATE_FIPS: continue
    try: y=int(x["TimePeriod"])
    except: continue
    if y not in YEARS: continue
    val=str(x.get("DataValue","")).replace(",","").strip()
    try: val=float(val)
    except: val=None
    records.append({"state":str(x.get("GeoName","")).strip(" *"),"state_fips":gf[:2],
      "year":y,"line_code":str(x.get("LineCode","")),"description":str(x.get("Description","")),
      "unit_mult":x.get("UNIT_MULT"),"value":val})

long=pd.DataFrame(records)
if long.empty: raise RuntimeError("No usable BEA SAGDP2N records")

labels=long[["line_code","description"]].drop_duplicates().sort_values("line_code")
labels.to_csv(OUT/"E5_SAGDP2N_line_labels.csv",index=False)

def choose(patterns, role):
    cand=labels.copy()
    mask=pd.Series(False,index=cand.index)
    for p in patterns: mask |= cand.description.str.contains(p,case=False,regex=True,na=False)
    cand=cand[mask]
    # manufacturing must be aggregate, not durable/nondurable subcomponents.
    if role=="manufacturing":
        cand=cand[~cand.description.str.contains("durable|nondurable",case=False,regex=True,na=False)]
    if len(cand)!=1:
        raise RuntimeError(f"Ambiguous {role} line; candidates="+cand.to_json(orient="records"))
    return str(cand.iloc[0].line_code), str(cand.iloc[0].description)

all_code,all_label=choose([r"^all industry",r"^all-industry"],"all_industry")
mfg_code,mfg_label=choose([r"^manufacturing\b"],"manufacturing")
sel=long[long.line_code.isin([all_code,mfg_code])].copy()
wide=sel.pivot(index=["state","state_fips","year"],columns="line_code",values="value").reset_index()
wide=wide.rename(columns={all_code:"all_industry_gdp_current",mfg_code:"manufacturing_va_current"})
wide["E5_MFG_VA_SHARE"]=100*wide["manufacturing_va_current"]/wide["all_industry_gdp_current"]
wide=wide.sort_values(["state_fips","year"])
wide["E5_MFG_VA_SHARE_D1"]=wide.groupby("state_fips").E5_MFG_VA_SHARE.diff(1)
wide["E5_MFG_VA_SHARE_D5"]=wide.groupby("state_fips").E5_MFG_VA_SHARE.diff(5)
base=wide[wide.year==2000].set_index("state_fips").E5_MFG_VA_SHARE
wide["E5_MFG_VA_SHARE_CUM2000"]=wide.E5_MFG_VA_SHARE-wide.state_fips.map(base)

if wide.duplicated(["state_fips","year"]).any(): raise RuntimeError("duplicate keys")
expected={(f,y) for f in STATE_FIPS for y in YEARS}
observed=set(map(tuple,wide[["state_fips","year"]].itertuples(index=False,name=None)))
if observed!=expected: raise RuntimeError(f"coverage {len(observed)}/1200, missing sample={list(expected-observed)[:20]}")
if wide.E5_MFG_VA_SHARE.isna().any(): raise RuntimeError("missing primary E5 share")\nif (wide.all_industry_gdp_current<=0).any(): raise RuntimeError("nonpositive all-industry current-dollar GDP")\nif ((wide.E5_MFG_VA_SHARE<0)|(wide.E5_MFG_VA_SHARE>100)).any(): raise RuntimeError("manufacturing share outside 0-100")\n# Both numerator and denominator must come from the exact same SAGDP2N response/vintage.\nif set(sel.unit_mult.dropna().astype(str).unique()) and len(set(sel.unit_mult.dropna().astype(str).unique()))!=1:\n    raise RuntimeError("numerator/denominator unit multiplier mismatch")
out=OUT/"E5_BEA_manufacturing_value_added_share_50states_2000_2023.csv"
wide.to_csv(out,index=False)
manifest={"source":"U.S. BEA Regional GDP by state/industry","table":"SAGDP2N",
 "all_industry_line":{"code":all_code,"label":all_label},
 "manufacturing_line":{"code":mfg_code,"label":mfg_label},
 "rows":len(wide),"states":wide.state_fips.nunique(),"years":[int(wide.year.min()),int(wide.year.max())],
 "no_interpolation":True,"raw_sha256":hashlib.sha256(raw_path.read_bytes()).hexdigest(),
 "csv_sha256":hashlib.sha256(out.read_bytes()).hexdigest()}
(OUT/"E5_BEA_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
print(json.dumps(manifest,indent=2))
