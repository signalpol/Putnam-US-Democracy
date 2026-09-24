"""
Acquire Putnam's ORIGINAL 14 state-level social-capital measures.
Primary preserved copy: GitHub issue attachment cached from BowlingAlone site.
Independent live copy: ICPSR ICSC state-level dataset 00163-0002.

Fail closed: success requires actual bytes plus structural validation.
"""
from pathlib import Path
import urllib.request, hashlib, csv, json, re

OUT=Path("04_Raw_Data/Putnam_Original_State_Measures")
OUT.mkdir(parents=True,exist_ok=True)

URLS=[
 ("github_preserved","https://github.com/datasets/awesome-data/files/5396422/StateMeasures.txt"),
]
dest=OUT/"StateMeasures.txt"
errors=[]
for label,url in URLS:
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req,timeout=90) as r:
            b=r.read()
        if len(b)<1000: raise ValueError(f"implausibly small file: {len(b)} bytes")
        dest.write_bytes(b)
        source={"label":label,"url":url}
        break
    except Exception as e:
        errors.append({"label":label,"url":url,"error":repr(e)})
else:
    (OUT/"acquisition_errors.json").write_text(json.dumps(errors,indent=2))
    raise SystemExit("FAIL: no source bytes acquired")

raw=dest.read_text(errors="replace")
lines=[x for x in raw.splitlines() if x.strip()]
# Original file should be a small state-level table, not respondent microdata.
if len(lines)<40:
    raise SystemExit(f"FAIL: too few nonblank lines: {len(lines)}")

header=re.split(r"\t+|\s{2,}",lines[0].strip())
low=" ".join(header).lower()
if "state" not in low:
    raise SystemExit("FAIL: STATE field not detected in header")

# Known canonical field anchors from ICPSR instructional copy.
anchors=["soccap","lcomm"]
present={a:(a in raw.lower()) for a in anchors}
if not all(present.values()):
    raise SystemExit(f"FAIL: canonical anchors absent: {present}")

manifest={
 "status":"ACQUIRED_AND_BASICALLY_VALIDATED",
 "source":source,
 "bytes":dest.stat().st_size,
 "sha256":hashlib.sha256(dest.read_bytes()).hexdigest(),
 "nonblank_lines":len(lines),
 "header":header,
 "canonical_anchors":present,
 "independent_copy":{
   "provider":"ICPSR Investigating Community and Social Capital",
   "dataset_id":"ICSC 00163-0002",
   "legacy_sda_url":"https://www.icpsr.umich.edu/cgi-bin/SDA-ID/ICSC/hsda?icsc+00163-0002"
 }
}
(OUT/"manifest.json").write_text(json.dumps(manifest,indent=2))
print(json.dumps(manifest,indent=2))
