"""P11 state estimates from official CPS raw files.
No interpolation. Exclude DC/territories. Preserve regime A/B.
Primary output: weighted category shares. Derived reverse-frequency score is secondary.
"""
import pandas as pd
STATE_FIPS={1,2,4,5,6,8,9,10,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56}
VALID={1,2,3,4,5,6}

def estimate(df,state_col,value_col="PES1",weight_col="PWNRWGT"):
    x=df[[state_col,value_col,weight_col]].copy()
    x=x[x[state_col].isin(STATE_FIPS)]
    x=x[x[value_col].isin(VALID) & x[weight_col].notna() & (x[weight_col]>0)]
    g=x.groupby([state_col,value_col],as_index=False)[weight_col].sum().rename(columns={weight_col:"weighted_count"})
    t=g.groupby(state_col,as_index=False)["weighted_count"].sum().rename(columns={"weighted_count":"weighted_total"})
    g=g.merge(t,on=state_col)
    g["share"]=g["weighted_count"]/g["weighted_total"]
    # Derived score: 6=most frequent, 1=not at all. Never overwrite raw categories.
    g["reverse_score"]=7-g[value_col]
    s=(g.assign(wx=lambda z:z.weighted_count*z.reverse_score)
         .groupby(state_col).agg(wx=("wx","sum"),w=("weighted_count","sum")).reset_index())
    s["p11_proxy_score_1_to_6"]=s.wx/s.w
    assert s[state_col].nunique()==50, "Expected 50 states"
    return g,s

# Regime A: 2011/2013 raw variable PES13 at positions 975-976.
# Regime B: 2017/2019/2021/2023 raw variable PES1 at positions 1001-1002.
# Use each wave's official raw file/layout and PWNRWGT; do not interpolate non-wave years.
