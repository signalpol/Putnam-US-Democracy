"""Build P03 density after CBP establishments are collected.
Denominator: Census resident population estimate for each state/year.
2000-2009: 2000-2010 intercensal characteristics file, total demographic row only.
2010-2020: Vintage 2020 state totals.
2021-2023: Vintage 2023 state totals.
Density = NAICS 813410 establishments / resident population * 1,000.
No interpolation.
"""
import pandas as pd, requests, io

FIPS={1,2,4,5,6,8,9,10,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56}
URL00="https://www2.census.gov/programs-surveys/popest/datasets/2000-2010/intercensal/state/st-est00int-alldata.csv"
URL20="https://www2.census.gov/programs-surveys/popest/datasets/2010-2020/state/totals/nst-est2020-alldata.csv"
URL23="https://www2.census.gov/programs-surveys/popest/datasets/2020-2023/state/totals/NST-EST2023-ALLDATA.csv"

def read_csv(url):
    r=requests.get(url,timeout=180); r.raise_for_status()
    return pd.read_csv(io.BytesIO(r.content))

def population_panel():
    out=[]
    a=read_csv(URL00)
    # File layout: total resident population is SEX=0, ORIGIN=0, RACE=0, AGEGRP=0.
    a=a[(a.STATE.isin(FIPS))&(a.SEX==0)&(a.ORIGIN==0)&(a.RACE==0)&(a.AGEGRP==0)]
    assert len(a)==50
    for y in range(2000,2010):
        for _,r in a.iterrows(): out.append((y,int(r.STATE),r.NAME,int(r[f"POPESTIMATE{y}"]),URL00))
    b=read_csv(URL20)
    b=b[b.STATE.isin(FIPS)]
    assert len(b)==50
    for y in range(2010,2021):
        for _,r in b.iterrows(): out.append((y,int(r.STATE),r.NAME,int(r[f"POPESTIMATE{y}"]),URL20))
    c=read_csv(URL23)
    c=c[c.STATE.isin(FIPS)]
    assert len(c)==50
    for y in range(2021,2024):
        for _,r in c.iterrows(): out.append((y,int(r.STATE),r.NAME,int(r[f"POPESTIMATE{y}"]),URL23))
    p=pd.DataFrame(out,columns=["year","state_fips","state_name","population","population_source"])
    assert len(p)==1200 and not p.duplicated(["year","state_fips"]).any()
    return p

def build(establishment_csv):
    e=pd.read_csv(establishment_csv,dtype={"state_fips":int})
    p=population_panel()
    z=e.merge(p,on=["year","state_fips"],how="validate",validate="one_to_one")
    assert len(z)==1200
    z["p03_density_per_1000"]=z["establishments"]/z["population"]*1000
    z["variable_id"]="P03"
    z["proxy_flag"]="PUTNAM_COMPATIBLE_ADMIN_REPLICATION"
    z["no_interpolation"]=True
    return z

if __name__=="__main__":
    z=build("P03_CBP_813410_establishments_2000_2023.csv")
    z.to_csv("P03_Civic_Social_Organization_Density_2000_2023.csv",index=False)
    print("OK",z.shape)
