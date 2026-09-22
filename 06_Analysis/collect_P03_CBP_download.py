"""P03 downloader/parser using official Census CBP downloadable state files.
No Census API key required. Target 2000-2023, 50 states, NAICS 813410.
The parser detects year-specific column names from the downloaded CSV.
Population denominator is merged separately; raw establishment counts are preserved.
"""
import io, zipfile, requests, pandas as pd

YEARS=range(2000,2024)
STATE_FIPS={f"{x:02d}" for x in [1,2,4,5,6,8,9,10,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56]}

def state_zip_url(year):
    yy=str(year)[2:]
    return f"https://www2.census.gov/programs-surveys/cbp/datasets/{year}/cbp{yy}st.zip"

def read_state_file(year):
    r=requests.get(state_zip_url(year),timeout=180); r.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        names=[n for n in z.namelist() if n.lower().endswith((".txt",".csv"))]
        if len(names)!=1: raise RuntimeError(f"{year}: unexpected archive {z.namelist()}")
        return pd.read_csv(z.open(names[0]),dtype=str,encoding_errors="replace")

def pick(cols,*candidates):
    low={c.lower():c for c in cols}
    for x in candidates:
        if x.lower() in low:return low[x.lower()]
    raise KeyError(candidates)

rows=[]
for year in YEARS:
    df=read_state_file(year)
    st=pick(df.columns,"fipstate","fipsstate","state")
    estab=pick(df.columns,"est","estab")
    naics=[c for c in df.columns if c.lower().startswith("naics") and not c.lower().endswith("_ttl")]
    if len(naics)!=1: raise RuntimeError(f"{year}: NAICS columns={naics}")
    n=naics[0]
    x=df[df[st].str.zfill(2).isin(STATE_FIPS)].copy()
    x=x[x[n].astype(str).str.strip()=="813410"]
    # Where size/LFO dimensions exist, retain total rows only.
    for c in ["empszes","empflag","lfo"]:
        matches=[q for q in x.columns if q.lower()==c]
        if matches and c=="empszes": x=x[x[matches[0]].astype(str).str.zfill(3)=="001"]
        if matches and c=="lfo": x=x[x[matches[0]].astype(str).str.zfill(3)=="001"]
    if len(x)!=50: raise RuntimeError(f"{year}: expected 50 rows, got {len(x)}")
    for _,r in x.iterrows():
        rows.append({"year":year,"state_fips":str(r[st]).zfill(2),"naics":"813410",
                     "establishments":pd.to_numeric(r[estab],errors="raise"),
                     "source_url":state_zip_url(year)})
out=pd.DataFrame(rows)
assert len(out)==1200 and not out.duplicated(["year","state_fips"]).any()
out.to_csv("P03_CBP_813410_establishments_2000_2023.csv",index=False)
print("OK",out.shape)
