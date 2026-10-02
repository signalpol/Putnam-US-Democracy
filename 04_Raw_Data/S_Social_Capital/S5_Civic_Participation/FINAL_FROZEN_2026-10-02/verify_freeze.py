import csv,json,hashlib,pathlib,shutil,zipfile
from openpyxl import load_workbook
R=pathlib.Path(__file__).resolve().parent
P=R/'final_package'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
panel=list(csv.DictReader((P/'S5_FINAL_2000_2023.csv').open()))
w=load_workbook(P/'S5_FINAL_2000_2023.xlsx',read_only=True,data_only=True)
rows=list(w['Canonical'].values); fields=rows[0]
assert len(rows)-1==1200
for expected,actual in zip(panel,rows[1:]):
 for k,v in zip(fields,actual):
  e=expected[k]
  if isinstance(v,(int,float)):assert abs(float(e)-v)<1e-12
  else:assert e==('' if v is None else v)
observed=list(csv.DictReader((P/'S5_DIRECT_OBSERVATIONS_FINAL.csv').open()))
rows=list(w['Observed items'].values); fields=rows[0]
assert len(rows)-1==2300
for expected,actual in zip(observed,rows[1:]):
 for k,v in zip(fields,actual):
  e=expected[k]
  if isinstance(v,(int,float)):assert abs(float(e)-v)<1e-12
  else:assert e==('' if v is None else v)
assert digest(P/'S5_DIRECT_OBSERVATIONS_FINAL.csv')=='3fa34e4f45b809dff94f542eb4c4948c700418d655dd72e54ae0be8098f60274'
checks=json.loads((R/'replication_results.json').read_text())
assert len(checks)==14 and all(x['match'] for x in checks)
(P/'S5_REPLICATION_VERIFICATION.json').write_text(json.dumps({'clean_rerun_csv_files':checks,'xlsx_canonical_cells_match':True,'xlsx_observed_cells_match':True,'observed_input_unchanged':True},indent=2))
qa=list(csv.DictReader((P/'S5_QA_FINAL.csv').open()))
extras=[('clean_numerical_rerun','14/14 CSV byte matches'),('observed_unchanged','Inherited observed SHA256 matches'),('xlsx_csv_comparison','1200 canonical + 2300 observed rows, all fields')]
for n,e in extras:
 if not any(x['check']==n for x in qa):qa.append({'check':n,'result':'PASS','evidence':e})
with (P/'S5_QA_FINAL.csv').open('w',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=['check','result','evidence']);writer.writeheader();writer.writerows(qa)
d=json.loads((R/'workbook_data.json').read_text());d['qa']=qa;(R/'workbook_data.json').write_text(json.dumps(d))
print(json.dumps({'QA':len(qa),'PASS':sum(x['result']=='PASS' for x in qa)}))
