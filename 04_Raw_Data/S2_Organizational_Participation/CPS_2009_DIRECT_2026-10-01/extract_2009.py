"""Extract 2009 S2 from authenticated Census CPS Civic API. Secrets never logged."""
import collections,concurrent.futures,csv,datetime,decimal,hashlib,json,pathlib,sys,urllib.parse,urllib.request
D=decimal.Decimal
ROOT=pathlib.Path(__file__).resolve().parent
BASE='https://api.census.gov/data/2009/cps/civic/nov'
KEY=pathlib.Path('/tmp/s2-2009-private/key').read_text().strip()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
log={'run_id':'S2_2009_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'),'start_utc':now(),'code_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'year':2009,'source':BASE,'steps':[],'requests':[]}
Q=['PEQ5'+c for c in 'ABCDE']
def fetch(name,query):
 clean=BASE+'?'+query;entry={'name':name,'url_without_key':clean,'start_utc':now()}
 url=clean+'&key='+urllib.parse.quote(KEY)
 try:
  with urllib.request.urlopen(url,timeout=55) as r:b=r.read();entry['http_status']=r.status
  data=json.loads(b);assert isinstance(data,list) and len(data)>1
  (ROOT/(name+'.json')).write_bytes(b)
  entry.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),data_rows=len(data)-1,end_utc=now())
  return data,entry
 except Exception as e:raise RuntimeError(str(e).replace(KEY,'REDACTED')) from None
universe='&PRTAGE=18:90&HRMIS=4,8&PRSUPINT=1&PRPERTYP=2&for=state:*'
try:
 fields=['GESTFIPS','PRTAGE','HRMIS','PRSUPINT','PRPERTYP','PWNRWGT']+Q
 raw,entry=fetch('respondents_2009','get='+','.join(fields)+universe);log['requests'].append(entry)
 h=raw[0];records=[{k:r[h.index(k)] for k in fields} for r in raw[1:]]
 log['steps'].append({'stage':'acquisition','end_utc':now(),'records':len(records),'status':'PASS'})
 selected=json.loads((ROOT/'verified_variables.json').read_text());mapping=selected['GESTFIPS']['values']['item']
 states=set(mapping)-{'11'};assert len(states)==50
 groups=collections.defaultdict(list)
 for r in records:
  assert int(r['PRTAGE'])>=18 and r['HRMIS'] in ['4','8'] and r['PRSUPINT']=='1' and r['PRPERTYP']=='2'
  assert r['GESTFIPS'] in mapping
  r['weight']=D(r['PWNRWGT']);r['answers']=[int(r[q]) for q in Q]
  assert all(v in [1,2,-1,-2,-3,-9] for v in r['answers'])
  r['any']=1 if 1 in r['answers'] else 0 if all(v==2 for v in r['answers']) else None
  groups[r['GESTFIPS']].append(r)
 assert set(groups)==set(mapping)
 def summarize(rs,measure):
  if measure=='ANY':vals=[(r['any'],r['weight']) for r in rs]
  else:vals=[(1 if r[measure]=='1' else 0 if r[measure]=='2' else None,r['weight']) for r in rs]
  yes=sum((w for v,w in vals if v==1 and w>0),D(0));no=sum((w for v,w in vals if v==0 and w>0),D(0))
  missing=sum((w for v,w in vals if v is None and w>0),D(0));den=yes+no
  return {'measure':measure,'n_eligible':len(rs),'n_yes':sum(v==1 and w>0 for v,w in vals),'n_no':sum(v==0 and w>0 for v,w in vals),'n_missing':sum(v is None and w>0 for v,w in vals),'n_invalid_weight':sum(w<=0 for v,w in vals),'weighted_yes':str(yes),'weighted_no':str(no),'weighted_missing':str(missing),'weighted_valid_denominator':str(den),'weighted_all_eligible':str(yes+no+missing),'percent':str(100*yes/den),'unit':'percent'}
 rows=[]
 for st in sorted(groups,key=int):
  for m in ['ANY']+Q:rows.append({'year':2009,'state_fips':st.zfill(2),'state_abbr':mapping[st],**summarize(groups[st],m)})
 def write(name,rs):
  with (ROOT/name).open('w',newline='') as f:
   w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
 canonical=[{'S_variable':'S2','construct':'Organizational participation','year':2009,'state_abbr':r['state_abbr'],'measure':'any_group_participation','value':r['percent'],'unit':'percent','source':'Census CPS November 2009 Civic Engagement API','source_file':'respondents_2009.json','provenance_status':'DIRECT_ESTIMATE','harmonized':'False'} for r in rows if r['measure']=='ANY' and r['state_fips']!='11']
 write('S2_2009_50_STATES_DIRECT.csv',canonical)
 write('S2_2009_ITEM_COUNTS_50_STATES.csv',[r for r in rows if r['state_fips']!='11'])
 write('S2_2009_DC_QA.csv',[r for r in rows if r['state_fips']=='11'])
 national=[{'year':2009,'scope':scope,**summarize(rs,m)} for scope,rs in [('US_50_PLUS_DC',records),('US_50_ONLY',[r for r in records if r['GESTFIPS']!='11'])] for m in ['ANY']+Q]
 write('S2_2009_NATIONAL_QA.csv',national)
 checks=[]
 def check(name,passed,detail):checks.append({'name':name,'pass':bool(passed),'detail':detail})
 check('canonical_50_states_no_DC',len(canonical)==50 and len({r['state_abbr'] for r in canonical})==50 and not any(r['state_abbr']=='DC' for r in canonical),'50 unique states, 2009 only')
 check('eligible_universe',True,'All returned records age18+, MIS4/8, supplement interview1, civilian2')
 check('positive_weights',all(r['weight']>0 for r in records),'PWNRWGT supplied by API in person units, no scaling applied')
 check('item_code_domain',True,'Validated 1,2,-1,-2,-3,-9')
 check('denominator_partition',all(r['n_eligible']==r['n_yes']+r['n_no']+r['n_missing']+r['n_invalid_weight'] for r in rows),'Counts partition universe; missing never coded No')
 check('percent_range',all(D(0)<=D(r['percent'])<=100 for r in rows),'All valid-denominator percentages in [0,100]')
 observed=dict(collections.Counter(r['PEQ5A'] for r in records));expected={'1':3227,'2':17630,'-2':70,'-3':243,'-9':56}
 check('official_external_PEQ5A_frequency',observed==expected,{'observed':observed,'expected':expected,'source':'https://www2.census.gov/programs-surveys/cps/techdocs/cpsnov09c.pdf Attachment13'})
 total=sum((r['weight'] for r in records),D(0))
 check('official_external_population',abs(total-D(227346000))<=500,{'observed':str(total),'published_rounded':227346000,'source':'Census 2009 technical documentation Attachment16 Illustration3'})
 for m,target in [('PEQ5A',34266000),('PEQ5C',22134000)]:
  weighted=sum((r['weight'] for r in records if r[m]=='1'),D(0))
  check('official_external_yes_'+m,abs(weighted-D(target))<=500,{'computed':str(weighted),'published_rounded':target,'tolerance_rounding_persons':500,'denominator_note':'Published percentages use all-eligible; canonical item percentages exclude item missing.'})
 # Compare raw-record calculation with the Census server's weighted tabulations.
 def get_item(m):return m,fetch('server_'+m,'tabulate=weight(PWNRWGT)&row+for&col+'+m+'&'+m+'=1,2'+universe)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  for m,(tab,entry) in pool.map(get_item,Q):
   log['requests'].append(entry)
   headers=tab[0];diff=[]
   state_index=next(i for i,x in enumerate(headers) if x=='state' or x=='GESTFIPS')
   for line in tab[1:]:
    st=str(int(line[state_index]))
    if st not in mapping:
     assert all(D(str(line[j]))==0 for j,col in enumerate(headers) if isinstance(col,dict)), 'Nonzero unexpected territory'
     continue
    target=next(r for r in rows if int(r['state_fips'])==int(st) and r['measure']==m)
    for j,col in enumerate(headers):
     if isinstance(col,dict) and col.get(m) in ['1','2']:
      local=D(target['weighted_yes' if col[m]=='1' else 'weighted_no']);remote=D(str(line[j]));diff.append(abs(local-remote))
   check('server_weighted_'+m,len(diff)==102 and max(diff)<=D('0.51'),{'compared_cells':len(diff),'max_abs_difference':str(max(diff)) if diff else None,'tolerance':'0.51 persons for API rounded counts'})
 # Union counts use joint respondent answers rather than summing marginal percentages.
 check('union_count_bounds',all(max(sum(r['weight'] for r in rs if r[m]=='1') for m in Q)<=sum(r['weight'] for r in rs if r['any']==1)<=sum(sum(r['weight'] for r in rs if r[m]=='1') for m in Q) for rs in groups.values()),'Weighted union between largest marginal Yes count and sum of marginal Yes counts')
 qa={'checks':checks,'pass':all(x['pass'] for x in checks),'external_union_percent_benchmark':'UNAVAILABLE; no same-year same-denominator independent union estimate verified','external_benchmark_scope':'Official published population, school and sports Yes totals and school frequencies verified; pooled Opportunity Index rejected','missing_rule':'Any Yes => 1, all No => 0, otherwise missing; unknown answers not individually imputed.'}
 (ROOT/'QA.json').write_text(json.dumps(qa,indent=2)+'\n')
 log['steps'].append({'stage':'estimate_and_QA','end_utc':now(),'status':'PASS' if qa['pass'] else 'FAILED','checks_passed':sum(x['pass'] for x in checks),'checks_total':len(checks),'canonical_rows':len(canonical)})
 log['exit_code']=0 if qa['pass'] else 3
except Exception as e:
 log['error']=(type(e).__name__+': '+str(e)).replace(KEY,'REDACTED');log['exit_code']=2
log['end_utc']=now()
log['outputs']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.iterdir() if p.name.startswith(('S2_2009_','server_')) or p.name=='QA.json'}
(ROOT/'authenticated_execution_log.json').write_text(json.dumps(log,indent=2)+'\n')
print(json.dumps(log,indent=2));sys.exit(log['exit_code'])
