import gzip, io, os, urllib.request, csv, hashlib
YEARS={
2008:("https://www2.census.gov/programs-surveys/cps/datasets/2008/supp/nov08pub.dat.gz",[(973,974),(975,976),(977,978),(979,980),(981,982)],(1005,1014)),
2009:("https://www2.census.gov/programs-surveys/cps/datasets/2009/supp/nov09pub.dat.gz",[(957,958),(959,960),(961,962),(963,964),(965,966)],(981,990)),
2010:("https://www2.census.gov/programs-surveys/cps/datasets/2010/supp/nov10pub_civic.dat.gz",[(957,958),(959,960),(961,962),(963,964),(965,966)],(981,990)),
2011:("https://www2.census.gov/programs-surveys/cps/datasets/2011/supp/nov11pub.dat.gz",[(959,960),(961,962),(963,964),(965,966),(967,968)],(1007,1016)),
2013:("https://www2.census.gov/programs-surveys/cps/datasets/2013/supp/nov13pub.dat.gz",[(959,960),(961,962),(963,964),(965,966),(967,968)],(1003,1012)),
}
FIPS={1:"AL",2:"AK",4:"AZ",5:"AR",6:"CA",8:"CO",9:"CT",10:"DE",12:"FL",13:"GA",15:"HI",16:"ID",17:"IL",18:"IN",19:"IA",20:"KS",21:"KY",22:"LA",23:"ME",24:"MD",25:"MA",26:"MI",27:"MN",28:"MS",29:"MO",30:"MT",31:"NE",32:"NV",33:"NH",34:"NJ",35:"NM",36:"NY",37:"NC",38:"ND",39:"OH",40:"OK",41:"OR",42:"PA",44:"RI",45:"SC",46:"SD",47:"TN",48:"TX",49:"UT",50:"VT",51:"VA",53:"WA",54:"WV",55:"WI",56:"WY"}
def field(line,a,b):
    s=line[a-1:b].strip()
    try:return int(s)
    except:return None
os.makedirs("s2_out",exist_ok=True)
rows=[]; manifest=[]
for year,(url,items,wpos) in YEARS.items():
    print("download",year,url,flush=True)
    raw=urllib.request.urlopen(url,timeout=120).read()
    manifest.append((year,url,len(raw),hashlib.sha256(raw).hexdigest()))
    data=gzip.decompress(raw).decode("latin1").splitlines()
    agg={f:[0.0,0.0,0] for f in FIPS}
    for line in data:
        f=field(line,93,94)
        if f not in FIPS: continue
        vals=[field(line,a,b) for a,b in items]
        w=field(line,*wpos)
        if not w or w<=0: continue
        # Canonical valid denominator: all five organization items valid Yes/No.
        if not all(v in (1,2) for v in vals): continue
        y=1 if any(v==1 for v in vals) else 0
        agg[f][0]+=w*y; agg[f][1]+=w; agg[f][2]+=1
    for f,(num,den,n) in agg.items():
        if den<=0: raise RuntimeError(f"{year} {f} empty")
        rows.append({"year":year,"state_fips":f,"state_abbr":FIPS[f],"value":num/den,"percent":100*num/den,"n_unweighted":n,"weight":"PWNRWGT","status":"DIRECT_OBSERVED","source_url":url})
    nat_num=sum(x[0] for x in agg.values()); nat_den=sum(x[1] for x in agg.values())
    print("NATIONAL",year,100*nat_num/nat_den,"states",sum(1 for x in agg.values() if x[1]>0),flush=True)
with open("s2_out/S2_Organizational_Participation_CPS_2008_2013_DIRECT_v2.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
with open("s2_out/S2_SOURCE_SHA256_v2.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(["year","url","compressed_bytes","sha256"]); w.writerows(manifest)
assert len(rows)==250
assert len({(r["year"],r["state_fips"]) for r in rows})==250
assert all(0<=r["value"]<=1 for r in rows)
print("QA PASS rows=250")
