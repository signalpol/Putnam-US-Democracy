#!/usr/bin/env python3
"""Fast preflight before long acquisition runs. Does not download large datasets."""
import os,sys,importlib.util,json,requests
checks={}
for pkg in ("pandas","requests","openpyxl","xlrd"):
    checks["pkg_"+pkg]="PASS" if importlib.util.find_spec(pkg) else "FAIL"
checks["BEA_API_KEY"]="PASS" if os.getenv("BEA_API_KEY") else "MISSING"
checks["CENSUS_API_KEY"]="PASS" if os.getenv("CENSUS_API_KEY") else "OPTIONAL_PUBLIC_MODE"
checks["BLS_API_KEY"]="PASS" if os.getenv("BLS_API_KEY") else "OPTIONAL_UNREGISTERED_MODE"
urls={
"CENSUS_2000_2010":"https://www2.census.gov/programs-surveys/popest/tables/2000-2010/intercensal/state/st-est00int-01.xls",
"CENSUS_2010_2020":"https://www2.census.gov/programs-surveys/popest/tables/2010-2020/intercensal/national/nst-est2020int-pop.xlsx",
"CENSUS_2020_2023":"https://www2.census.gov/programs-surveys/popest/datasets/2020-2023/state/totals/NST-EST2023-ALLDATA.csv",
"BERKELEY_SDI2":"https://democracypolicylab.berkeley.edu/wp-content/uploads/2025/01/SDI_2.0.csv",
"NCCS_P08_SAMPLE":"https://nccsdata.s3.us-east-1.amazonaws.com/processed/bmf-legacy/2020_04/bmf_legacy_2020_04_processed.csv"}
for k,u in urls.items():
    try:
        r=requests.head(u,timeout=20,allow_redirects=True,headers={"User-Agent":"Putnam-US-Democracy/1.0"})
        checks[k]={"status":"PASS" if r.status_code<400 else "FAIL","http":r.status_code,
                   "content_length":r.headers.get("content-length"),"content_type":r.headers.get("content-type")}
    except Exception as e: checks[k]={"status":"FAIL","reason":str(e)}
# Missing BEA key is an execution blocker for E1/E2/E5 but not for public-source D/S collectors.
checks["PUBLIC_SOURCE_PREFLIGHT"]="PASS" if all(checks[k]["status"]=="PASS" for k in urls) and all(checks["pkg_"+p]=="PASS" for p in ("pandas","requests","openpyxl","xlrd")) else "FAIL"
checks["FULL_PIPELINE_CREDENTIALS"]="PASS" if checks["BEA_API_KEY"]=="PASS" else "MISSING_BEA_KEY"
print(json.dumps(checks,indent=2))
sys.exit(0 if checks["PUBLIC_SOURCE_PREFLIGHT"]=="PASS" else 2)
