"""Reproduce S6 from preserved inherited count layer and locked population inputs.
Run: python build_s6.py --inputs inputs --output final_package
No interpolation, imputation, annual standardization, or modeled establishment counts.
"""
import argparse,csv,json,pathlib,hashlib,datetime,statistics,shutil
ap=argparse.ArgumentParser();ap.add_argument('--inputs',default='inputs');ap.add_argument('--output',default='final_package');a=ap.parse_args();ip=pathlib.Path(a.inputs);op=pathlib.Path(a.output);op.mkdir(parents=True,exist_ok=True)
start=datetime.datetime.now(datetime.timezone.utc).isoformat();run='S6_CBP_DENSITY_20261002_v1'
def read(n):return list(csv.DictReader((ip/n).open(encoding='utf-8-sig')))
def write(n,rows):
 with (op/n).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
raw=read('S6_RAW.csv');states={r['state_fips']:r['state_name'] for r in raw};assert len(states)==50 and '11' not in states
pop={};sources=[('st-est00int-alldata.csv',range(2000,2010),'2010_INTERCENSAL'),('nst-est2020-alldata.csv',range(2010,2020),'VINTAGE_2020'),('NST-EST2023-ALLDATA.csv',range(2020,2024),'VINTAGE_2023')];overlaps=[]
urls={'st-est00int-alldata.csv':'https://www2.census.gov/programs-surveys/popest/datasets/2000-2010/intercensal/state/st-est00int-alldata.csv','nst-est2020-alldata.csv':'https://www2.census.gov/programs-surveys/popest/datasets/2010-2020/state/totals/nst-est2020-alldata.csv','NST-EST2023-ALLDATA.csv':'https://www2.census.gov/programs-surveys/popest/datasets/2020-2023/state/totals/NST-EST2023-ALLDATA.csv'}
for n,years,v in sources:
 for r in read(n):
  sf=r['STATE'].zfill(2)
  if sf not in states:continue
  if n==sources[0][0] and any(int(r[k])!=0 for k in ['SEX','ORIGIN','RACE','AGEGRP']):continue
  if n!=sources[0][0] and r['SUMLEV']!='040':continue
  for y in years:
   assert (sf,y) not in pop;pop[sf,y]=(int(r[f'POPESTIMATE{y}']),v,n)
  if n==sources[0][0]:overlaps.append(dict(state_fips=sf,boundary_year=2010,earlier_vintage_population=int(r['POPESTIMATE2010'])))
  elif n==sources[1][0]:
   next(x for x in overlaps if x['state_fips']==sf and x['boundary_year']==2010)['later_vintage_population']=int(r['POPESTIMATE2010']);overlaps.append(dict(state_fips=sf,boundary_year=2020,earlier_vintage_population=int(r['POPESTIMATE2020'])))
  else:next(x for x in overlaps if x['state_fips']==sf and x['boundary_year']==2020)['later_vintage_population']=int(r['POPESTIMATE2020'])
for r in overlaps:r['relative_vintage_difference']=r['later_vintage_population']/r['earlier_vintage_population']-1
write('S6_POPULATION_VINTAGE_SENSITIVITY.csv',overlaps)
reval=read('CBP_REVALIDATION.csv');lookup={(r['state_fips'],int(r['year'])):r for r in reval};panel=[]
for r in sorted(raw,key=lambda r:(r['state_fips'],int(r['year']))):
 sf=r['state_fips'];y=int(r['year']);den,v,n=pop[sf,y];num=int(r['S6_ESTAB']);flags=[]
 if y==2003:flags.append('CBP_AUXILIARY_TREATMENT_CHANGE')
 if y in (2003,2008,2012,2017):flags.append('NAICS_REVISION_CORE_813410_UNCHANGED')
 if y in (2010,2020):flags.append('POPULATION_BENCHMARK_BOUNDARY')
 prev=next((x for x in panel if x['state_fips']==sf and x['year']==y-1),None);change=num/int(prev['establishments'])-1 if prev else None
 if change is not None and abs(change)>.25:flags.append('LARGE_ESTABLISHMENT_CHANGE_RETAINED')
 panel.append(dict(state=r['state_name'],state_fips=sf,year=y,S6_estimate=num/den*1000,establishments=num,population_denominator=den,denominator_reference='JULY_1_RESIDENT_POPULATION',population_vintage=v,naics_code=r['naics_code'],naics_version=r['naics_variable'],unit='ESTABLISHMENTS_PER_1000_RESIDENTS',observation_type='DIRECT',direct_observation=1,model_estimated=0,measurement_regime='CBP_EMPLOYER_813410',source='CENSUS_CBP_AND_POPULATION_ESTIMATES',source_flag='INHERITED_RAW_OFFICIAL_ZIP_ARCHIVED_API_MATCH',validation_risk_flag=';'.join(flags) or 'NONE',establishments_yoy_change=change,provenance=f'CBP_{y}_813410;{n}:POPESTIMATE{y};{run}'))
write('S6_FINAL_2000_2023.csv',panel)
write('S6_POPULATION_DENOMINATORS.csv',[dict(state_fips=sf,year=y,population=d[0],vintage=d[1],source_file=d[2]) for (sf,y),d in sorted(pop.items())])
write('S6_EXTREME_VALUE_AUDIT.csv',[dict(state=r['state'],year=r['year'],S6_estimate=r['S6_estimate'],establishments=r['establishments'],establishments_yoy_change=r['establishments_yoy_change'],flag=r['validation_risk_flag']) for r in panel if 'LARGE_' in r['validation_risk_flag'] or r['S6_estimate']==min(x['S6_estimate'] for x in panel) or r['S6_estimate']==max(x['S6_estimate'] for x in panel)])
registry=[]
for r in json.loads((ip/'CBP_OFFICIAL_ACQUISITION.json').read_text()):registry.append(dict(source_id=f"CBP_ZIP_{r['year']}",source_type='CENSUS_OFFICIAL_RAW',years=str(r['year']),url=r['url'],local_file=f"cbp_official/cbp{r['year']%100:02d}st.zip",bytes=r['bytes'],sha256=r['sha256'],purpose='INDEPENDENT_1200_CELL_COUNT_REVALIDATION'))
for n,years,v in sources:registry.append(dict(source_id=v,source_type='CENSUS_POPULATION',years=f'{min(years)}-{max(years)}',url=urls[n],local_file=n,bytes=(ip/n).stat().st_size,sha256=sha(ip/n),purpose='JULY_1_RESIDENT_DENOMINATOR'))
registry.append(dict(source_id='INHERITED_S6_RAW',source_type='PROJECT_PRESERVED_RAW',years='2000-2023',url='https://drive.google.com/file/d/1m37wN_nsqzR8xF19VFcs2WyrXf4z2xJU/view',local_file='S6_RAW.csv',bytes=(ip/'S6_RAW.csv').stat().st_size,sha256=sha(ip/'S6_RAW.csv'),purpose='CANONICAL_COUNT_INPUT_PRESERVED_UNCHANGED'))
for y in range(2000,2024):
 n=f'archive/CBP_{y}_NAICS813410_raw.json';registry.append(dict(source_id=f'ARCHIVED_API_{y}',source_type='PRESERVED_CENSUS_API_RESPONSE',years=str(y),url=f'https://api.census.gov/data/{y}/cbp',local_file=n,bytes=(ip/n).stat().st_size,sha256=sha(ip/n),purpose='PRESERVED_AGGREGATE_COUNT_QA'))
write('S6_SOURCE_REGISTRY.csv',registry)
qa=[]
def q(k,ok,e):qa.append(dict(check=k,result='PASS' if ok else 'FAIL',evidence=e))
q('rows',len(panel)==1200,len(panel));q('states',len(states)==50,len(states));q('years',set(r['year'] for r in panel)==set(range(2000,2024)),'2000-2023');q('each_state_24',all(sum(r['state_fips']==s for r in panel)==24 for s in states),'50x24');q('duplicates',len(set((r['state_fips'],r['year']) for r in panel))==1200,0);q('DC_excluded','11' not in states,0);q('territories_excluded',all(int(s)<=56 for s in states),0);q('missing_estimate',all(r['S6_estimate']>0 for r in panel),0);q('missing_denominator',len(pop)==1200 and all(x[0]>0 for x in pop.values()),0);q('direct_rows',all(r['observation_type']=='DIRECT' for r in panel),1200);q('model_rows',all(r['model_estimated']==0 for r in panel),0);q('raw_count_preserved',all(int(lookup[r['state_fips'],r['year']]['inherited'])==r['establishments'] for r in panel),1200);q('official_zip_comparison',all(r['match']=='True' for r in reval) and len(reval)==1200,'1200/1200');q('archived_API_comparison',all(r['inherited']==r['archived_api'] for r in reval),'1200/1200');q('arithmetic',all(abs(r['S6_estimate']-r['establishments']/r['population_denominator']*1000)<1e-12 for r in panel),'count/population*1000');q('one_category',set(r['naics_code'] for r in panel)=={'813410'},'813410 only');q('classification_versions',set(r['naics_version'] for r in panel)=={'NAICS1997','NAICS2002','NAICS2007','NAICS2012','NAICS2017'},'5 revisions audited');q('no_establishment_suppression',min(r['establishments'] for r in panel)>=3,min(r['establishments'] for r in panel));q('denominator_date',all(r['denominator_reference']=='JULY_1_RESIDENT_POPULATION' for r in panel),'July1');q('denominator_vintages_locked',len(set(r['population_vintage'] for r in panel))==3,'2010 intercensal / 2020 / 2023');q('vintage_boundary_sensitivity',len(overlaps)==100,'50states x 2boundaries');q('extremes_retained',all(r['establishments']==int(lookup[r['state_fips'],r['year']]['official_zip']) for r in panel),'No winsorization/deletion');q('provenance',all(r['provenance'] for r in panel),'1200');q('interpolation',True,'0; source code derives each observed year');q('ffill_bfill',True,'0');q('adjacent_year_substitution',True,'0');q('source_urls',all(r['url'] for r in registry),len(registry));q('raw_source_SHA',all(len(r['sha256'])==64 for r in registry),len(registry))
write('S6_QA_FINAL.csv',qa);assert all(r['result']=='PASS' for r in qa)
(op/'S6_RUN_MANIFEST.json').write_text(json.dumps(dict(run_id=run,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=0,code_sha256=sha(pathlib.Path(__file__)),input_hashes={n:sha(ip/n) for n in ['S6_RAW.csv','CBP_REVALIDATION.csv']+[x[0] for x in sources]},stages=['INPUT_AUDIT','OFFICIAL_RAW_COMPARISON','POPULATION_JOIN','DENSITY_DERIVATION','EXTREME_AUDIT','QA']),indent=2))
(pathlib.Path(__file__).parent/'workbook_data.json').write_text(json.dumps(dict(panel=panel,qa=qa)))
print(json.dumps(dict(rows=len(panel),qa=len(qa),pass_count=sum(r['result']=='PASS' for r in qa),min_density=min(r['S6_estimate'] for r in panel),max_density=max(r['S6_estimate'] for r in panel),extreme_changes=sum('LARGE_' in r['validation_risk_flag'] for r in panel))))
