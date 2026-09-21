"""State weighted estimates for Putnam P01/P02 combined CPS proxy.
Waves: 2008-2011, 2013. No interpolation. 50 states only; exclude DC/territories.
Output is an auxiliary combined proxy, NEVER duplicated into canonical P01 and P02.
"""
import pandas as pd
STATE_FIPS={1,2,4,5,6,8,9,10,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56}
WAVES={2008:"PEQ6",2009:"PEQ6",2010:"PEQ6",2011:"PES7",2013:"PES7"}

def estimate_yes_share(df,state_col,var,weight_col="PWNRWGT"):
    x=df[[state_col,var,weight_col]].copy()
    x=x[x[state_col].isin(STATE_FIPS)]
    x=x[x[var].isin([1,2]) & x[weight_col].notna() & (x[weight_col]>0)]
    x["wy"]=x[weight_col]*(x[var]==1)
    out=x.groupby(state_col).agg(weighted_yes=("wy","sum"),weighted_total=(weight_col,"sum"),n=(var,"size")).reset_index()
    out["officer_committee_combined_share"]=out.weighted_yes/out.weighted_total
    assert out[state_col].nunique()==50, f"Expected 50 states, got {out[state_col].nunique()}"
    return out

def validate_wave(year,var):
    assert WAVES[year]==var, f"Unexpected mapping {year}:{var}"

# Raw layouts:
# 2008 PEQ6 983-984
# 2009 PEQ6 967-968
# 2010 PEQ6 967-968
# 2011 PES7 969-970
# 2013 PES7 969-970
# Valid substantive responses: 1 Yes, 2 No. Negative codes excluded.
