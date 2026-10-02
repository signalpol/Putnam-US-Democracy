import csv,io,json,zipfile,pathlib,urllib.request,concurrent.futures,hashlib
p=pathlib.Path(__file__).parent;raw=list(csv.DictReader((p/'inputs/S6_RAW.csv').open(encoding='utf-8-sig')));official={};out=[]
for y in range(2000,2024):
 z=zipfile.ZipFile(p/f'inputs/cbp_official/cbp{y%100:02d}st.zip')
 for r in csv.DictReader(io.StringIO(z.read(z.namelist()[0]).decode('utf-8-sig'))):
  r={k.lower():v for k,v in r.items()}
  if r['naics']=='813410' and r.get('lfo','-')=='-':official[y,r['fipstate']]=int(r['est'])
 api=json.loads((p/f'inputs/archive/CBP_{y}_NAICS813410_raw.json').read_text());h=api[0];rows=[dict(zip(h,r)) for r in api[1:]]
 a={r['state']:int(r['ESTAB']) for r in rows}
 for r in [r for r in raw if int(r['year'])==y]:
  v=int(r['S6_ESTAB']);o=official[y,r['state_fips']];av=a[r['state_fips']]
  out.append(dict(year=y,state_fips=r['state_fips'],inherited=v,official_zip=o,archived_api=av,match=(v==o==av)))
(p/'inputs/CBP_REVALIDATION.csv').write_text('');
with (p/'inputs/CBP_REVALIDATION.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
print('comparison',len(out),'matches',sum(x['match'] for x in out))
urls=[f'https://www.census.gov/naics/concordances/{a}_to_{b}_NAICS.{ext}' for a,b in [(2002,1997),(2007,2002),(2012,2007),(2017,2012)] for ext in ['xls','xlsx']]
def fetch(u):
 try:
  b=urllib.request.urlopen(u,timeout=25).read();n=u.split('/')[-1];(p/'inputs'/n).write_bytes(b);return dict(url=u,filename=n,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
 except Exception as e:return dict(url=u,error=str(e))
rs=list(concurrent.futures.ThreadPoolExecutor(8).map(fetch,urls));(p/'inputs/NAICS_ACQUISITION.json').write_text(json.dumps(rs,indent=2));print(json.dumps(rs))
