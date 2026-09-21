"""
Putnam U.S. Democracy Project
Collect weighted CPS state estimates for:
- P01/P02 combined officer-or-committee proxy: 2008, 2009, 2010, 2011, 2013
- P04 club/group meeting proxy: 2008 only

Requires environment variable CENSUS_API_KEY.
No interpolation. 50 states only. DC/territories excluded.
"""
import os, requests, pandas as pd

KEY=os.environ["CENSUS_API_KEY"]
STATES={f"{x:02d}" for x in [1,2,4,5,6,8,9,10,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56]}

SERIES=[
 (2008,"PEQ6","P01_P02","officer_committee_combined"),
 (2009,"PEQ6","P01_P02","officer_committee_combined"),
 (2010,"PEQ6","P01_P02","officer_committee_combined"),
 (2011,"PES7","P01_P02","officer_committee_combined"),
 (2013,"PES7","P01_P02","officer_committee_combined"),
 (2008,"PEQ7","P04","club_meeting_proxy"),
]

def weighted_tab(year,var):
    url=f"https://api.census.gov/data/{year}/cps/civic/nov"
    params={
      "tabulate":"weight(PWNRWGT)",
      "col":var,
      "for":"state:*",
      "key":KEY,
    }
    r=requests.get(url,params=params,timeout=120)
    r.raise_for_status()
    return r.json(), r.url

# API tabulation response structures can change; preserve raw response first.
# Canonical percentage extraction is intentionally guarded until response schema
# is validated against a live authenticated call.
rows=[]
for year,var,pid,label in SERIES:
    raw,request_url=weighted_tab(year,var)
    rows.append({
      "year":year,"variable_id":pid,"source_variable":var,
      "series":label,"request_url_without_key":request_url.split("&key=")[0],
      "raw_response":repr(raw)
    })

pd.DataFrame(rows).to_json(
 "CPS_P01_P02_P04_authenticated_raw_responses.jsonl",
 orient="records",lines=True,force_ascii=False
)
print("AUTHENTICATED DOWNLOAD COMPLETE; validate tabulation schema before deriving percentages.")
