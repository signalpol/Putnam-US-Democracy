"""2009 CPS Civic API acquisition probe; no credentials in URLs or logs."""
import concurrent.futures,datetime,hashlib,json,pathlib,re,sys,urllib.request
BASE='https://api.census.gov/data/2009/cps/civic/nov'
ROOT=pathlib.Path(__file__).resolve().parent
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
log={'run_id':'S2_2009_CENSUS_API_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ'),'started_at':now(),'source':BASE,'year':2009,'key_parameter_present':False,'code_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'requests':[]}
def request(label,url):
 entry={'label':label,'url':url,'started_at':now()}
 try:
  with urllib.request.urlopen(url,timeout=35) as r:
   b=r.read();entry.update(http_status=r.status,content_type=r.headers.get('Content-Type'),response_sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
  (ROOT/(label+'.response')).write_bytes(b)
  try:
   data=json.loads(b);entry['json_valid']=True
   if label=='variables':
    names=['PEQ5A','PEQ5B','PEQ5C','PEQ5D','PEQ5E','GESTFIPS','PRTAGE','HRMIS','PRSUPINT','PRPERTYP','PWNRWGT']
    selected={k:data['variables'].get(k) for k in names}
    (ROOT/'verified_variables.json').write_text(json.dumps(selected,indent=2)+'\n');entry['all_required_variables_present']=all(selected.values())
   else:entry['data_rows']=len(data)-1 if isinstance(data,list) else None
  except (ValueError,KeyError):
   entry['json_valid']=False;entry['html_title']=re.findall(r'<title>(.*?)</title>',b.decode('utf-8','replace'),re.S)[:1]
 except Exception as e:entry['error']=str(e)
 entry['ended_at']=now();return entry
# Full records retain joint item responses; marginal counts cannot identify the union.
fields='GESTFIPS,PRTAGE,HRMIS,PRSUPINT,PRPERTYP,PWNRWGT,PEQ5A,PEQ5B,PEQ5C,PEQ5D,PEQ5E'
queries=[('variables',BASE+'/variables.json'),('raw_eligible_no_key',BASE+'?get='+fields+'&PRTAGE=18:90&HRMIS=4,8&PRSUPINT=1&PRPERTYP=2&for=state:*')]
for q in 'ABCDE':
 item='PEQ5'+q
 queries.append(('weighted_'+item+'_no_key',BASE+'?tabulate=weight(PWNRWGT)&row+for&col+'+item+'&'+item+'=1,2&PRTAGE=18:90&HRMIS=4,8&PRSUPINT=1&PRPERTYP=2&for=state:*'))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for result in pool.map(lambda x:request(*x),queries):log['requests'].append(result)
data_requests=log['requests'][1:]
log['ended_at']=now();log['acquisition_status']='PASS' if all(r.get('json_valid') and r.get('data_rows',0)>0 for r in data_requests) else 'FAILED'
log['estimation_status']='ENGINE NOT EXECUTED';log['state_estimate_rows_created']=0;log['exit_code']=0 if log['acquisition_status']=='PASS' else 2
(ROOT/'execution_log.json').write_text(json.dumps(log,indent=2)+'\n')
print(json.dumps(log,indent=2))
sys.exit(log['exit_code'])
