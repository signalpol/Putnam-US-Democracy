"""Common-scale S2 index. Direct data are preserved in a separate table.
Conditional latent covariance, profile-Hessian propagation, bounded model sensitivity.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
from pathlib import Path
import csv,json,datetime,hashlib,shutil
import numpy as np
from scipy.linalg import cho_solve
from scipy.special import expit
import model_core as c
R=Path(__file__).resolve().parent;O=R/'final_package';O.mkdir(exist_ok=True)
INPUT=c.INPUT
START=datetime.datetime.now(datetime.timezone.utc).isoformat();RUN='S2_FINAL_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
def log(stage,**kw):print(json.dumps(dict(run_id=RUN,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stage=stage,**kw)),flush=True)
def write(n,rows):
 with (O/n).open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def hess(f):
 x=f['theta'];ids=list(range(2 if f['model']=='M0' else 4));h=2e-3;out=np.zeros((len(ids),len(ids)));ev=f['evaluate'];b=ev(x)
 for i,a in enumerate(ids):
  ea=np.zeros(4);ea[a]=h;out[i,i]=(ev(x+ea)-2*b+ev(x-ea))/h**2
  for j,bb in enumerate(ids[:i]):
   eb=np.zeros(4);eb[bb]=h;out[i,j]=out[j,i]=(ev(x+ea+eb)-ev(x+ea-eb)-ev(x-ea+eb)+ev(x-ea-eb))/(4*h*h)
 return out,np.linalg.eigvalsh(out)
def pred(f,ss,tt,latent=True,obs=False):
 xx=c.design(tt,f['model']);
 if latent and f['model']=='M2':xx[:,2]=0
 ks=c.kernel(ss,tt,f['ss'],f['tt'],f['theta'],f['model']);ik=cho_solve(f['c'],ks.T);d=xx-ks@cho_solve(f['c'],f['xx']);mu=xx@f['beta']+ks@f['alpha'];vv=np.diag(c.kernel(ss,tt,ss,tt,f['theta'],f['model']))-(ks*ik.T).sum(1)+np.einsum('ij,jk,ik->i',d,f['bc'],d)
 if obs:vv+=np.exp(f['theta'][1])**2
 return mu,np.maximum(vv,0)
log('INPUT_VERIFIED',sha256=hashlib.sha256(INPUT.read_bytes()).hexdigest(),rows=len(c.rows))
ss=np.repeat(np.arange(50),24);tt=np.tile(np.arange(2000,2024),50);mask=np.ones(400,bool)
fits={};comparison=[];sensitivity=[];hold=[];parameter=[]
for m,L in [('M0',6),('M1',6),('M2',6),('M1',3),('M1',12),('M2',3),('M2',12)]:
 c.LENGTH=L;f=c.fit(mask,m);H,e=hess(f);name=f'{m}_L{L}';fits[name]=(f,L,H);k=len(f['beta'])+(2 if m=='M0' else 4)
 row=dict(specification=name,model=m,length_years=L,log_likelihood=-f['nll'],AIC=2*k+2*f['nll'],BIC=k*np.log(400)+2*f['nll'],converged=f['success'],gradient_max=f['gradient_max'],hessian_min_eigenvalue=float(e.min()),hessian_condition=float(e.max()/e.min()),start_nll_difference=abs(f['start_results'][0]['nll']-f['start_results'][1]['nll']),trend_logit_decade=f['beta'][1],CEV_offset=f['beta'][2] if m=='M2' else '',CEV_offset_conditional_SE=np.sqrt(f['bc'][2,2]) if m=='M2' else '',selected=name=='M2_L6');comparison.append(row);log('FIT',**row)
 parameter.append(dict(specification=name,theta=f['theta'].tolist(),beta=f['beta'].tolist(),beta_covariance=f['bc'].tolist(),profile_hessian=H.tolist(),starts=f['start_results']))
 if m!='M0':
  mu,vv=pred(f,ss,tt);sensitivity.append((name,mu,vv))
 if L==6:
  for yr in [2009,2011,2013,2019,2021]:
   f2=c.fit(c.t!=yr,m);a=c.t==yr;hm,hv=pred(f2,c.s[a],c.t[a],latent=False);hv+=np.where(c.missing[a],np.exp(f2['theta'][1])**2,c.v[a]);pr=expit(hm);lo=expit(hm-1.96*np.sqrt(hv));hi=expit(hm+1.96*np.sqrt(hv))
   for j,i in enumerate(np.flatnonzero(a)):hold.append(dict(model=m,holdout_year=yr,state=c.rows[i]['state'],observed=c.p[i],prediction=pr[j],residual=pr[j]-c.p[i],covered=bool(lo[j]<=c.p[i]<=hi[j]),CI_lower=lo[j],CI_upper=hi[j],converged=f2['success'],trend_logit_decade=f2['beta'][1],CEV_offset=f2['beta'][2] if m=='M2' else '',CEV_offset_SE=np.sqrt(f2['bc'][2,2]) if m=='M2' else ''))
   log('HOLDOUT',model=m,year=yr,RMSE=float(np.sqrt(np.mean((pr-c.p[a])**2))),coverage=float(np.mean((lo<=c.p[a])&(hi>=c.p[a]))))
c.LENGTH=6;f,_,H=fits['M2_L6'];mu,var=pred(f,ss,tt)
anchor_mu,anchor_v=pred(f,np.arange(50),np.repeat(2013,50));center=float(anchor_mu.mean());scale=float(anchor_mu.std(ddof=0));log('ANCHOR',year=2013,center=center,scale=scale)
# Profile-Hessian propagation: covariance hyperparameters are sampled, with GLS
# coefficients reestimated; conditional coefficient variance stays in base variance.
rng=np.random.default_rng(20261002);cov=np.linalg.inv(H);draws=[];attempt=0
while len(draws)<32 and attempt<300:
 attempt+=1;th=rng.multivariate_normal(f['theta'],cov)
 if np.any(th<np.array([-5,-7,-6,-6])) or np.any(th>np.array([1,-.5,0,0])):continue
 ff=f['evaluate'](th,True);ff['model']='M2';mm,vv=pred(ff,ss,tt);draws.append(mm)
assert len(draws)==32,'Hyperparameter draws insufficient'
hyper_var=np.var(draws,axis=0,ddof=1)
# A conservative model envelope incorporates M1/M2 and lengths 3,6,12.
model_mu=np.array([x[1] for x in sensitivity]);between=np.mean((model_mu-mu)**2,axis=0)
total_var=var+hyper_var+between;se=np.sqrt(total_var)/scale;zz=(mu-center)/scale
lower=np.minimum(zz-1.96*se,np.min(np.array([(m-1.96*np.sqrt(v)-center)/scale for _,m,v in sensitivity]),axis=0));upper=np.maximum(zz+1.96*se,np.max(np.array([(m+1.96*np.sqrt(v)-center)/scale for _,m,v in sensitivity]),axis=0))
direct={(x['state'],int(x['year'])):x for x in c.rows};panel=[];sens=[]
for i in range(1200):
 state=c.states[ss[i]];yr=int(tt[i]);d=direct.get((state,yr));flags=['REGIME_BRIDGE_ASSUMPTION','EARLY_CPS_DESIGN_BREAKS','UNKNOWN_SAMPLING_SE_WAVES']
 if yr<=2008:flags+=['BACKCAST','BACKCAST_MODEL_SENSITIVITY']
 if yr==2008:flags+=['NO_DIRECT_OBSERVATION_AVAILABLE_IN_CURRENT_EVIDENCE']
 if 2014<=yr<=2016:flags+=['CPS_CEV_GAP']
 panel.append(dict(state=state,year=yr,S2_estimate=float(zz[i]),S2_SE=float(se[i]),CI_lower=float(lower[i]),CI_upper=float(upper[i]),observation_type='MODEL_ESTIMATED',direct_observation=0,direct_input_available=int(d is not None),source_series='CPS_PARTICIPATION_AND_CEV_MEMBERSHIP_LATENT_MODEL',measurement_regime='COMMON_SCALE_CPS_2013_ANCHOR',model_estimated=1,backcast_flag=int(yr<=2008),bridge_flag=1,uncertainty_flag=';'.join(flags),provenance=f'{RUN}|M2_L6|inherited_base_sha256:'+hashlib.sha256(INPUT.read_bytes()).hexdigest(),unit='LATENT_INDEX_2013_STATE_SD',CI_method='MODEL_AND_LENGTH_SENSITIVITY_ENVELOPE',latent_logit_coordinate=float(mu[i])))
 for name,mm,vv in sensitivity:sens.append(dict(state=state,year=yr,specification=name,latent_index=float((mm[i]-center)/scale),conditional_SE=float(np.sqrt(vv[i])/scale),backcast_flag=int(yr<=2008)))
observed=[dict(**r,observation_type='DIRECT',direct_observation=1,model_estimated=0,unit='proportion',measurement_regime='CPS_PARTICIPATION' if int(r['year'])<2017 else 'CEV_MEMBERSHIP') for r in c.rows]
write('S2_DIRECT_OBSERVED_2009_2023.csv',observed);write('S2_DIRECT_OBSERVATIONS_FINAL.csv',observed);write('S2_FINAL_2000_2023.csv',panel);write('S2_M1_M2_SENSITIVITY.csv',sens);write('S2_MODEL_COMPARISON.csv',comparison);write('S2_HOLDOUT_VALIDATION.csv',hold)
summary=[]
for m in ['M0','M1','M2']:
 rr=[x for x in hold if x['model']==m];er=np.array([x['residual'] for x in rr]);summary.append(dict(model=m,n=len(rr),MAE=float(np.mean(abs(er))),RMSE=float(np.sqrt(np.mean(er**2))),mean_bias=float(np.mean(er)),coverage=float(np.mean([x['covered'] for x in rr])),all_converged=all(x['converged'] for x in rr)))
write('S2_HOLDOUT_SUMMARY.csv',summary)
qa=[]
def check(n,ok,actual):qa.append(dict(check=n,result='PASS' if ok else 'FAIL',actual=actual))
check('rows',len(panel)==1200,len(panel));check('states',len(c.states)==50,len(c.states));check('years',sorted(set(tt))==list(range(2000,2024)),'2000-2023');check('state_year_duplicates',len({(x['state'],x['year']) for x in panel})==1200,0);check('each_state_24',all(sum(x['state']==s for x in panel)==24 for s in c.states),24);check('DC_excluded','DC' not in c.states,0);check('territories_excluded',not(set(c.states)&{'PR','GU','VI','AS','MP'}),0);check('finite_estimates',np.isfinite(zz).all(),int(np.isfinite(zz).sum()));check('finite_positive_SE',np.isfinite(se).all() and (se>0).all(),1200);check('CI_order',all(x['CI_lower']<=x['S2_estimate']<=x['CI_upper'] for x in panel),1200);check('latent_all_model',all(x['observation_type']=='MODEL_ESTIMATED' and x['direct_observation']==0 for x in panel),1200);check('observed_direct_rows',len(observed)==400 and all(x['observation_type']=='DIRECT' for x in observed),400);check('observed_exact_input_values',all(r['s2_participation']==c.rows[j]['s2_participation'] and r['s2_se']==c.rows[j]['s2_se'] for j,r in enumerate(observed)),400);check('backcast_2000_2008',sum(x['backcast_flag'] for x in panel)==450,450);check('2012_not_direct',all(x['direct_observation']==0 for x in panel if x['year']==2012),50);check('backcast_sensitivity_flag',all('BACKCAST_MODEL_SENSITIVITY' in x['uncertainty_flag'] for x in panel if x['year']<=2008),450);check('provenance_complete',all(x['provenance'] for x in panel),1200);check('no_percentage_latent',all(x['unit']=='LATENT_INDEX_2013_STATE_SD' for x in panel),1200);check('selected_converged',f['success'],f['message']);check('selected_hessian_positive',np.linalg.eigvalsh(H).min()>0,float(np.linalg.eigvalsh(H).min()));check('holdouts_executed',len(hold)==750,len(hold));check('holdouts_converged',all(x['converged'] for x in hold),sum(x['converged'] for x in hold));check('hyperparameter_draws',len(draws)==32,len(draws));check('no_interpolation_ffill_bfill',True,'Gaussian process conditional expectation');check('no_synthetic_direct_2008',not any(int(x['year'])==2008 for x in observed),0);check('anchor_mean',abs(np.mean(zz[tt==2013]))<1e-12,float(np.mean(zz[tt==2013])));check('anchor_sd',abs(np.std(zz[tt==2013])-1)<1e-12,float(np.std(zz[tt==2013])))
write('S2_QA_FINAL.csv',qa);assert all(x['result']=='PASS' for x in qa),qa
(O/'S2_MODEL_PARAMETERS.json').write_text(json.dumps(dict(run_id=RUN,anchor=dict(year=2013,center=center,scale=scale,conditional_fixed_anchor=True),hyper_draws=32,seed=20261002,models=parameter),indent=2))
for n in ['model_core.py','finalize_s2.py']:shutil.copy2(R/n,O/n)
shutil.copy2(INPUT,O/'canonical_base.csv')
for name in ['S2_SOURCE_REGISTRY.csv','S2_MEASUREMENT_EQUIVALENCE_AUDIT.md']:
 src=R/'decision_review'/name
 if not src.exists():src=R/name
 shutil.copy2(src,O/name)
log('QA_COMPLETE',PASS=len(qa),total=len(qa))
(O/'S2_RUN_MANIFEST.json').write_text(json.dumps(dict(run_id=RUN,started_utc=START,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=0,input_sha256=hashlib.sha256(INPUT.read_bytes()).hexdigest(),code_sha256={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in ['model_core.py','finalize_s2.py']},selected_model='M2_L6',QA_pass=len(qa),output_rows=1200,direct_rows=400,stage_log='S2_FINAL_RUN_LOG.txt',limitations=['regime offset identified conditionally on temporal-process assumptions; no overlapping measurement calibration','2008 unavailable in current evidence','2019/2021 document audit incomplete','unknown design SE for 2009/2010/CEV','fixed loading 1 and constant CEV offset','hyperparameter uncertainty approximate; anchor fixed','CI is conservative sensitivity envelope, not calibrated 95% confidence coverage']),indent=2))
# Typed values for artifact-tool authoring; statistics themselves remain in code.
(R/'workbook_data.json').write_text(json.dumps(dict(panel=panel,observed=observed,qa=qa,holdout_summary=summary,comparison=comparison),allow_nan=False))
