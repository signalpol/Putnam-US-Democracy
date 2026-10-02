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
OUT=ROOT/'final_package';OUT.mkdir(exist_ok=True)
LENGTH=6.0
INPUT=ROOT/'inputs/canonical_base.csv'
if not INPUT.exists():INPUT=ROOT/'canonical_base.csv'
rows=list(csv.DictReader(open(INPUT)))
states=sorted({r['state'] for r in rows});si={s:i for i,s in enumerate(states)}
s=np.array([si[r['state']] for r in rows]);t=np.array([int(r['year']) for r in rows]);p=np.array([float(r['s2_participation']) for r in rows]);y=logit(p)
v=np.array([(float(r['s2_se'])/(float(r['s2_participation'])*(1-float(r['s2_participation']))))**2 if r['s2_se'] else 0 for r in rows])
missing=np.array([not r['s2_se'] for r in rows])
def design(tt,m):
    return np.column_stack([np.ones(len(tt)),(tt-2013)/10]+([(tt>=2017).astype(float)] if m=='M2' else []))
def kernel(ss,tt,ss2,tt2,theta,m):
    same=ss[:,None]==ss2[None,:];distance=abs(tt[:,None]-tt2[None,:]);a,e,qs,qc=np.exp(theta)
    k=a*a*same
    if m!='M0':k=k+qs*qs*same*np.exp(-distance/LENGTH)+qc*qc*np.exp(-distance/LENGTH)
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
    opt=min(opts,key=lambda z:z.fun);f=evaluate(opt.x,True);f['evaluate']=evaluate;f['start_results']=[dict(nll=float(o.fun),success=bool(o.success),theta=o.x.tolist()) for o in opts];f.update(success=bool(opt.success),message=str(opt.message),gradient_max=float(max(abs(opt.jac))),model=m)
    return f
def predict(f,ss,tt,observation=False):
    m=f['model'];xx=design(tt,m);ks=kernel(ss,tt,f['ss'],f['tt'],f['theta'],m);ik=cho_solve(f['c'],ks.T);d=xx-ks@cho_solve(f['c'],f['xx']);mu=xx@f['beta']+ks@f['alpha'];vv=np.diag(kernel(ss,tt,ss,tt,f['theta'],m))-(ks*ik.T).sum(1)+np.einsum('ij,jk,ik->i',d,f['bc'],d)
    if observation:vv+=np.exp(f['theta'][1])**2
    sd=np.sqrt(np.maximum(vv,0));return expit(mu),expit(mu-1.96*sd),expit(mu+1.96*sd),mu,sd
def write(name,data):
    with open(OUT/name,'w',newline='') as h:
        w=csv.DictWriter(h,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
