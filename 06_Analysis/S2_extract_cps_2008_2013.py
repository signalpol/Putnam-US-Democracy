import io, os, urllib.request, csv, hashlib, zipfile
SRC={
2008:(["https://data.nber.org/cps/cpsnov08c.zip"],[(973,974),(975,976),(977,978),(979,980),(981,982)],(1005,1014)),
2009:(["https://www.icpsr.umich.edu/web/ICPSR/studies/29881/datasets/1/download/zip"],[(957,958),(959,960),(961,962),(963,964),(965,966)],(981,990)),
2010:(["https://www2.census.gov/programs-surveys/cps/datasets/2010/supp/nov10pub_civic.zip","https://www2.census.gov/programs-surveys/cps/datasets/2010/supp/nov10pub.zip"],[(957,958),(959,960),(961,962),(963,964),(965,966)],(981,990)),
2011:(["https://www2.census.gov/programs-surveys/cps/datasets/2011/supp/nov11pub.zip"],[(959,960),(961,962),(963,964),(965,966),(967,968)],(1007,1016)),
2013:(["https://www2.census.gov/programs-surveys/cps/datasets/2013/supp/nov13pub.zip"],[(959,960),(961,962),(963,964),(965,966),(967,968)],(1003,1012))}
FIPS={1:"AL",2:"AK",4:"AZ",5:"AR",6:"CA",8:"CO",9:"CT",10:"DE",12:"FL",13:"GA",15:"HI",16:"ID",17:"IL",18:"IN",19:"IA",20:"KS",21:"KY",22:"LA",23:"ME",24:"MD",25:"MA",26:"MI",27:"MN",28:"MS",29:"MO",30:"MT",31:"NE",32:"NV",33:"NH",34:"NJ",35:"NM",36:"NY",37:"NC",38:"ND",39:"OH",40:"OK",41:"OR",42:"PA",44:"RI",45:"SC",46:"SD",47:"TN",48:"TX",49:"UT",50:"VT",51:"VA",53:"WA",54:"WV",55:"WI",56:"WY"}
def fld(s,a,b):
 try:return int(s[a-1:b].strip())
 except:return None
def fetchzip(urls):
 last=None
 for u in urls:
  try:
   print("FETCH",u,flush=True); b=urllib.request.urlopen(u,timeout=180).read()
   z=zipfile.ZipFile(io.BytesIO(b)); files=[x for x in z.infolist() if not x.is_dir()]
   cand=max(files,key=lambda x:x.file_size)
   data=z.read(cand).decode("latin1").splitlines()
   print("ZIP_OK",u,cand.filename,cand.file_size,"recordlen",len(data[0]),flush=True)
   return u,b,data
  except Exception as e: last=e; print("FETCH_FAIL",u,repr(e),flush=True)
 raise RuntimeError(repr(last))
os.makedirs("s2_out",exist_ok=True); rows=[]; man=[]
for year,(urls,items,wpos) in SRC.items():
 url,blob,lines=fetchzip(urls); man.append((year,url,len(blob),hashlib.sha256(blob).hexdigest()))
 agg={f:[0.,0.,0] for f in FIPS}
 for line in lines:
  st=fld(line,93,94)
  if st not in FIPS: continue
  vals=[fld(line,a,b) for a,b in items]; wt=fld(line,*wpos)
  if not wt or wt<=0 or not all(v in (1,2) for v in vals): continue
  y=int(any(v==1 for v in vals)); agg[st][0]+=wt*y; agg[st][1]+=wt; agg[st][2]+=1
 for st,(num,den,n) in agg.items():
  if den<=0: raise RuntimeError(f"{year} state {st} empty")
  rows.append(dict(year=year,state_fips=st,state_abbr=FIPS[st],value=num/den,percent=100*num/den,n_unweighted=n,weight="PWNRWGT",status="DIRECT_OBSERVED",source_url=url))
 natn=sum(v[0] for v in agg.values()); natd=sum(v[1] for v in agg.values())
 print("NATIONAL",year,round(100*natn/natd,4),"STATES",sum(v[1]>0 for v in agg.values()),flush=True)
with open("s2_out/S2_Organizational_Participation_CPS_2008_2013_DIRECT_v2.csv","w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
with open("s2_out/S2_SOURCE_SHA256_v2.csv","w",newline="") as f:
 w=csv.writer(f); w.writerow(["year","url","compressed_bytes","sha256"]); w.writerows(man)
assert len(rows)==250 and len({(r["year"],r["state_fips"]) for r in rows})==250
assert all(0<=r["value"]<=1 for r in rows)
print("QA PASS rows=250",flush=True)
