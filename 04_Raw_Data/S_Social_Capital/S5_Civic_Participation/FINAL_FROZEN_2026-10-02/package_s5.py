import pathlib,shutil,hashlib,json,zipfile
R=pathlib.Path(__file__).resolve().parent
P=R/'final_package'
for n in ['build_workbook.mjs','verify_freeze.py','package_s5.py','replication_results.json']:
 shutil.copy2(R/n,P/n)
for p in P.glob('*.inspect.ndjson'):p.unlink()
files=sorted(p for p in P.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt')
(P/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(P).as_posix()+'\n' for p in files))
z=R/'S5_FINAL_FROZEN_2026-10-02.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as f:
 for p in sorted(P.rglob('*')):
  if p.is_file():f.write(p,p.relative_to(P).as_posix())
upload=[p for p in sorted(P.iterdir()) if p.is_file()]+[z]
manifest=[{'name':p.name,'path':str(p.resolve()),'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in upload]
(R/'upload_manifest.json').write_text(json.dumps(manifest,indent=2))
with zipfile.ZipFile(z) as f:
 for line in f.read('SHA256SUMS.txt').decode().splitlines():
  h,n=line.split('  ',1);assert hashlib.sha256(f.read(n)).hexdigest()==h
print(json.dumps({'payload_files':len(manifest),'zip_members':len(files)+1,'zip_size':z.stat().st_size,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest()}))
