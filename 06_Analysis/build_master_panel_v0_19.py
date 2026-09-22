"""Build canonical Putnam 50-state x 2000-2023 master panel v0.19.
Never infer canonical P numbers from legacy filenames.
No interpolation. Structural and survey non-wave missingness preserved.
"""
import pandas as pd
BASE="02_Putnam_14_Variables/"
LEGACY={
 "PUTNAM_01_PublicMeeting.csv":"P07",
 "PUTNAM_02_GroupMembership.csv":"P05",
 "PUTNAM_03_Volunteering.csv":"P10",
 "PUTNAM_04_CommunityActivity.csv":"P09",
 "PUTNAM_05_PresidentialTurnout.csv":"P06",
 "PUTNAM_06_NonprofitDensity.csv":"P08",
}
OPTIONAL={
 "P03_Civic_Social_Organization_Density_2000_2023.csv":("P03","p03_density_per_1000"),
 "P01_P02_Officer_Committee_Combined_Proxy.csv":("P01_P02_COMBINED","officer_committee_combined_share"),
 "P04_Club_Meetings_2008.csv":("P04","p04_meeting_share"),
 "P11_Visiting_Friends_CPS.csv":("P11","p11_proxy_score_1_to_6"),
}
KEY=["state_fips","state_abbr","state_name","year"]

def load_legacy(path,pid):
    x=pd.read_csv(BASE+path,dtype={"state_fips":str})
    x["state_fips"]=x.state_fips.str.zfill(2)
    assert len(x)==1200 and not x.duplicated(["state_fips","year"]).any()
    return x[KEY+["value","missing_status"]].rename(
        columns={"value":pid,"missing_status":pid+"_status"})

def build():
    panel=None
    for f,pid in LEGACY.items():
        x=load_legacy(f,pid)
        panel=x if panel is None else panel.merge(x,on=KEY,how="outer",validate="one_to_one")
    assert len(panel)==1200
    # Canonical placeholders: never fabricate unavailable observations.
    for pid in ["P01","P02","P03","P04","P11","P12","P13","P14"]:
        if pid not in panel: panel[pid]=pd.NA
        panel[pid+"_status"]="STRUCTURAL_MISSING" if pid in ["P12","P13","P14"] else "PENDING_EXECUTION"
    # P01/P02 remain individually missing even when combined auxiliary proxy becomes available.
    panel["P01_P02_COMBINED"]=pd.NA
    panel["P01_P02_COMBINED_status"]="PENDING_EXECUTION"
    cols=KEY+sum(([p,p+"_status"] for p in [f"P{i:02d}" for i in range(1,15)]),[])+[
        "P01_P02_COMBINED","P01_P02_COMBINED_status"]
    panel=panel[cols].sort_values(["state_fips","year"])
    assert len(panel)==50*24
    panel.to_csv("Putnam_US_Democracy_Master_Panel_v0_19.csv",index=False)
    return panel

if __name__=="__main__":
    p=build()
    print("OK",p.shape)
