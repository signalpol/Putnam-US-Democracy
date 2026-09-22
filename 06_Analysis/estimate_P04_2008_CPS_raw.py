"""P04 Club Meetings proxy — 2008 CPS Civic Engagement only.
PEQ7: attended a meeting of any group or organization in last 12 months.
1 Yes / 2 No; negative codes excluded. PWNRWGT. 50 states only.
No interpolation; P07 public meeting must never substitute for P04.
"""
import pandas as pd
FIPS={1,2,4,5,6,8,9,10,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56}

def estimate(df,state_col,var="PEQ7",weight="PWNRWGT"):
    required={state_col,var,weight}
    if not required.issubset(df.columns):
        raise ValueError(f"Not 2008 Civic supplement; missing {sorted(required-set(df.columns))}")
    x=df[[state_col,var,weight]].copy()
    x=x[x[state_col].isin(FIPS)&x[var].isin([1,2])&x[weight].notna()&(x[weight]>0)]
    x["wy"]=x[weight]*(x[var]==1)
    z=x.groupby(state_col).agg(weighted_yes=("wy","sum"),weighted_total=(weight,"sum"),n=(var,"size")).reset_index()
    z["p04_meeting_share"]=z.weighted_yes/z.weighted_total
    assert z[state_col].nunique()==50
    z["year"]=2008
    z["variable_id"]="P04"
    z["proxy_flag"]="PROXY"
    z["no_interpolation"]=True
    return z
