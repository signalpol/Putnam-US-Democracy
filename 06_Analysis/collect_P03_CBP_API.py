"""
P03 Civic & Social Organization Density — Census API route
Target: 50 states x 2000-2023.
Numerator: CBP establishments, NAICS 813410 Civic and Social Organizations.
Requires CENSUS_API_KEY. Population merge remains separate and provenance-preserving.
"""
import os, requests, pandas as pd

KEY=os.environ["CENSUS_API_KEY"]
FIPS=[f"{x:02d}" for x in [1,2,4,5,6,8,9,10,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56]]

def naics_field(year):
    if year <= 2002: return "NAICS1997"
    if year <= 2007: return "NAICS2002"
    if year <= 2011: return "NAICS2007"
    if year <= 2016: return "NAICS2012"
    return "NAICS2017"

out=[]
for year in range(2000,2024):
    nf=naics_field(year)
    url=f"https://api.census.gov/data/{year}/cbp"
    params={"get":"NAME,ESTAB","for":"state:*",nf:"813410","key":KEY}
    r=requests.get(url,params=params,timeout=120); r.raise_for_status()
    data=r.json(); hdr=data[0]
    for rec in data[1:]:
        d=dict(zip(hdr,rec))
        st=d["state"]
        if st in FIPS:
            out.append({"year":year,"state_fips":st,"state_name":d["NAME"],
                        "naics_field":nf,"naics":"813410",
                        "establishments":int(d["ESTAB"])})

df=pd.DataFrame(out)
assert len(df)==1200, f"Expected 1200 state-years, got {len(df)}"
assert not df.duplicated(["year","state_fips"]).any()
df.to_csv("P03_CBP_813410_establishments_2000_2023.csv",index=False)
print(df.shape)
