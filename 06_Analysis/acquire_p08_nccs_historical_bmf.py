#!/usr/bin/env python3
"""Acquire/aggregate Putnam P08 from NCCS harmonized historical BMF snapshots.
Downloads one selected snapshot per observed year, filters 501(c)(3), counts
unique EIN by 50 states. No interpolation; snapshot month is always retained.
Large raw BMF files are not committed to GitHub by this script.
"""
from pathlib import Path
import hashlib,json,requests
import pandas as pd

# Prefer a mid/late-year vintage when available; only catalog-verified vintages.
VINTAGES={
2000:"2000_05",2001:"2001_07",2002:"2002_07",2003:"2003_07",
2004:"2004_12",2005:"2005_07",2006:"2006_05",
2007:"2007_09",2008:"2008_06",2009:"2009_07",2010:"2010_07",2011:"2011_07",2012:"2012_07",
2013:"2013_07",2014:"2014_04",2015:"2015_12",2016:"2016_08",
2019:"2019_08",2020:"2020_04",2022:"2022_08",
2023:"2023_06"}
# Catalog-confirmed harmonized/transformed snapshots only.\n# 2017-09, 2017-12 and 2018-12 are explicitly known-bad upstream vintages in\n# current NCCS harmonization documentation and are excluded from canonical P08.
# Canonical NCCS catalog lists harmonized releases for 2007 and 2008; selected vintages above use them.
# No harmonized monthly release is listed for 2017 or 2021. Raw-archive-only 2017 releases are NOT silently mixed into the harmonized series.



STATE_ABBR={"AL":"01","AK":"02","AZ":"04","AR":"05","CA":"06","CO":"08","CT":"09","DE":"10","FL":"12","GA":"13","HI":"15","ID":"16","IL":"17","IN":"18","IA":"19","KS":"20","KY":"21","LA":"22","ME":"23","MD":"24","MA":"25","MI":"26","MN":"27","MS":"28","MO":"29","MT":"30","NE":"31","NV":"32","NH":"33","NJ":"34","NM":"35","NY":"36","NC":"37","ND":"38","OH":"39","OK":"40","OR":"41","PA":"42","RI":"44","SC":"45","SD":"46","TN":"47","TX":"48","UT":"49","VT":"50","VA":"51","WA":"53","WV":"54","WI":"55","WY":"56"}
BASE="https://nccsdata.s3.us-east-1.amazonaws.com"

def url_for(v):
    y=int(v[:4])
    if y>=2023:
        return f"{BASE}/processed/bmf/{v}/bmf_{v}_processed.csv"
    return f"{BASE}/processed/bmf-legacy/{v}/bmf_legacy_{v}_processed.csv"

def aggregate(v):
    url=url_for(v); seen={s:set() for s in STATE_ABBR}
    # Read only canonical identity/classification/geography columns in chunks.
    use=["ein","subsection_code","org_addr_state_raw"]
    try:
        it=pd.read_csv(url,usecols=use,dtype=str,chunksize=200000,low_memory=False)
    except Exception as e:
        raise RuntimeError(f"{v}: cannot open harmonized BMF {url}: {e}")
    n=0
    for ch in it:
        sub=ch["subsection_code"].astype(str).str.replace(r"\\.0$","",regex=True).str.zfill(2)
        z=ch[sub.eq("03")].copy()
        z["st"]=z["org_addr_state_raw"].astype(str).str.upper().str.strip()
        z=z[z.st.isin(STATE_ABBR)]
        for st,g in z.groupby("st"): seen[st].update(g["ein"].dropna().astype(str))
        n+=len(ch)
    rows=[{"year":int(v[:4]),"snapshot":v,"state":STATE_ABBR[st],"state_abbr":st,
           "P08_501c3_unique_ein_count":len(eins),"source_url":url} for st,eins in seen.items()]
    if len(rows)!=50: raise RuntimeError(f"{v}: state aggregation failure")
    return rows,n,url

if __name__=="__main__":
    allrows=[]; provenance=[]
    for year,v0 in sorted(VINTAGES.items()):
        v=v0.replace("_","-")
        rows,n,url=aggregate(v)
        allrows.extend(rows); provenance.append({"year":year,"snapshot":v,"source_url":url,"source_rows_scanned":n})
    x=pd.DataFrame(allrows)
    if x.duplicated(["year","state"]).any(): raise RuntimeError("duplicate observed state-year")
    out=Path("02_Putnam_14_Variables/P08"); out.mkdir(parents=True,exist_ok=True)
    p=out/"S1_P08_501c3_BMF_state_counts_observed_snapshots.csv"; x.to_csv(p,index=False)
    m={"construct":"unique 501(c)(3) EINs by state in observed NCCS harmonized/transformed BMF snapshot",
       "no_interpolation":True,"excluded_known_bad":["2017-09","2017-12","2018-12"],
       "observed_years":sorted(map(int,x.year.unique())),"rows":len(x),"provenance":provenance,
       "output_sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
    (out/"S1_P08_BMF_counts_manifest.json").write_text(json.dumps(m,indent=2),encoding="utf-8")
    print(json.dumps({"rows":len(x),"years":m["observed_years"],"sha256":m["output_sha256"]},indent=2))
