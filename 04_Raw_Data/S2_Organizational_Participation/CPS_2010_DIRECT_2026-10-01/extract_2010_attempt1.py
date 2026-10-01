"""2010-only direct S2 extraction. Census raw primary; API weighted-count QA."""
import collections,concurrent.futures,csv,datetime,decimal,gzip,hashlib,json,os,pathlib,sys,urllib.parse,urllib.request
D=decimal.Decimal;ROOT=pathlib.Path(__file__).resolve().parent
BASE='https://api.census.gov/data/2010/cps/civic/nov'
RAWURL='https://www2.census.gov/programs-surveys/cps/datasets/2010/supp/nov10pub_civic.dat.gz'
DOCURL='https://www2.census.gov/programs-surveys/cps/techdocs/cpsnov10c.pdf'
Q=['PEQ5'+c for c in 'ABCDE'];now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
RUN_ID='S2_2010_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
KEY=os.environ.get('CENSUS_API_KEY','')
log={'run_id':RUN_ID,'start_utc':now(),'year':2010,'code_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'inputs':{},'steps':[],'api_requests':[]}
checks=[]
def check(n,p,d):checks.append({'name':n,'pass':bool(p),'detail':d})
def write(name,rs):
 with (ROOT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
def api(m):
 query='tabulate=weight(PWNRWGT)&row+for&col+'+m+'&'+m+'=1,2&PRTAGE=18:90&PRSUPINT=1&PRPERTYP=2&for=state:*'
 clean=BASE+'?'+query;entry={'variable':m,'url_without_key':clean,'start_utc':now()}
 try:
  with urllib.request.urlopen(clean+'&key='+urllib.parse.quote(KEY),timeout=45) as r:b=r.read();status=r.status
  data=json.loads(b);assert isinstance(data,list) and len(data)>1
  (ROOT/('API_'+m+'.json')).write_bytes(b)
  entry.update(end_utc=now(),http_status=status,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
  return m,data,entry
 except Exception as e:raise RuntimeError(type(e).__name__+': '+str(e).replace(KEY,'REDACTED') if KEY else type(e).__name__+': API credential unavailable') from None
try:
 for n in ['nov10pub_civic.dat.gz','cpsnov10c.pdf','variables.json','verified_variables.json']:
  b=(ROOT/n).read_bytes();log['inputs'][n]={'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
 raw=ROOT/'nov10pub_civic.dat.gz';rs=[];lens=collections.Counter();total=0;personkeys=set();key_duplicates=0
 # Fixed positions verified from 2010 Attachment6/7. Four implied decimals on raw weights.
 with gzip.open(raw,'rt',encoding='ascii') as f:
  for line in f:
   s=line.rstrip('\r\n');lens[len(s)]+=1;total+=1
   assert len(s)==990
   age=int(s[121:123]);typ=int(s[160:162]);interview=int(s[978:980])
   if age<18 or typ!=2 or interview!=1:continue
   st=str(int(s[92:94]));mis=int(s[62:64]);w=D(s[980:990].strip())/D(10000)
   answers=[int(s[i:i+2]) for i in range(956,966,2)]
   assert all(v in [1,2,-1,-2,-3,-9] for v in answers)
   # Do not deduplicate identical response profiles; multiple distinct people can share them.
   rs.append({'state':st,'age':age,'type':typ,'interview':interview,'mis':mis,'w':w,'a':answers,'any':1 if 1 in answers else 0 if answers==[2]*5 else None})
 check('full_raw_structure',total==152162 and dict(lens)=={990:152162},{'records':total,'record_lengths':dict(lens),'official_records':152162})
 metadata=json.loads((ROOT/'variables.json').read_text())['variables'];mapping=metadata['GESTFIPS']['values']['item'];states=set(mapping)-{'11'}
 groups=collections.defaultdict(list)
 for r in rs:groups[r['state']].append(r)
 check('all_51_geographies',set(groups)==set(mapping),'50 states+DC in eligible records')
 check('universe_verified',all(r['age']>=18 and r['type']==2 and r['interview']==1 for r in rs) and set(r['mis'] for r in rs)==set(range(1,9)),{'age_min':18,'civilian':True,'supplement_interview':1,'MIS_counts':dict(collections.Counter(r['mis'] for r in rs)),'outgoing_only':False,'proxy_allowed':True,'source':'Attachment1/3'})
 check('valid_group_variables_verified',all(q in metadata and metadata[q]['values']['item']['1']=='Yes' and metadata[q]['values']['item']['2']=='No' for q in Q),'2010 Attachment7/8 and API metadata: PEQ5A-E')
 check('weight_verified',metadata['PWNRWGT'].get('is-weight') and all(r['w']>0 for r in rs),'2010 Attachment3 instructs PWNRWGT; raw field 981-990 divided by10000; API reports person units')
 check('missing_rule_verified',all((r['any']==1)==(1 in r['a']) and (r['any']==0)==(r['a']==[2]*5) for r in rs),'Any Yes=>1; all five No=>0; otherwise missing, no negative recoding')
 def estimate(records,j):
  vals=[(r['any'] if j is None else 1 if r['a'][j]==1 else 0 if r['a'][j]==2 else None,r['w']) for r in records]
  yes=sum((w for v,w in vals if v==1 and w>0),D(0));no=sum((w for v,w in vals if v==0 and w>0),D(0));missing=sum((w for v,w in vals if v is None and w>0),D(0));den=yes+no
  return {'n_eligible':len(records),'n_unweighted':sum(v is not None and w>0 for v,w in vals),'n_yes':sum(v==1 and w>0 for v,w in vals),'n_no':sum(v==0 and w>0 for v,w in vals),'n_missing':sum(v is None for v,w in vals),'weighted_yes':str(yes),'weighted_no':str(no),'weighted_missing':str(missing),'weighted_denominator':str(den),'weighted_all_eligible':str(yes+no+missing),'proportion':str(yes/den)}
 details=[];canonical=[];dc=[]
 for st in sorted(groups,key=int):
  for j,m in [(None,'ANY')]+list(enumerate(Q)):
   e=estimate(groups[st],j);details.append({'state':mapping[st],'state_fips':st.zfill(2),'year':2010,'measure':m,**e})
   if j is None:
    row={'state':mapping[st],'state_fips':st.zfill(2),'year':2010,'s2_participation':e['proportion'],'s2_se':'','n_unweighted':e['n_unweighted'],'weighted_denominator':e['weighted_denominator'],'source':RAWURL,'weight':'PWNRWGT','observation_type':'DIRECT','run_id':RUN_ID,'unit':'proportion','se_method':'UNAVAILABLE_DESIGN_BASED','n_eligible':e['n_eligible'],'n_missing':e['n_missing']}
    (dc if st=='11' else canonical).append(row)
 write('S2_Organizational_Participation_2010_DIRECT_v1.csv',canonical);write('S2_2010_DC_QA_v1.csv',dc)
 write('S2_2010_ITEM_COUNTS_v1.csv',details)
 nat=[]
 for scope,records in [('US_50_PLUS_DC',rs),('US_50_ONLY',[r for r in rs if r['state']!='11'])]:
  for j,m in [(None,'ANY')]+list(enumerate(Q)):nat.append({'scope':scope,'year':2010,'measure':m,**estimate(records,j)})
 write('S2_2010_NATIONAL_QA_v1.csv',nat)
 check('50_states_exactly',len(canonical)==50,'canonical row count')
 check('DC_excluded',not any(r['state_fips']=='11' for r in canonical),'DC stored separately')
 check('duplicates_zero',len({r['state_fips'] for r in canonical})==len(canonical),'state-year duplicates=0')
 check('missing_state_estimate_zero',all(r['s2_participation']!='' for r in canonical),'all states have positive valid denominator')
 check('year_2010',all(r['year']==2010 for r in canonical),'no other year extraction')
 check('direct_observations_50',sum(r['observation_type']=='DIRECT' for r in canonical)==50,'all observations DIRECT')
 check('respondent_count_recorded',len(rs)==76084,{'respondents':len(rs),'published_Q5A_total':76084})
 check('weighted_denominators_recorded',all(D(r['weighted_denominator'])>0 for r in canonical),'state and item denominators preserved')
 check('partition',all(r['n_yes']+r['n_no']+r['n_missing']==r['n_eligible'] and D(r['weighted_yes'])+D(r['weighted_no'])==D(r['weighted_denominator']) for r in details),'valid plus missing partition, weights sum')
 check('range',all(0<=D(r['s2_participation'])<=1 for r in canonical),'proportions [0,1]')
 expected={1:11369,2:63408,-2:360,-3:816,-9:131};obs=dict(collections.Counter(r['a'][0] for r in rs))
 check('official_Q5A_frequencies',expected==obs,{'expected':expected,'observed':obs,'source':'Attachment13'})
 for j,target in [(None,229690000),(0,31295000),(2,21561000)]:
  val=sum((r['w'] for r in rs if j is None or r['a'][j]==1),D(0))
  check('official_benchmark_'+str(j),abs(val-D(target))<=500,{'observed':str(val),'published_rounded':target,'tolerance_persons':500,'source':'2010 Attachment16 Illustration3'})
 log['steps'].append({'stage':'direct_extraction','end_utc':now(),'respondents':len(rs),'canonical_rows':len(canonical),'status':'PASS'})
 if not KEY:raise RuntimeError('CENSUS_API_KEY is not set')
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  for m,tab,entry in pool.map(api,Q):
   log['api_requests'].append(entry);head=tab[0];idx=head.index('state');diff=[]
   for line in tab[1:]:
    st=str(int(line[idx]))
    if st not in mapping:
     assert all(D(str(line[j]))==0 for j,x in enumerate(head) if isinstance(x,dict));continue
    t=next(r for r in details if int(r['state_fips'])==int(st) and r['measure']==m)
    for j,x in enumerate(head):
     if isinstance(x,dict) and x.get(m) in ['1','2']:diff.append(abs(D(str(line[j]))-D(t['weighted_yes' if x[m]=='1' else 'weighted_no'])))
   check('raw_API_weighted_'+m,len(diff)==102 and max(diff)<=D('0.51'),{'cells':len(diff),'max_abs_difference':str(max(diff)) if diff else None,'tolerance_persons':'0.51'})
 check('SE_coverage_reported',all(r['s2_se']=='' and r['se_method']=='UNAVAILABLE_DESIGN_BASED' for r in canonical),'0/50. No 2010 Civic replicate series provided by consulted Census 2010 download page or API metadata; official generalized variance parameters preserved in source excerpts, but no unverified state-domain design formula used. No binomial SE substituted.')
 for name in ['no_interpolation','no_model_estimates','no_adjacent_year_substitution']:check(name,True,'2010 respondent microdata only; no other-year estimates used')
 log['steps'].append({'stage':'API_QA','end_utc':now(),'status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','checks_passed':sum(c['pass'] for c in checks),'checks_total':len(checks)})
 log['exit_code']=0 if all(c['pass'] for c in checks) else 3
except Exception as e:
 log['error']=(type(e).__name__+': '+str(e)).replace(KEY,'REDACTED') if KEY else type(e).__name__+': '+str(e);log['exit_code']=2
log['end_utc']=now();log['outputs']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.iterdir() if p.name.endswith('.csv') or p.name.startswith('API_')}
(ROOT/'QA_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
(ROOT/'S2_2010_RUN_LOG.txt').write_text(json.dumps(log,indent=2)+'\n')
print(json.dumps(log,indent=2));sys.exit(log['exit_code'])
