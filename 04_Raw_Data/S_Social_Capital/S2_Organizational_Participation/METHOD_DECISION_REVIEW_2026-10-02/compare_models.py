"""Bounded Gaussian-process comparison on inherited direct observations.
No interpolation or source-value replacement. Outputs are diagnostic, not final.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import csv,json,hashlib,datetime,time,pathlib
import numpy as np
from scipy.linalg import cho_factor,cho_solve
from scipy.optimize import minimize
from scipy.special import expit,logit
ROOT=pathlib.Path(__file__).resolve().parent
OUT=ROOT/'diagnostics';OUT.mkdir(exist_ok=True)
rows=list(csv.DictReader(open(ROOT/'inputs/canonical_base.csv')))
states=sorted({r['state'] for r in rows});si={s:i for i,s in enumerate(states)}
s=np.array([si[r['state']] for r in rows]);t=np.array([int(r['year']) for r in rows]);p=np.array([float(r['s2_participation']) for r in rows]);y=logit(p)
v=np.array([(float(r['s2_se'])/(float(r['s2_participation'])*(1-float(r['s2_participation']))))**2 if r['s2_se'] else 0 for r in rows])
missing=np.array([not r['s2_se'] for r in rows])
def design(tt,m):
    return np.column_stack([np.ones(len(tt)),(tt-2013)/10]+([(tt>=2017).astype(float)] if m=='M2' else []))
def kernel(ss,tt,ss2,tt2,theta,m):
    same=ss[:,None]==ss2[None,:];distance=abs(tt[:,None]-tt2[None,:]);a,e,qs,qc=np.exp(theta)
    k=a*a*same
    if m!='M0':k=k+qs*qs*same*np.exp(-distance/6)+qc*qc*np.exp(-distance/6)
    return k
def fit(mask,m):
    ss,tt,yy=s[mask],t[mask],y[mask];xx=design(tt,m)
    def evaluate(th,details=False):
        k=kernel(ss,tt,ss,tt,th,m)+np.diag(v[mask]+np.exp(th[1])**2*missing[mask]+1e-8)
        try:
            c=cho_factor(k,lower=True);ix=cho_solve(c,xx);iy=cho_solve(c,yy);bc=np.linalg.inv(xx.T@ix);beta=bc@(xx.T@iy);r=yy-xx@beta;alpha=cho_solve(c,r)
            nll=.5*(r@alpha+2*np.log(np.diag(c[0])).sum()+len(yy)*np.log(2*np.pi))
            if details:return dict(theta=th,beta=beta,bc=bc,c=c,alpha=alpha,ss=ss,tt=tt,xx=xx,nll=nll)
            return nll
        except np.linalg.LinAlgError:return 1e20
    bounds=[(-5,1),(-7,-.5),(-6,0),(-6,0)]
    if m=='M0':bounds[2]=(-12,-12);bounds[3]=(-12,-12)
    opts=[]
    for init in [[-1.5,-2.6,-2.4,-2.4],[-1.3,-3.2,-3,-1.8]]:
        opt=minimize(evaluate,init,method='L-BFGS-B',bounds=bounds,options={'maxiter':160,'ftol':1e-9});opts.append(opt)
    opt=min(opts,key=lambda z:z.fun);f=evaluate(opt.x,True);f.update(success=bool(opt.success),message=str(opt.message),gradient_max=float(max(abs(opt.jac))),model=m)
    return f
def predict(f,ss,tt,observation=False):
    m=f['model'];xx=design(tt,m);ks=kernel(ss,tt,f['ss'],f['tt'],f['theta'],m);ik=cho_solve(f['c'],ks.T);d=xx-ks@cho_solve(f['c'],f['xx']);mu=xx@f['beta']+ks@f['alpha'];vv=np.diag(kernel(ss,tt,ss,tt,f['theta'],m))-(ks*ik.T).sum(1)+np.einsum('ij,jk,ik->i',d,f['bc'],d)
    if observation:vv+=np.exp(f['theta'][1])**2
    sd=np.sqrt(np.maximum(vv,0));return expit(mu),expit(mu-1.96*sd),expit(mu+1.96*sd),mu,sd
def write(name,data):
    with open(OUT/name,'w',newline='') as h:
        w=csv.DictWriter(h,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
start=datetime.datetime.now(datetime.timezone.utc).isoformat();run='S2_MODELCOMP_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
summary=[];hold=[];pred=[];fits={}
for m in ['M0','M1','M2']:
    f=fit(np.ones(len(rows),bool),m);fits[m]=f;np_=len(f['beta'])+(2 if m=='M0' else 4)
    z={'model':m,'n':len(rows),'parameters':np_,'log_likelihood':-f['nll'],'AIC':2*np_+2*f['nll'],'BIC':np_*np.log(len(rows))+2*f['nll'],'converged':f['success'],'gradient_max':f['gradient_max'],'state_intercept_sd':np.exp(f['theta'][0]),'unknown_sampling_sd_logit':np.exp(f['theta'][1]),'state_process_sd':np.exp(f['theta'][2]),'common_process_sd':np.exp(f['theta'][3]),'trend_per_decade_logit':f['beta'][1],'CEV_offset_logit':f['beta'][2] if m=='M2' else '', 'CEV_offset_SE_logit':np.sqrt(f['bc'][2,2]) if m=='M2' else ''};summary.append(z)
    ss=np.repeat(np.arange(50),24);tt=np.tile(np.arange(2000,2024),50);pp,ll,uu,mm,sd=predict(f,ss,tt)
    for i in range(len(tt)):pred.append(dict(model=m,state=states[ss[i]],year=int(tt[i]),estimate=pp[i],CI_lower=ll[i],CI_upper=uu[i],latent_sd_logit=sd[i],diagnostic_only=True))
    print('FIT',m,json.dumps(z),flush=True)
    for yr in [2009,2011,2013,2019,2021]:
        train=t!=yr;test=~train;ff=fit(train,m);pr,lo,hi,mu,sd=predict(ff,s[test],t[test],True)
        for j,i in enumerate(np.flatnonzero(test)):hold.append(dict(model=m,holdout_year=yr,state=rows[i]['state'],observed=p[i],predicted=pr[j],CI_lower=lo[j],CI_upper=hi[j],covered=bool(lo[j]<=p[i]<=hi[j]),residual=pr[j]-p[i],converged=ff['success'],regime_offset=ff['beta'][2] if m=='M2' else ''))
        print('HOLDOUT',m,yr,'RMSE',np.sqrt(np.mean((pr-p[test])**2)),'coverage',np.mean((lo<=p[test])&(hi>=p[test])),flush=True)
write('S2_MODEL_COMPARISON.csv',summary);write('S2_HOLDOUT_VALIDATION.csv',hold);write('S2_DIAGNOSTIC_MODEL_PREDICTIONS.csv',pred)
hs=[]
for m in ['M0','M1','M2']:
    h=[r for r in hold if r['model']==m];er=np.array([r['residual'] for r in h]);hs.append(dict(model=m,n=len(h),MAE=np.mean(abs(er)),RMSE=np.sqrt(np.mean(er*er)),mean_bias=np.mean(er),coverage=np.mean([r['covered'] for r in h])))
write('S2_HOLDOUT_SUMMARY.csv',hs)
manifest=dict(run_id=run,started_utc=start,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),input_SHA256=hashlib.sha256((ROOT/'inputs/canonical_base.csv').read_bytes()).hexdigest(),script_SHA256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),exit_status=0,models=summary,holdout_summary=hs,warning='Diagnostics only; regime identification depends on temporal prior and no cross-regime overlapping wave exists.')
(OUT/'MODEL_RUN_MANIFEST.json').write_text(json.dumps(manifest,indent=2))
