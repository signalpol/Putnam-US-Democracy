"""S5 concrete method-decision review. No canonical series selected or frozen."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import csv,json,pathlib,datetime,hashlib,gzip,collections,time
import numpy as np
from scipy.linalg import cho_factor,cho_solve
from scipy.optimize import minimize
ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/'review_package';OUT.mkdir(exist_ok=True)
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
started=now();run='S5_REVIEW_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
log={'run_id':run,'started_utc':started,'code_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'stages':[],'inputs':{}}
def stage(n,**kw):log['stages'].append({'stage':n,'utc':now(),**kw})
def write(name,rows):
 with open(OUT/name,'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def source(p):
 b=p.read_bytes();log['inputs'][str(p.relative_to(ROOT) if p.is_relative_to(ROOT) else p)]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
raw=list(csv.DictReader(open(ROOT/'inputs/raw.csv')));source(ROOT/'inputs/raw.csv');source(ROOT/'inputs/cev.xlsx')
names=list(dict.fromkeys(r['measure'] for r in raw));states=sorted({r['state_abbr'] for r in raw});keys=sorted({(r['state_abbr'],int(r['year'])) for r in raw});lookup={(r['state_abbr'],int(r['year']),r['measure']):float(r['value']) for r in raw}
X=np.array([[lookup[k+(m,)] for m in names] for k in keys]);assert X.shape==(200,10) and len(lookup)==2000
import openpyxl
book=openpyxl.load_workbook(ROOT/'inputs/cev.xlsx',data_only=True);mismatch=[]
for r in raw:
 sheet=book[r['measure']];row=next(z for z in sheet.values if z[0]==r['state_abbr']);p=row[1+[2017,2019,2021,2023].index(int(r['year']))]
 if float(r['value'])!=p:mismatch.append(r)
assert not mismatch
stage('raw_audit',rows=len(raw),states=len(states),measures=names,archived_workbook_mismatches=len(mismatch))
observed=[{'state':r['state_abbr'],'year':int(r['year']),'measure':r['measure'],'value':r['value'],'SE':'','unit':'proportion','observation_type':'DIRECT','source':r['source'],'weight':'PWNRWGT per official Census documentation; archived denominator details not independently reproduced','measurement_regime':'CEV_ARCHIVED_RATE','eligible_n':'','valid_n':'','weighted_denominator':'','provenance':'Drive raw exact archived workbook match; design SE unavailable in archived rates'} for r in raw]
# Exact binary contacted-official / boycott items are independent earlier item observations,
# not observations of either ten-item or six-item basket. Adult operational sample preserves document/raw MIS conflicts.
historical=lambda directory,name: ROOT/'historical_inputs'/directory/name if (ROOT/'historical_inputs'/directory/name).exists() else ROOT.parent/directory/name
fips=json.load(open(historical('2011_run','variables.json')))['variables']['GESTFIPS']['values']['item'];abbr_by_name={}
state_names={'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'}
for ff,n in fips.items():
 if n in states:abbr_by_name[int(ff)]=n
 for nn,aa in state_names.items():
  if n.upper()==nn.upper():abbr_by_name[int(ff)]=aa
for yr,directory,filename,interview,weight,rawlength in [(2010,'2010_run','nov10pub_civic.dat.gz',978,980,990),(2011,'2011_run','nov11pub.dat.gz',994,1006,1016),(2013,'2013_run','nov13pub.dat.gz',990,1002,1012)]:
 p=historical(directory,filename);source(p);doc=historical(directory,'codebook.txt');source(doc)
 records=[];mis=collections.Counter();all_n=0
 with gzip.open(p,'rt',encoding='ascii') as f:
  for line in f:
   z=line.rstrip('\r\n');assert len(z)==rawlength;all_n+=1
   if int(z[121:123])<18 or int(z[160:162])!=2 or int(z[interview:interview+2])!=1:continue
   st=int(z[92:94]);mis[int(z[62:64])]+=1
   if st==11:continue
   records.append((z[814:821],abbr_by_name[st],int(z[weight:weight+10]),int(z[952:954]),int(z[954:956])))
 agg={}
 for st in states:
  rr=[r for r in records if r[1]==st]
  for j,name in [(3,'Contacting Public Officials'),(4,'Buycotting or Boycotting')]:
   valid=[r for r in rr if r[j] in [1,2] and r[2]>0];den=sum(r[2] for r in valid);yes=sum(r[2] for r in valid if r[j]==1);assert den>0
   agg[(st,j)]={'den':den,'yes':yes,'repden':np.zeros(160),'repyes':np.zeros(160),'rr':rr,'valid':valid}
 if yr in [2011,2013]:
  rep=historical(directory,'nov'+str(yr)[2:]+'nrrep.dat.gz');source(rep);bykey={r[0]:r for r in records};assert len(bykey)==len(records);matched=0
  with gzip.open(rep,'rt',encoding='ascii') as f:
   for line in f:
    z=line.rstrip('\r\n');assert len(z)==1617
    if z[:7] not in bykey:continue
    r=bykey[z[:7]];ww=np.array([int(z[k:k+10]) for k in range(7,1617,10)]);assert ww[0]==r[2];matched+=1
    for j in [3,4]:
     if r[j] in [1,2] and r[2]>0:
      a=agg[(r[1],j)];a['repden']+=ww[1:];a['repyes']+=ww[1:]*(r[j]==1)
  assert matched==len(records)
 for (st,j),a in agg.items():
  p=a['yes']/a['den'];se=''
  if yr in [2011,2013]:
   pr=a['repyes']/a['repden'];se=float(np.sqrt(4/160*np.sum((pr-p)**2)))
  observed.append({'state':st,'year':yr,'measure':names[5 if j==3 else 9],'value':p,'SE':se,'unit':'proportion','observation_type':'DIRECT','source':f'Census November {yr} Civic Engagement raw','weight':'PWNRWGT, 4 implied decimals','measurement_regime':'CPS_CIVIC_BINARY_ITEM_PARTIAL_BASKET','eligible_n':len(a['rr']),'valid_n':len(a['valid']),'weighted_denominator':a['den']/10000,'provenance':f'{filename}; positions953–956; adult civilian supplement interviews; missing negatives excluded; document/raw MIS conflict retained; SE '+('160 NR replicate ratios, 4/160' if se!='' else 'NOT VERIFIED')})
 stage('historical_direct_item_extraction',year=yr,raw_records=all_n,eligible_50states=len(records),MIS_counts_DC_inclusive=dict(mis),direct_item_cells=100)
write('S5_DIRECT_ITEM_OBSERVATIONS_REVIEW.csv',observed)
# One fixed 2017 anchor. No year-specific standardization. Item basket choices are unresolved.
baseline=np.array([k[1]==2017 for k in keys]);center=X[baseline].mean(0);scale=X[baseline].std(0,ddof=0);Z=(X-center)/scale
active=[4,5,6,7,8,9];C=np.corrcoef(X,rowvar=False);ev,evec=np.linalg.eigh(C);load=evec[:,-1];load*=np.sign(load.sum())
baskets={'BROAD_10':np.ones(10)/10,'ACTIVE_6':np.array([1/6 if j in active else 0 for j in range(10)]),'PC1_10_DIAGNOSTIC':load/load.sum()}
desc=[];scored=[]
for b,ww in baskets.items():
 score=Z@ww;score/=score[baseline].std()
 for yr in [2017,2019,2021,2023]:
  ix=np.array([k[1]==yr for k in keys]);desc.append({'basket':b,'year':yr,'equal_state_mean_fixed2017_SD':float(score[ix].mean()),'states':50,'status':'DIAGNOSTIC_NOT_CANONICAL'})
 for k,ss in zip(keys,score):scored.append({'basket':b,'state':k[0],'year':k[1],'candidate_score':ss,'unit':'fixed2017 index SD','status':'DIAGNOSTIC_NOT_CANONICAL'})
write('S5_BASKET_TREND_COMPARISON.csv',desc);write('S5_CANDIDATE_OBSERVED_SCORES.csv',scored)
write('S5_ITEM_LOADINGS_DIAGNOSTIC.csv',[{'measure':n,'2017_center':center[i],'2017_scale':scale[i],'pooled_PC1_loading':load[i],'active6_inclusion':int(i in active),'broad10_inclusion':1} for i,n in enumerate(names)])
stage('construct_sensitivity',PC1_variance_share=float(ev[-1]/10),eigenvalues=ev[::-1].tolist(),minimum_pairwise_correlation=float(C[np.triu_indices(10,1)].min()))
# Bounded prospective model comparison. Four leave-one-wave-out folds; preprocessing uses training waves only.
S=np.array([states.index(k[0]) for k in keys]);T=np.array([k[1] for k in keys]);modelout=[];foldout=[];rawout={}
def gpfit(y,mask,model):
 ss,tt,yy=S[mask],T[mask],y[mask];xx=np.ones((len(tt),1));dist=np.abs(tt[:,None]-tt[None,:]);same=ss[:,None]==ss[None,:]
 def evaluate(th,detail=False):
  a,e,q,c=np.exp(th);K=a*a*same+np.diag(np.full(len(tt),e*e))
  if model=='M1':K+=q*q*same*np.exp(-dist/6)+c*c*np.exp(-dist/6)
  ch=cho_factor(K);ix=cho_solve(ch,xx);bc=np.linalg.inv(xx.T@ix);beta=bc@(xx.T@cho_solve(ch,yy));r=yy-xx@beta;al=cho_solve(ch,r);nll=.5*(r@al+2*np.log(np.diag(ch[0])).sum()+len(yy)*np.log(2*np.pi))
  if detail:return {'th':th,'ch':ch,'beta':beta,'bc':bc,'al':al,'ix':ix,'xx':xx,'ss':ss,'tt':tt,'nll':nll}
  return nll
 bounds=[(-4,2),(-5,1),(-6,2),(-6,2)]
 if model=='M0':bounds[2:]=[(-12,-12),(-12,-12)]
 opts=[minimize(evaluate,ini,method='L-BFGS-B',bounds=bounds,options={'maxiter':180}) for ini in [[-.2,-1,-1,-1],[-.5,-.5,-2,-.5]]];o=min(opts,key=lambda o:o.fun);f=evaluate(o.x,True)
 free=[j for j,(a,b) in enumerate(bounds) if a!=b];h=1e-3;H=np.zeros((len(free),len(free)))
 for ii,i in enumerate(free):
  ei=np.eye(4)[i]*h
  for jj,j in enumerate(free):
   ej=np.eye(4)[j]*h;H[ii,jj]=(evaluate(o.x+ei+ej)-evaluate(o.x+ei-ej)-evaluate(o.x-ei+ej)+evaluate(o.x-ei-ej))/(4*h*h)
 eigen=np.linalg.eigvalsh(H);boundary=[j for j in free if min(abs(o.x[j]-bounds[j][0]),abs(o.x[j]-bounds[j][1]))<.01]
 f.update(success=bool(o.success),gradient=float(np.nanmax(np.abs(o.jac))),hessian_eigenvalues=eigen.tolist(),boundary_parameters=boundary,starts=[{'success':bool(z.success),'nll':float(z.fun),'theta':z.x.tolist()} for z in opts]);return f
def pred(f,ss,tt,model):
 a,e,q,c=np.exp(f['th']);same=ss[:,None]==f['ss'][None,:];dist=abs(tt[:,None]-f['tt'][None,:]);ks=a*a*same
 if model=='M1':ks+=q*q*same*np.exp(-dist/6)+c*c*np.exp(-dist/6)
 xx=np.ones((len(ss),1));d=xx-ks@f['ix'];mu=xx@f['beta']+ks@f['al'];vv=a*a+(q*q+c*c if model=='M1' else 0)+e*e-np.sum(ks*cho_solve(f['ch'],ks.T).T,axis=1)+np.einsum('ij,jk,ik->i',d,f['bc'],d);return mu,np.sqrt(np.maximum(vv,0))
for b,ww in list(baskets.items())[:2]:
 for model in ['M0','M1']:
  sco=Z@ww;sco/=sco[baseline].std();f=gpfit(sco,np.ones(200,dtype=bool),model);params=5 if model=='M1' else 3;modelout.append({'basket':b,'model':model,'n':200,'nll':f['nll'],'AIC':2*params+2*f['nll'],'BIC':params*np.log(200)+2*f['nll'],'convergence':f['success'],'gradient_max':f['gradient'],'hessian_min_eigenvalue':min(f['hessian_eigenvalues']),'boundary_parameters':str(f['boundary_parameters']),'temporal_length_years':6 if model=='M1' else '', 'status':'DIAGNOSTIC_NOT_CANONICAL'})
  rawout[b+'_'+model]={'theta':f['th'].tolist(),'beta':f['beta'].tolist(),'starts':f['starts'],'hessian_eigenvalues':f['hessian_eigenvalues'],'boundary_parameters':f['boundary_parameters']}
  for hold in [2017,2019,2021,2023]:
   mask=T!=hold;traincenter=X[mask].mean(0);trainscale=X[mask].std(0);yy=((X-traincenter)/trainscale)@ww;yy/=yy[mask].std();ff=gpfit(yy,mask,model);p,sd=pred(ff,S[~mask],T[~mask],model);err=p-yy[~mask];foldout.append({'basket':b,'model':model,'holdout_year':hold,'heldout_states':50,'MAE_training_scale_SD':float(np.abs(err).mean()),'RMSE_training_scale_SD':float(np.sqrt(np.mean(err**2))),'mean_bias_training_scale_SD':float(err.mean()),'95pct_prediction_interval_coverage':float((np.abs(err)<=1.96*sd).mean()),'convergence':ff['success'],'preprocessing':'training_only','status':'DIAGNOSTIC_NOT_CANONICAL'})
write('S5_MODEL_COMPARISON_REVIEW.csv',modelout);write('S5_HOLDOUT_REVIEW.csv',foldout)
(OUT/'S5_MODEL_RAW_OUTPUT.json').write_text(json.dumps(rawout,indent=2));stage('model_comparison',fits=20,canonical_selected=False)
log.update(ended_utc=now(),exit_code=0,status='PARTIAL_BLOCKED_METHOD_DECISION');(OUT/'S5_RUN_LOG.json').write_text(json.dumps(log,indent=2))
print(json.dumps({'run_id':run,'observed_item_rows':len(observed),'CEV_rows':2000,'historical_rows':300,'basket_trends':desc,'model_comparison':modelout,'holdout':foldout,'status':log['status']}))
