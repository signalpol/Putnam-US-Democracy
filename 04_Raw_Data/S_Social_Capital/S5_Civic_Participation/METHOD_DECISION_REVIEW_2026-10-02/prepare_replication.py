import pathlib,json,urllib.request,hashlib,shutil
R=pathlib.Path(__file__).resolve().parent
(R/'inputs').mkdir(exist_ok=True)
shutil.copy(R/'S5_ORIGINAL_RAW_UNCHANGED.csv',R/'inputs/raw.csv')
shutil.copy(R/'CEV_ARCHIVED_SOURCE.xlsx',R/'inputs/cev.xlsx')
for x in json.load(open(R/'HISTORICAL_RAW_DOWNLOAD_MANIFEST.json')):
 p=R/'historical_inputs'/x['relative_path'];p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists():p.write_bytes(urllib.request.urlopen(x['url'],timeout=180).read())
 assert p.stat().st_size==x['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==x['sha256']
for y in [2010,2011,2013]:shutil.copy(R/f'CENSUS_{y}_CODEBOOK.txt',R/'historical_inputs'/f'{y}_run/codebook.txt')
shutil.copy(R/'CENSUS_2011_API_VARIABLES.json',R/'historical_inputs/2011_run/variables.json')
print('Replication inputs ready; run python build_review.py')
