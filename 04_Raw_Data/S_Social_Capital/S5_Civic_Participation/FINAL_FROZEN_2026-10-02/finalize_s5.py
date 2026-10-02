"""S5 approved Active6 analytical series. Original item proportions are immutable.
Run python finalize_s5.py from extracted replication root. numpy/scipy required.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import csv,json,pathlib,datetime,hashlib,time
import numpy as np
from scipy.linalg import cho_factor,cho_solve
from scipy.optimize import minimize
ROOT=pathlib.Path(__file__).resolve().parent;IP=ROOT/'inputs';OUT=ROOT/'final_package';OUT.mkdir(exist_ok=True)
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();start=now();RUN='S5_ACTIVE6_FINAL_20261002_v1'
manifest=dict(run_id=RUN,start_utc=start,code_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),input_hashes={},stages=[])
def stage(n,**kw):manifest['stages'].append(dict(stage=n,utc=now(),**kw));print(n,json.dumps(kw),flush=True)
def write(n,rs):
 with (OUT/n).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
def read(n):
 p=IP/n;manifest['input_hashes'][n]=dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest());return list(csv.DictReader(p.open(encoding='utf-8-sig')))
obs=read('S5_DIRECT_ITEM_OBSERVATIONS_REVIEW.csv');raw=read('S5_ORIGINAL_RAW_UNCHANGED.csv');names=list(dict.fromkeys(r['measure'] for r in raw));states=sorted({r['state_abbr'] for r in raw});keys=sorted({(r['state_abbr'],int(r['year'])) for r in raw});D={(r['state_abbr'],int(r['year']),r['measure']):float(r['value']) for r in raw};X=np.array([[D[k+(n,)] for n in names] for k in keys]);T=np.array([k[1] for k in keys]);S=np.array([states.index(k[0]) for k in keys]);assert X.shape==(200,10) and len(obs)==2300
hist=[r for r in obs if int(r['year'])<2017];hkeys=sorted({(r['state'],int(r['year'])) for r in hist});HD={(r['state'],int(r['year']),r['measure']):r for r in hist};HX=np.array([[float(HD[k+(names[j],)]['value']) for j in [5,9]] for k in hkeys]);HSE=np.array([[float(HD[k+(names[j],)]['SE']) if HD[k+(names[j],)]['SE'] else 0 for j in [5,9]] for k in hkeys]);HS=np.array([states.index(k[0]) for k in hkeys]);HT=np.array([k[1] for k in hkeys]);baskets={'ACTIVE6':[4,5,6,7,8,9],'BROAD10':list(range(10)),'ACTIVE5':[5,6,7,8,9]}
write('S5_DIRECT_OBSERVATIONS_FINAL.csv',obs);write('S5_DIRECT_OBSERVED_ITEMS_2010_2023.csv',obs)
# Actual observed years:2010/11/13/17/19/21/23.
stage('approved_construct_inputs',item_rows=len(obs),full_basket_waves=4,partial_historical_item_rows=len(hist),approval='Active6 primary;Broad10 andActive5 sensitivity;construct validity decision')
modelrows=[];rawfits={};hold=[];residual=[];linkrows=[];calibrations={}
def prepare(basket,mask):
 anchor=int(min(T[mask]));am=mask&(T==anchor);center=X[am].mean(0);scale=X[am].std(0);z=(X-center)/scale;ii=baskets[basket];score=z[:,ii].mean(1);norm=score[am].std();score/=norm
 b=np.column_stack([np.ones(200),z[:,5],z[:,9]]);coeff=np.linalg.lstsq(b[mask],score[mask],rcond=None)[0];rr=score[mask]-b[mask]@coeff;v=float(rr@rr/(mask.sum()-3));cov=v*np.linalg.inv(b[mask].T@b[mask]);hb=np.column_stack([np.ones(len(hkeys)),(HX[:,0]-center[5])/scale[5],(HX[:,1]-center[9])/scale[9]]);proxy=hb@coeff
 known=(np.abs(coeff[1])*HSE[:,0]/scale[5]+np.abs(coeff[2])*HSE[:,1]/scale[9])**2
 return dict(y=score,proxy=proxy,bridge_v=v,bridge_cov=hb@cov@hb.T,hb=hb,coeff=coeff,coeff_cov=cov,known=known,center=center,scale=scale,norm=norm,anchor=anchor,link_R2=1-v/np.var(score[mask],ddof=1),link_residual=rr)
def fit(pr,cm,hm,model,length=6,tau=.5):
 include_hist=model!='CEV_ONLY';hm=hm if include_hist else np.zeros(len(hkeys),bool);ss=np.r_[S[cm],HS[hm]];tt=np.r_[T[cm],HT[hm]];yy=np.r_[pr['y'][cm],pr['proxy'][hm]];reg=np.r_[np.zeros(cm.sum()),np.ones(hm.sum())];same=ss[:,None]==ss[None,:];dist=np.abs(tt[:,None]-tt[None,:]);E=np.exp(-dist/length);Z=np.ones((len(yy),1));nc=cm.sum()
 extra=np.zeros((len(yy),len(yy)));extra[nc:,nc:]=np.diag(pr['known'][hm]+pr['bridge_v'])
 if model=='M2':extra[nc:,nc:]+=pr['bridge_cov'][np.ix_(hm,hm)]+tau*tau
 # M0/M1 use the same partial-item projection, but omit systematic regime/calibration covariance.
 comps=[same.astype(float),np.eye(len(yy)),same*E,E]
 if model=='M0':comps=comps[:2]
 def eval(th,detail=False):
  var=np.exp(2*th);K=extra.copy()+np.eye(len(yy))*1e-8
  for v,c in zip(var,comps):K+=v*c
  ch=cho_factor(K,lower=True,check_finite=False);kiZ=cho_solve(ch,Z,check_finite=False);BC=np.linalg.inv(Z.T@kiZ);beta=BC@(Z.T@cho_solve(ch,yy,check_finite=False));r=yy-Z@beta;alpha=cho_solve(ch,r,check_finite=False);nll=.5*(r@alpha+2*np.log(np.diag(ch[0])).sum()+len(yy)*np.log(2*np.pi))
  if detail:return dict(th=th,var=var,ch=ch,kiZ=kiZ,BC=BC,beta=beta,alpha=alpha,nll=float(nll),ss=ss,tt=tt,yy=yy,reg=reg,comps=comps,extra=extra,model=model,length=length,tau=tau)
  inv=cho_solve(ch,np.eye(len(yy)),check_finite=False);A=inv-np.outer(alpha,alpha);jac=np.array([v*np.sum(A*c) for v,c in zip(var,comps)]);return nll,jac
 bounds=[(-5,2),(-5,1)]+([(-5,2),(-5,2)] if len(comps)==4 else []);initials=[[-.2,-1,-1,-1],[-.5,-.5,-2,-.5]];opts=[minimize(eval,np.array(x[:len(comps)]),jac=True,method='L-BFGS-B',bounds=bounds,options={'maxiter':160,'ftol':1e-10,'gtol':1e-6}) for x in initials];o=min(opts,key=lambda x:x.fun);f=eval(o.x,True)
 H=np.zeros((len(o.x),len(o.x)));h=1e-3
 for j in range(len(o.x)):
  ej=np.eye(len(o.x))[j]*h;H[:,j]=(eval(o.x+ej)[1]-eval(o.x-ej)[1])/(2*h)
 H=(H+H.T)/2;ev=np.linalg.eigvalsh(H);boundary=[j for j in range(len(o.x)) if min(abs(o.x[j]-bounds[j][0]),abs(o.x[j]-bounds[j][1]))<.015]
 f['_evaluate']=eval
 f.update(success=bool(o.success),gradient=float(np.max(abs(o.jac))),H=H,hessian_eigenvalues=ev.tolist(),boundary=boundary,starts=[dict(success=bool(z.success),nll=float(z.fun),theta=z.x.tolist()) for z in opts]);return f
PS=np.repeat(np.arange(50),24);PT=np.tile(np.arange(2000,2024),50)
def predict(f,ss,tt,partial=False,pr=None,hm=None):
 same=ss[:,None]==f['ss'][None,:];E=np.exp(-np.abs(tt[:,None]-f['tt'][None,:])/f['length']);vv=f['var'];cross=vv[0]*same;prior=np.full(len(ss),vv[0]);
 if len(vv)==4:cross=cross+vv[2]*same*E+vv[3]*E;prior+=vv[2]+vv[3]
 if partial and f['model']=='M2':cross+=f['tau']**2*f['reg'][None,:];prior+=f['tau']**2
 Z=np.ones((len(ss),1));d=Z-cross@f['kiZ'];mu=Z@f['beta']+cross@f['alpha'];sd2=prior-np.sum(cross*cho_solve(f['ch'],cross.T,check_finite=False).T,axis=1)+np.einsum('ij,jk,ik->i',d,f['BC'],d)
 if partial and pr is not None:sd2+=vv[1]+pr['bridge_v']+pr['known'][hm]+np.diag(pr['bridge_cov'])[hm]
 return mu,np.sqrt(np.maximum(sd2,1e-10))
def summarize(b,mod,f,scope='FULL',length=6,tau=.5):
 k=len(f['th'])+1;return dict(basket=b,model=mod,scope=scope,n=len(f['yy']),length_years=length,regime_prior_SD=tau if mod=='M2' else 0,nll=f['nll'],AIC=2*f['nll']+2*k,BIC=2*f['nll']+k*np.log(len(f['yy'])),converged=f['success'],gradient_max=f['gradient'],hessian_min_eigenvalue=min(f['hessian_eigenvalues']),boundary_parameters=str(f['boundary']),information_criterion_comparability='within_same_basket_input_set_only')
allc=np.ones(200,bool);allh=np.ones(150,bool);full={};sens={}
for b in baskets:
 pr=prepare(b,allc);calibrations[b]={k:(v.tolist() if isinstance(v,np.ndarray) else v) for k,v in pr.items() if k in ['coeff','coeff_cov','center','scale','norm','anchor','bridge_v','link_R2']}
 for k,coeff in enumerate(pr['coeff']):linkrows.append(dict(basket=b,term=['intercept','contact_scaled','political_consumption_scaled'][k],coefficient=float(coeff),coefficient_SE=float(np.sqrt(pr['coeff_cov'][k,k])),link_residual_SD=float(np.sqrt(pr['bridge_v'])),R_squared=pr['link_R2'],status='CEV_CALIBRATION_ASSUMED_TRANSFER_TO_CPS'))
 for mod in ['M0','M1','M2']:
  f=fit(pr,allc,allh,mod);full[b,mod]=(f,pr);modelrows.append(summarize(b,mod,f));rawfits[b+'_'+mod]={k:f[k] for k in ['nll','success','gradient','hessian_eigenvalues','boundary','starts']};mu,sd=predict(f,PS,PT);sens[b+'_'+mod]=(mu,sd)
  rawfits[b+'_'+mod].update(selected_theta=f['th'].tolist(),selected_beta=f['beta'].tolist())
  stage('full_fit',basket=b,model=mod,nll=f['nll'],converged=f['success'],boundary=f['boundary'])
# Primary M2 explicitly represents measurement-regime uncertainty; definition is not selected by declining trend.
for tag,length,tau,usehist in [('LENGTH3',3,.5,True),('LENGTH12',12,.5,True),('REGIME_SD1',6,1.,True),('CEV_ONLY',6,0,False)]:
 pr=prepare('ACTIVE6',allc);mod='M2' if usehist else 'CEV_ONLY';f=fit(pr,allc,allh,mod,length,tau);modelrows.append(summarize('ACTIVE6',mod,f,tag,length,tau));mu,sd=predict(f,PS,PT);sens['ACTIVE6_'+tag]=(mu,sd);rawfits['ACTIVE6_'+tag]={k:f[k] for k in ['nll','success','gradient','hessian_eigenvalues','boundary','starts']};rawfits['ACTIVE6_'+tag].update(selected_theta=f['th'].tolist(),selected_beta=f['beta'].tolist())
 stage('sensitivity_fit',tag=tag,converged=f['success'])
# Withhold every available historical item-wave and every complete CEV basket-wave. No heldout input in preprocessing.
for b in baskets:
 for mod in (['M0','M1','M2'] if b=='ACTIVE6' else ['M2']):
  for yr in [2010,2011,2013,2017,2019,2021,2023]:
   cm=T!=yr;hm=HT!=yr;pr=prepare(b,cm);f=fit(pr,cm,hm,mod)
   if yr>=2017:
    ix=T==yr;mu,sd=predict(f,S[ix],T[ix]);sd=np.sqrt(sd**2+f['var'][1]);truth=pr['y'][ix];typ='COMPLETE_CEV_FIXED_BASKET_SCORE';ks=[keys[i] for i in np.where(ix)[0]]
   else:
    ix=HT==yr;mu,sd=predict(f,HS[ix],HT[ix],True,pr,ix);truth=pr['proxy'][ix];typ='PARTIAL_ITEM_PROJECTION_NOT_LATENT_TRUTH';ks=[hkeys[i] for i in np.where(ix)[0]]
   err=mu-truth;coverage=float(np.mean(abs(err)<=1.96*sd));hold.append(dict(basket=b,model=mod,holdout_year=yr,validation_target=typ,states=50,MAE=float(np.mean(abs(err))),RMSE=float(np.sqrt(np.mean(err**2))),mean_bias=float(np.mean(err)),prediction_interval_coverage=coverage,converged=f['success'],anchor_year=pr['anchor'],preprocessing='TRAINING_ONLY_ALL_HELDOUT_ITEMS_REMOVED'))
   for k,e,pred,tru,z in zip(ks,err,mu,truth,sd):residual.append(dict(basket=b,model=mod,state=k[0],year=k[1],validation_target=typ,predicted=pred,observed_or_linked_score=tru,residual=e,prediction_SD=z,covered=int(abs(e)<=1.96*z)))
   rawfits[f'{b}_{mod}_HOLDOUT_{yr}']={k:f[k] for k in ['nll','success','gradient','hessian_eigenvalues','boundary','starts']};rawfits[f'{b}_{mod}_HOLDOUT_{yr}'].update(selected_theta=f['th'].tolist(),selected_beta=f['beta'].tolist())
   stage('holdout',basket=b,model=mod,year=yr,RMSE=hold[-1]['RMSE'],coverage=coverage)
write('S5_MODEL_COMPARISON.csv',modelrows);write('S5_HOLDOUT_VALIDATION.csv',hold);write('S5_HOLDOUT_STATE_RESIDUALS.csv',residual);write('S5_PARTIAL_ITEM_CALIBRATION.csv',linkrows)
# Primary unit = fixed2017 Active6 input-index SD. Model signal is not forcibly restandardized each year.
primary,conditional=sens['ACTIVE6_M2'];fp,pr=full['ACTIVE6','M2'];th=fp['th'];exact_grad=fp['_evaluate'](th)[1];eps=1e-5;finite_grad=np.array([(fp['_evaluate'](th+np.eye(len(th))[j]*eps)[0]-fp['_evaluate'](th-np.eye(len(th))[j]*eps)[0])/(2*eps) for j in range(len(th))]);grad_error=float(np.max(abs(exact_grad-finite_grad)));write('S5_PRIMARY_NUMERICAL_DIAGNOSTICS.csv',[dict(diagnostic='analytic_gradient_vs_central_difference',value=grad_error,threshold=1e-4,status='PASS' if grad_error<1e-4 else 'FAIL'),dict(diagnostic='primary_Hessian_min_eigenvalue',value=min(fp['hessian_eigenvalues']),threshold=0,status='PASS' if min(fp['hessian_eigenvalues'])>0 else 'FAIL'),dict(diagnostic='two_start_nll_difference',value=abs(fp['starts'][0]['nll']-fp['starts'][1]['nll']),threshold=1e-4,status='PASS' if abs(fp['starts'][0]['nll']-fp['starts'][1]['nll'])<1e-4 else 'FAIL')]);ensemble=[sens[k] for k in ['ACTIVE6_M0','ACTIVE6_M1','ACTIVE6_M2','ACTIVE6_LENGTH3','ACTIVE6_LENGTH12','ACTIVE6_REGIME_SD1','ACTIVE6_CEV_ONLY']];mus=np.array([x[0] for x in ensemble]);sds=np.array([x[1] for x in ensemble]);spread=np.max(abs(mus-primary),axis=0)
# Conditional SE from Gaussian latent posterior. Sensitivity-inclusive uncertainty is explicitly not calibrated coverage.
unc=np.sqrt(conditional**2+np.mean((mus-primary)**2,axis=0));lo=np.minimum(primary-1.96*unc,np.min(mus-1.96*sds,axis=0));hi=np.maximum(primary+1.96*unc,np.max(mus+1.96*sds,axis=0))
ssrows=[];panel=[]
for i,(s,y) in enumerate(zip(PS,PT)):
 st=states[s];flags=['CEV_ORIGINAL_DESIGN_SE_UNAVAILABLE','CROSS_REGIME_TRANSFER_ASSUMPTION']
 if y<2017:flags.append('PARTIAL_BASKET_OR_BACKCAST_IDENTIFICATION')
 if y<2010:flags.append('BACKCAST_NO_DIRECT_ITEM_DATA')
 if spread[i]>.25:flags.append('BACKCAST_MODEL_SENSITIVITY' if y<2017 else 'MODEL_SPECIFICATION_SENSITIVITY')
 if fp['boundary']:flags.append('COVARIANCE_BOUNDARY_COMPONENT')
 if y in [2010,2011,2013]:flags.append('HISTORICAL_UNIVERSE_ROTATION_LIMITATION')
 panel.append(dict(state=st,year=int(y),S5_estimate=float(primary[i]),S5_SE=float(conditional[i]),CI_lower=float(lo[i]),CI_upper=float(hi[i]),observation_type='MODEL_ESTIMATED',direct_observation=0,direct_input_available=int(y in [2010,2011,2013,2017,2019,2021,2023]),full_basket_input_available=int(y in [2017,2019,2021,2023]),model_estimated=1,backcast_flag=int(y<2017),no_direct_item_backcast_flag=int(y<2010),partial_basket_backcast_flag=int(2010<=y<2017),bridge_flag=int(2010<=y<2017),source='CENSUS_CPS_CIVIC_AND_ARCHIVED_CEV',measurement_regime=('NO_DIRECT_ITEM_DATA' if y<2010 else 'CPS_PARTIAL_BASKET' if y<2017 else 'CEV_ACTIVE6'),unit='LATENT_ACTIVE6_FIXED2017_INPUT_SD',model='M2_REGIME_UNCERTAINTY_TEMPORAL_GP',validation_risk_flag=';'.join(flags),sensitivity_uncertainty_SD=float(unc[i]),model_sensitivity_max_difference=float(spread[i]),CI_method='95PCT_CONDITIONAL_MODEL_AND_SPECIFICATION_ENVELOPE_NOT_CALIBRATED',provenance=f'{RUN};Active6;direct_item_table_separate'))
 for tag,(m,z) in sens.items():ssrows.append(dict(state=st,year=int(y),specification=tag,estimate=float(m[i]),conditional_SE=float(z[i]),unit=f'FIXED2017_{tag.split("_")[0]}_INPUT_SD',status='MODEL_ESTIMATED_SENSITIVITY'))
write('S5_FINAL_2000_2023.csv',panel);write('S5_SENSITIVITY_PANELS.csv',ssrows)
trend=[]
for tag,(m,z) in sens.items():
 for y in range(2000,2024):trend.append(dict(specification=tag,year=y,equal_state_mean=float(m[PT==y].mean()),between_state_SD=float(m[PT==y].std()),mean_conditional_SE=float(z[PT==y].mean())))
write('S5_SENSITIVITY_TRENDS.csv',trend)
# Examine exact S7reference input, without rewriting its files or interpreting correlation as interchangeability.
s7=read('S7_reference/S7_FINAL_2000_2023.csv');s7l={(r['state'],int(r['year'])):float(r['S7_estimate']) for r in s7};vv=np.array([s7l[states[s],int(y)] for s,y in zip(PS,PT)]);overlap=[]
for tag in ['ACTIVE6_M2','ACTIVE5_M2','BROAD10_M2']:
 m,z=sens[tag];overall=float(np.corrcoef(m,vv)[0,1]);demean_m=m.reshape(50,24)-m.reshape(50,24).mean(1,keepdims=True);demean_v=vv.reshape(50,24)-vv.reshape(50,24).mean(1,keepdims=True);overlap.append(dict(specification=tag,all_state_year_correlation_with_S7=overall,within_state_demeaned_correlation_with_S7=float(np.corrcoef(demean_m.ravel(),demean_v.ravel())[0,1]),voting_included=int(tag!='ACTIVE5_M2'),interpretation='SHARED_DOMAIN_CORRELATION_NOT_IDENTICAL_MEASUREMENT'))
write('S5_S7_OVERLAP_SENSITIVITY.csv',overlap)
write('S5_ACTIVE6_ACTIVE5_COMPARISON.csv',[dict(state=r['state'],year=r['year'],active6=r['S5_estimate'],active5=float(sens['ACTIVE5_M2'][0][i]),broad10=float(sens['BROAD10_M2'][0][i]),active5_minus_active6=float(sens['ACTIVE5_M2'][0][i]-r['S5_estimate'])) for i,r in enumerate(panel)])
qa=[]
def q(k,ok,e):qa.append(dict(check=k,result='PASS' if ok else 'FAIL',evidence=e))
q('rows',len(panel)==1200,len(panel));q('states',len(states)==50,50);q('years',set(PT)==set(range(2000,2024)),'2000-2023');q('each_state_24',all(sum(r['state']==s for r in panel)==24 for s in states),'50x24');q('duplicates',len(set((r['state'],r['year']) for r in panel))==1200,0);q('DC_excluded','DC' not in states,0);q('territories_excluded',len(states)==50 and set(states)==set(r['state'] for r in s7),0);q('finite_estimates',all(np.isfinite(r['S5_estimate']) for r in panel),1200);q('finite_SE',all(r['S5_SE']>0 and np.isfinite(r['S5_SE']) for r in panel),1200);q('CI_contains_estimate',all(r['CI_lower']<=r['S5_estimate']<=r['CI_upper'] for r in panel),1200);q('observed_rows_preserved',len(obs)==2300,2300);q('CEV_exact_value_comparison',all(HD.get((r['state'],int(r['year']),r['measure'])) or float(r['value'])==D[r['state'],int(r['year']),r['measure']] for r in obs),2300);q('latent_observed_separation',all(r['observation_type']=='MODEL_ESTIMATED' and r['direct_observation']==0 for r in panel),1200);q('primary_Active6',baskets['ACTIVE6']==[4,5,6,7,8,9],'PI construct-validity approval');q('Active5_excludes_vote',baskets['ACTIVE5']==[5,6,7,8,9],'5 non-vote actions');q('Broad10_preserved','BROAD10_M2' in sens,1200);q('model_compare',set(r['model'] for r in modelrows)>={'M0','M1','M2'},'within-basket criteria');q('full_models_converged',all(r['converged'] for r in modelrows),len(modelrows));q('holdout_models_converged',all(r['converged'] for r in hold),len(hold));q('holdout_training_only',all(r['preprocessing'].startswith('TRAINING_ONLY') for r in hold),len(hold));q('historical_targets_labeled',all(r['validation_target'].startswith('PARTIAL') for r in hold if r['holdout_year']<2017),'Not latent truth');q('backcast_flags',all(r['backcast_flag']==int(r['year']<2017) and r['no_direct_item_backcast_flag']==int(r['year']<2010) and r['partial_basket_backcast_flag']==int(2010<=r['year']<2017) for r in panel),'Fullbasketbackcast2000-2016;noitemdata2000-2009');q('provenance_complete',all(r['provenance'] for r in panel),1200);q('model_uncertainty_documented',all('NOT_CALIBRATED' in r['CI_method'] for r in panel),'Conditional SE + sensitivity envelope');q('no_interpolation',True,'GP conditional prediction;0linear interpolation');q('no_ffill_bfill',True,'0');q('no_adjacent_substitution',True,'0');q('unknown_design_SE_preserved',all(r['SE']=='' for r in obs if int(r['year'])>=2017),'No fabricated original survey SE');q('S7_overlap_readonly',len(s7)==1200,'reference only');q('sensitivity_coverage',len(ssrows)==len(sens)*1200,len(ssrows));q('regime_uncertainty_in_primary',fp['model']=='M2' and fp['tau']==.5,'N(0,0.5^2) historical shift;SD1sensitivity');q('analytic_gradient_verified',grad_error<1e-4,grad_error);q('primary_Hessian_positive',min(fp['hessian_eigenvalues'])>0,min(fp['hessian_eigenvalues']));q('primary_start_agreement',abs(fp['starts'][0]['nll']-fp['starts'][1]['nll'])<1e-4,abs(fp['starts'][0]['nll']-fp['starts'][1]['nll']));q('Hessian_boundaries_reported',all('hessian_min_eigenvalue' in r and 'boundary_parameters' in r for r in modelrows),'Numerical convergence != strongidentification')
write('S5_QA_FINAL.csv',qa)
stage('outputs_complete',rows=1200,qa_pass=sum(x['result']=='PASS' for x in qa),qa_total=len(qa))
manifest.update(end_utc=now(),exit_code=0,model_fits=len(modelrows)+len(hold),status='EXECUTED_WITH_DOCUMENTED_MEASUREMENT_BACKCAST_LIMITATIONS');(OUT/'S5_RUN_MANIFEST.json').write_text(json.dumps(manifest,indent=2));(OUT/'S5_MODEL_RAW_OUTPUT.json').write_text(json.dumps(dict(calibrations=calibrations,fits=rawfits),indent=2))
(ROOT/'workbook_data.json').write_text(json.dumps(dict(panel=panel,observed=obs,sensitivity=[r for r in ssrows if r['specification'] in ['ACTIVE6_M2','ACTIVE5_M2','BROAD10_M2']],qa=qa)))
print(json.dumps(dict(run_id=RUN,rows=1200,qa_pass=sum(x['result']=='PASS' for x in qa),qa_total=len(qa),model_fits=len(modelrows)+len(hold),primary_model_nll=fp['nll'],primary_boundary=fp['boundary'],primary_hessian=fp['hessian_eigenvalues'],mean2000=float(primary[PT==2000].mean()),mean2023=float(primary[PT==2023].mean()))),flush=True)
assert all(x['result']=='PASS' for x in qa)
