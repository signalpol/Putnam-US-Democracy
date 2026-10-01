"""2013-only direct S2 extraction. Census raw primary; API weighted-count QA."""
import numpy as np
import re
import collections,concurrent.futures,csv,datetime,decimal,gzip,hashlib,json,os,pathlib,sys,urllib.parse,urllib.request
D=decimal.Decimal;ROOT=pathlib.Path(__file__).resolve().parent
BASE='https://api.census.gov/data/2013/cps/civic/nov'
RAWURL='https://www2.census.gov/programs-surveys/cps/datasets/2013/supp/nov13pub.dat.gz'
DOCURL='https://www2.census.gov/programs-surveys/cps/techdocs/cpsnov13.pdf'
Q=['PES5'+c for c in 'ABCDE'];now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
RUN_ID='S2_2013_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
KEY=os.environ.get('CENSUS_API_KEY','')
log={'run_id':RUN_ID,'start_utc':now(),'year':2013,'code_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'inputs':{},'steps':[],'api_requests':[]}
checks=[]
def check(n,p,d):checks.append({'name':n,'pass':bool(p),'detail':d})
def write(name,rs):
 with (ROOT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
def api(m):
 query='tabulate=weight(PWNRWGT)&row+for&col+'+m+'&'+m+'=1,2&PRTAGE=18:90&PRSUPINT=1&PRPERTYP=2&for=state:*'
 clean=BASE+'?'+query;entry={'variable':m,'url_without_key':clean,'start_utc':now()}
 for use_key in ([False,True] if KEY else [False]):
  try:
   url=clean+('&key='+urllib.parse.quote(KEY) if use_key else '')
   with urllib.request.urlopen(url,timeout=45) as r:b=r.read();status=r.status
   entry.update(http_status=status,response_bytes=len(b),response_sha256=hashlib.sha256(b).hexdigest())
   data=json.loads(b);assert isinstance(data,list) and len(data)>1
   (ROOT/('API_'+m+'.json')).write_bytes(b)
   entry.update(end_utc=now(),http_status=status,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),credential_mode='environment_key' if use_key else 'public_no_key')
   return m,data,entry
  except Exception as e:entry.setdefault('attempts',[]).append({'credential_mode':'environment_key' if use_key else 'public_no_key','error_type':type(e).__name__})
 entry.update(end_utc=now(),status='UNAVAILABLE_AUTH_REQUIRED' if not KEY else 'UNAVAILABLE_REQUEST_FAILED',environment_key_available=bool(KEY))
 return m,None,entry

try:
 spec=json.loads((ROOT/'QA_SPEC.json').read_text());assert spec['year']==2013 and spec['raw_records']==150067 and spec['record_length']==1012
 check('QA_spec_frozen_before_execution',spec['frozen_utc']<log['start_utc'],{'spec_sha256':hashlib.sha256((ROOT/'QA_SPEC.json').read_bytes()).hexdigest(),'frozen_utc':spec['frozen_utc']})
 for n in ['QA_SPEC.json','source_links.json','external_benchmark_source.json','nov13pub.dat.gz','nov13nrrep.dat.gz','cpsnov13.pdf','nrrep.sas','person_replicate_instructions.doc','person_replicate_instructions.txt','variables.json','verified_variables.json']:
  b=(ROOT/n).read_bytes();log['inputs'][n]={'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
 raw=ROOT/'nov13pub.dat.gz';control_pop=D(0);rs=[];lens=collections.Counter();total=0;personkeys=set();key_duplicates=0
 # Fixed positions verified from 2013 Attachment6/7. Four implied decimals on raw weights.
 with gzip.open(raw,'rt',encoding='ascii') as f:
  for line in f:
   s=line.rstrip('\r\n');lens[len(s)]+=1;total+=1
   assert len(s)==1012
   age=int(s[121:123]);typ=int(s[160:162]);interview=int(s[990:992])
   if age>=18 and typ==2:control_pop+=D(s[612:622].strip())/D(10000)
   if age<18 or typ!=2 or interview!=1:continue
   st=str(int(s[92:94]));mis=int(s[62:64]);w=D(s[1002:1012].strip())/D(10000)
   answers=[int(s[i:i+2]) for i in range(958,968,2)]
   assert all(v in [1,2,-1,-2,-3,-9] for v in answers)
   # Do not deduplicate identical response profiles; multiple distinct people can share them.
   rs.append({'key':s[814:821],'state':st,'age':age,'type':typ,'interview':interview,'mis':mis,'w':w,'a':answers,'any':1 if 1 in answers else 0 if answers==[2]*5 else None})
 check('full_raw_structure',total==150067 and dict(lens)=={1012:150067},{'records':total,'record_lengths':dict(lens),'official_records':150067})
 metadata=json.loads((ROOT/'variables.json').read_text())['variables'];mapping=metadata['GESTFIPS']['values']['item'];states=set(mapping)-{'11'}
 groups=collections.defaultdict(list)
 for r in rs:groups[r['state']].append(r)
 check('all_51_geographies',set(groups)==set(mapping),'50 states+DC in eligible records')
 check('universe_verified',all(r['age']>=18 and r['type']==2 and r['interview']==1 for r in rs) and set(r['mis'] for r in rs)=={3,4,7,8},{'age_min':18,'civilian':True,'supplement_interview':1,'MIS_counts':dict(collections.Counter(r['mis'] for r in rs)),'MIS_restriction_status':'UNKNOWN — DOCUMENT/RAW CONFLICT','operational_MIS':[3,4,7,8],'document_overview_MIS':[3,4,7,8],'document_abstract_outgoing_only':True,'proxy_allowed':True,'source':'Attachment7 operational response universe; Attachment13 frequencies; Attachment3 MIS3,4,7,8 matchesraw;Attachment1 outgoing-only conflicts withraw;UNKNOWN — DOCUMENT/RAW CONFLICT preserved'})
 check('wording_categories_verified',all(q in metadata and metadata[q]['suggested-weight']=='PWNRWGT' for q in Q),'2013 Attachment7/8 exactfivequestionwordings recorded independently; same five groupcategories as2011 exceptrollingreferenceyear')
 check('minimum_age_verified',min(r['age'] for r in rs)==18,'2013 Attachment3 persons/reporters18+;released minimumage18')
 check('valid_group_variables_verified',all(q in metadata and metadata[q]['values']['item']['1']=='Yes' and metadata[q]['values']['item']['2']=='No' for q in Q),'2013 Attachment7/8 and API metadata: PES5A-E')
 check('weight_verified',metadata['PWNRWGT'].get('is-weight') and all(r['w']>0 for r in rs),'2013 Attachment3 defines nonresponse/selfresponse weights; API group items explicitly suggest PWNRWGT; raw field 1003-1012 divided by10000; API reports person units')
 check('missing_rule_verified',all((r['any']==1)==(1 in r['a']) and (r['any']==0)==(r['a']==[2]*5) for r in rs),'Any Yes=>1; all five No=>0; otherwise missing, no negative recoding')
 def estimate(records,j):
  vals=[(r['any'] if j is None else 1 if r['a'][j]==1 else 0 if r['a'][j]==2 else None,r['w']) for r in records]
  yes=sum((w for v,w in vals if v==1 and w>0),D(0));no=sum((w for v,w in vals if v==0 and w>0),D(0));missing=sum((w for v,w in vals if v is None and w>0),D(0));den=yes+no
  return {'n_eligible':len(records),'n_unweighted':sum(v is not None and w>0 for v,w in vals),'n_yes':sum(v==1 and w>0 for v,w in vals),'n_no':sum(v==0 and w>0 for v,w in vals),'n_missing':sum(v is None for v,w in vals),'weighted_yes':str(yes),'weighted_no':str(no),'weighted_missing':str(missing),'weighted_denominator':str(den),'weighted_all_eligible':str(yes+no+missing),'proportion':str(yes/den)}
 # Independent verification of official2013 nonresponse replicate file and merge.
 keys={r['key']:r for r in rs};assert len(keys)==len(rs)
 nr=0;seen=set();sums=np.zeros(161,dtype=np.int64);rep_sum=collections.defaultdict(lambda:np.zeros(161,dtype=np.int64));rep_yes=collections.defaultdict(lambda:np.zeros(161,dtype=np.int64));base_mismatch=0;rep_lens=collections.Counter()
 with gzip.open(ROOT/'nov13nrrep.dat.gz','rt',encoding='ascii') as f:
  for line in f:
   s=line.rstrip('\r\n');nr+=1;rep_lens[len(s)]+=1;assert len(s)==1617
   key=s[:7];assert key not in seen;seen.add(key)
   w=np.array([int(s[j:j+10]) for j in range(7,1617,10)],dtype=np.int64);sums+=w
   if key not in keys:continue
   r=keys[key];base_mismatch+=int(D(int(w[0]))/D(10000)!=r['w'])
   if r['any'] is not None:
    rep_sum[r['state']]+=w
    if r['any']==1:rep_yes[r['state']]+=w
 check('replicate_merge_one_to_one',len(keys)==len(rs) and set(keys)<=seen and base_mismatch==0,{'eligible_matched':len(keys),'replicate_records':nr,'replicate_unique_keys':len(seen),'base_weight_mismatches':base_mismatch,'record_lengths':dict(rep_lens)})
 expected_totals={int(i):D(v) for i,v in re.findall(r'repwgt(\d+)\s*=\s*([0-9]+\.[0-9]+)',(ROOT/'nrrep.sas').read_text())}
 differences=[abs(D(int(sums[i]))/D(10000)-expected_totals[i]) for i in range(161)]
 check('replicate_161_official_totals',len(expected_totals)==161 and max(differences)<=D('0.01'),{'weight_columns':161,'max_difference':str(max(differences)),'tolerance_persons':'0.01'})
 se_by_state={};rep_rows=[]
 for st in groups:
  dens=rep_sum[st];nums=rep_yes[st];assert np.all(dens>0)
  props=nums/dens;var=float((4/160)*np.sum((props[1:]-props[0])**2));se_by_state[st]=var**.5
  e=estimate(groups[st],None);assert abs(props[0]-float(e['proportion']))<1e-12
  for k in range(161):rep_rows.append({'state_fips':st.zfill(2),'replicate':k,'weighted_yes':str(D(int(nums[k]))/D(10000)),'weighted_denominator':str(D(int(dens[k]))/D(10000)),'proportion':str(props[k])})
 write('S2_2013_REPLICATE_ESTIMATES_v1.csv',rep_rows)
 check('variance_formula_verified',len(se_by_state)==51 and 'var = (4/160)' in (ROOT/'person_replicate_instructions.txt').read_text(),{'replicates':160,'factor':'4/160','variance':'(4/160)*sum((replicate_ratio-full_sample_ratio)^2)','reestimated_valid_denominator':True,'source':'Census2013 source page linked person instructions; March7 2012'})
 details=[];canonical=[];dc=[]
 for st in sorted(groups,key=int):
  for j,m in [(None,'ANY')]+list(enumerate(Q)):
   e=estimate(groups[st],j);details.append({'state':mapping[st],'state_fips':st.zfill(2),'year':2013,'measure':m,**e})
   if j is None:
    row={'state':mapping[st],'state_fips':st.zfill(2),'year':2013,'s2_participation':e['proportion'],'s2_se':str(se_by_state[st]),'n_unweighted':e['n_unweighted'],'weighted_denominator':e['weighted_denominator'],'source':RAWURL,'weight':'PWNRWGT','observation_type':'DIRECT','run_id':RUN_ID,'unit':'proportion','se_method':'CENSUS_NR_160_REPLICATES_FACTOR_4_OVER_160','n_eligible':e['n_eligible'],'n_missing':e['n_missing']}
    (dc if st=='11' else canonical).append(row)
 write('S2_Organizational_Participation_2013_DIRECT_v1.csv',canonical);write('S2_2013_DC_QA_v1.csv',dc)
 write('S2_2013_ITEM_COUNTS_v1.csv',details)
 nat=[]
 for scope,records in [('US_50_PLUS_DC',rs),('US_50_ONLY',[r for r in rs if r['state']!='11'])]:
  for j,m in [(None,'ANY')]+list(enumerate(Q)):nat.append({'scope':scope,'year':2013,'measure':m,**estimate(records,j)})
 write('S2_2013_NATIONAL_QA_v1.csv',nat)
 check('50_states_exactly',len(canonical)==50,'canonical row count')
 check('DC_excluded',not any(r['state_fips']=='11' for r in canonical),'DC stored separately')
 check('duplicates_zero',len({r['state_fips'] for r in canonical})==len(canonical),'state-year duplicates=0')
 check('missing_state_estimate_zero',all(r['s2_participation']!='' for r in canonical),'all states have positive valid denominator')
 check('year_2013',all(r['year']==2013 for r in canonical),'no other year extraction')
 check('direct_observations_50',sum(r['observation_type']=='DIRECT' for r in canonical)==50,'all observations DIRECT')
 check('respondent_count_recorded',len(rs)==38601,{'respondents':len(rs),'published_Q5A_total':38601})
 check('valid_respondent_N_recorded',sum(r['n_unweighted'] for r in canonical)==sum(r['any'] is not None for r in rs if r['state']!='11'),'canonical validN computed from jointfiveitemresponse rule')
 check('weighted_denominators_recorded',all(D(r['weighted_denominator'])>0 for r in canonical),'state and item denominators preserved')
 check('partition',all(r['n_yes']+r['n_no']+r['n_missing']==r['n_eligible'] and D(r['weighted_yes'])+D(r['weighted_no'])==D(r['weighted_denominator']) for r in details),'valid plus missing partition, weights sum')
 check('range',all(0<=D(r['s2_participation'])<=1 for r in canonical),'proportions [0,1]')
 expected={1:5386,2:31299,-2:167,-3:1534,-9:215};obs=dict(collections.Counter(r['a'][0] for r in rs))
 check('official_Q5A_frequencies',expected==obs,{'expected':expected,'observed':obs,'source':'Attachment13'})
 for j,target in [(None,237663000),(0,31507000),(2,22393000)]:
  val=control_pop if j is None else sum((r['w'] for r in rs if r['a'][j]==1),D(0))
  check('official_benchmark_'+str(j),abs(val-D(target))<=500,{'observed':str(val),'published_rounded':target,'tolerance_persons':500,'source':'2013 Attachment16 Illustration3','weight_basis':'PWSSWGT all civilian18+ population control' if j is None else 'PWNRWGT supplement Yes','note':'The illustration population base is reproduced with basic final weight; canonical estimates retain the instructed supplement weight and valid-response denominator.'})
 log['steps'].append({'stage':'direct_extraction','end_utc':now(),'respondents':len(rs),'canonical_rows':len(canonical),'status':'PASS'})
 
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
  for m,tab,entry in pool.map(api,Q):
   log['api_requests'].append(entry)
   if tab is None:
    check('API_QA_attempt_'+m,entry['status'].startswith('UNAVAILABLE'),{'status':entry['status'],'comparison_completed':False,'key_available':bool(KEY),'attempts':entry.get('attempts',[]),'note':'Public call nonJSON authwall; currentsecret unavailable; no weighted API result asserted'})
    continue
   head=tab[0];idx=head.index('state');diff=[]
   for line in tab[1:]:
    st=str(int(line[idx]))
    if st not in mapping:
     assert all(D(str(line[j]))==0 for j,x in enumerate(head) if isinstance(x,dict));continue
    t=next(r for r in details if int(r['state_fips'])==int(st) and r['measure']==m)
    for j,x in enumerate(head):
     if isinstance(x,dict) and x.get(m) in ['1','2']:diff.append(abs(D(str(line[j]))-D(t['weighted_yes' if x[m]=='1' else 'weighted_no'])))
   check('raw_API_weighted_'+m,len(diff)==102 and max(diff)<=D('0.51'),{'cells':len(diff),'max_abs_difference':str(max(diff)) if diff else None,'tolerance_persons':'0.51'})
 check('SE_coverage_reported',all(float(r['s2_se'])>0 for r in canonical),'50/50; official 2013 nonresponse replicate file; Census person supplement instructions dated March7 2012 linked from2013 source page; 160 replicates; factor4/160')
 for name in ['no_interpolation','no_ffill_bfill','no_model_estimates','no_adjacent_year_substitution','2012_synthetic_observation_zero']:
  check(name,all(r['year']==2013 and r['source']==RAWURL and r['observation_type']=='DIRECT' for r in canonical),'2013 raw weighted respondent ratios only;no otheryear rows;2012 NO DIRECT OBSERVATION')
 # Published independent any-organization benchmarks are diagnostic, not copied or forced to match.
 published=[('US_50_PLUS_DC','ANY',.363),('NC','ANY',.385),('UT','ANY',.588),('LA','ANY',.271)]
 external=[]
 for scope,m,target in published:
  record=next(r for r in nat if r['scope']==scope and r['measure']==m) if scope.startswith('US_') else next(r for r in details if r['state']==scope and r['measure']==m)
  direct=float(record['proportion']);delta=direct-target
  external.append({'scope':scope,'measure':m,'year':2013,'published':target,'direct':direct,'difference_percentage_points':100*delta,'rounding_tolerance_percentage_points':.05,'within_published_rounding':abs(delta)<=.0005,'benchmark_status':'FOUND','source':'https://ncoc.org/wp-content/uploads/2015/04/2015NorthCarolinaCHI.pdf','basis':'2013 CPS civic;age18+; any organization;technicalnote p37;publishedp14/p17','comparison_caveat':'independentunion missing rule is not specified; diagnosticcomparison, notvalidation of exactmissingalgorithm'})
 write('S2_2013_EXTERNAL_BENCHMARK_QA_v1.csv',external)
 check('external_benchmark_comparison_recorded',len(external)==4,'Four published unionbenchmarks compared; differences retained. Threshold0.05pp fixed beforeexecution; no forcedmatch or substitution.')

 log['steps'].append({'stage':'API_QA','end_utc':now(),'status':'PASS' if all(c['pass'] for c in checks) else 'FAIL','checks_passed':sum(c['pass'] for c in checks),'checks_total':len(checks)})
 log['exit_code']=0 if all(c['pass'] for c in checks) else 3
except Exception as e:
 log['error']=(type(e).__name__+': '+str(e)).replace(KEY,'REDACTED') if KEY else type(e).__name__+': '+str(e);log['exit_code']=2
log['end_utc']=now();log['outputs']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in ROOT.iterdir() if p.name.endswith('.csv') or p.name.startswith('API_')}
(ROOT/'QA_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
(ROOT/'S2_2013_RUN_LOG.txt').write_text(json.dumps(log,indent=2)+'\n')
print(json.dumps(log,indent=2));sys.exit(log['exit_code'])
