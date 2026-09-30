import gzip, os, urllib.request, csv, hashlib, re
YEARS={
2008:(["nov08pub_civic.dat.gz","nov08pub_civ.dat.gz","nov08pub.dat.gz"],[(973,974),(975,976),(977,978),(979,980),(981,982)],(1005,1014)),
2009:(["nov09pub_civic.dat.gz","nov09pub_civ.dat.gz","nov09pub.dat.gz"],[(957,958),(959,960),(961,962),(963,964),(965,966)],(981,990)),
2010:(["nov10pub_civic.dat.gz"],[(957,958),(959,960),(961,962),(963,964),(965,966)],(981,990)),
2011:(["nov11pub.dat.gz"],[(959,960),(961,962),(963,964),(965,966),(967,968)],(1007,1016)),
2013:(["nov13pub.dat.gz"],[(959,960),(961,962),(963,964),(965,966),(967,968)],(1003,1012))}
FIPS={1:"AL",2:"AK",4:"AZ",5:"AR",6:"CA",8:"CO",9:"CT",10:"DE",12:"FL",13:"GA",15:"HI",16:"ID",17:"IL",18:"IN",19:"IA",20:"KS",21:"KY",22:"LA",23:"ME",24:"MD",25:"MA",26:"MI",27:"MN",28:"MS",29:"MO",30:"MT",31:"NE",32:"NV",33:"NH",34:"NJ",35:"NM",36:"NY",37:"NC",38:"ND",39:"OH",40:"OK",41:"OR",42:"PA",44:"RI",45:"SC",46:"SD",47:"TN",48:"TX",49:"UT",50:"VT",51:"VA",53:"WA",54:"WV",55:"WI",56:"WY"}
def field(line,a,b):
 s=line[a-1:b].strip()
 try:return int(s)
 except:return None
def getraw(year,names):
 base=f"https://www2.census.gov/programs-surveys/cps/datasets/{year}/supp/"
 for name in names:
  try:
   u=base+name; print("TRY",u,flush=True)
   return u,urllib.request.urlopen(u,timeout=120).read()
  except Exception as e: print("FAIL",repr(e),flush=True)
 html=urllib.request.urlopen(base,timeout=60).read().decode("utf8","ignore")
 found=re.findall(r'href="([^"]*nov[^"]*\.dat\.gz)"',html,re.I)
 print("NOV_FILES",year,found,flush=True)
 for name in found:
  try:
   u=base+name; raw=urllib.request.urlopen(u,timeout=120).read()
   # civic files must be long enough to contain supplement locations
   first=gzip.decompress(raw).splitlines()[0]
   if len(first)>=max(p[1] for p in YEARS[year][1]+[YEARS[year][2]]):
    print("DISCOVERED",u,len(first),flush=True); return u,raw
  except Exception as e: print("DISCOVERY_FAIL",name,repr(e),flush=True)
 raise RuntimeError(f"No usable source for {year}")
os.makedirs("s2_out",exist_ok=True); rows=[]; manifest=[]
for year,(names,items,wpos) in YEARS.items():
 url,raw=getraw(year,names); manifest.append((year,url,len(raw),hashlib.sha256(raw).hexdigest()))
 lines=gzip.decompress(raw).decode("latin1").splitlines(); agg={f:[0.,0.,0] for f in FIPS}
 for line in lines:
  st=field(line,93,94)
  if st not in FIPS: continue
  vals=[field(line,a,b) for a,b in items]; w=field(line,*wpos)
  if not w or w<=0 or not all(v in (1,2) for v in vals): continue
  y=int(any(v==1 for v in vals)); agg[st][0]+=w*y; agg[st][1]+=w; agg[st][2]+=1
 for st,(num,den,n) in agg.items():
  if den<=0: raise RuntimeError(f"{year} {st} empty")
  rows.append(dict(year=year,state_fips=st,state_abbr=FIPS[st],value=num/den,percent=100*num/den,n_unweighted=n,weight="PWNRWGT",status="DIRECT_OBSERVED",source_url=url))
 natn=sum(v[0] for v in agg.values()); natd=sum(v[1] for v in agg.values())
 print("NATIONAL",year,100*natn/natd,"STATES",len(agg),flush=True)
with open("s2_out/S2_Organizational_Participation_CPS_2008_2013_DIRECT_v2.csv","w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
with open("s2_out/S2_SOURCE_SHA256_v2.csv","w",newline="") as f:
 w=csv.writer(f); w.writerow(["year","url","compressed_bytes","sha256"]); w.writerows(manifest)
assert len(rows)==250 and len({(r["year"],r["state_fips"]) for r in rows})==250
assert all(0<=r["value"]<=1 for r in rows)
print("QA PASS rows=250",flush=True)
