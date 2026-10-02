"""Optional independent official-source replay; preserves primary inherited RAW."""
import pathlib,json,urllib.request,hashlib,concurrent.futures
p=pathlib.Path(__file__).parent/'inputs';m=json.loads((p/'CBP_OFFICIAL_ACQUISITION.json').read_text())
def acquire(r):
 n=p/f"cbp_official/cbp{r['year']%100:02d}st.zip";n.parent.mkdir(exist_ok=True)
 if not n.exists():n.write_bytes(urllib.request.urlopen(r['url'],timeout=120).read())
 digest=hashlib.sha256(n.read_bytes()).hexdigest()
 if digest!=r['sha256']:raise ValueError(f"Official source revision/hash mismatch {r['year']}; do not silently replace vintage")
 return r['year']
print('Verified official years:',list(concurrent.futures.ThreadPoolExecutor(4).map(acquire,m)))
print('Run audit_sources.py with this package as its directory to compare all1,200 counts.')
