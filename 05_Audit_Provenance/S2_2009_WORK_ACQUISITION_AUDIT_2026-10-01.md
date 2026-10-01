# S2 2009 acquisition and specification audit
Date: 2026-10-01
Status: PARTIAL — RAW MICRODATA NOT ACQUIRED; ENGINE NOT EXECUTED
Scope: 2009 only. User explicitly authorized starting 2009 while 2008 remains incomplete.
No state estimates, national estimates, imputation, or panel updates were produced.

## Verified official sources
- Census technical documentation: https://www2.census.gov/programs-surveys/cps/techdocs/cpsnov09c.pdf
  Retrieved HTTP 200, 731525 bytes; SHA256 8d3d23ba195b76e5ee340f3c656db1fe727017d0c9e7d18f56e6bb12bb3193ad.
- Census API variable metadata: https://api.census.gov/data/2009/cps/civic/nov/variables.json
  Retrieved HTTP 200, 416684 bytes; SHA256 ceb4aa5eb2b1f6d91b403684b35f720e6f7c9f323b26153b49173c45f3fa9518.
These are documentation/metadata, not respondent microdata. Local downloads are temporary working copies; this committed audit records their hashes and retrieval evidence.

## 2009 specification
The supplement covers civilian noninstitutional people age 18 or older in outgoing rotation households, two of eight rotation groups. This differs from the 2008 age-15+ design. Official full-file specification: 152658 logical records, 990-character record length.

Fixed-width positions are 1-based, inclusive:
| Field | Position | Role |
|---|---|---|
| GESTFIPS | 93–94 | State |
| PEAGE | 122–123 | Raw-file age; API field is PRTAGE |
| HRMIS | 63–64 | Month-in-sample; outgoing groups 4/8 |
| PRPERTYP | 161–162 | Person type; adult civilian = 2 |
| PEQ5A | 957–958 | School/neighborhood/community association |
| PEQ5B | 959–960 | Service/civic organization |
| PEQ5C | 961–962 | Sports/recreation organization |
| PEQ5D | 963–964 | Religious organization, excluding service attendance |
| PEQ5E | 965–966 | Other organization |
| PRSUPINT | 979–980 | Supplement interview = 1 |
| PWNRWGT | 981–990 | Supplement weight |

Before calculating, verify actual record lengths, population filters, weight storage scale, and all field distributions against the dictionary. An existing multi-year script was inspected but not executed; its complete-case rule must not override the project rule below.

S2 rule: any of five responses = 1 (yes) gives participant=1; all five = 2 (no) gives participant=0; remaining patterns are missing. Negative response codes (-1 NIU, -2 don't know, -3 refused, -9 N/A) are not zero. Denominator uses positive valid supplement weights among classified eligible interviews. Compute 50 states; retain DC separately for national QA. No interpolation, carry-forward, neighbor-year substitution, or pooled-year substitution.

Official unweighted PEQ5A tally for acquisition QA: yes 3227, no 17630, don't know 70, refused 243, no response 56. This is a single-item frequency, not the five-item S2 percentage.

## Observed acquisition results
| Endpoint | Observed result |
|---|---|
| https://www2.census.gov/programs-surveys/cps/datasets/2009/supp/ | HTTP 200 directory; jan09pub.zip, jan09rep.zip, oct09pub.zip listed; no civic file observed |
| https://www2.census.gov/programs-surveys/cps/datasets/2009/supp/nov09pub.zip | HTTP 404 (candidate path, not a verified published link) |
| https://data.nber.org/cps/cpsnov09c.zip | HTTP 403 |
| https://data.nber.org/cps/cpsnov09.zip | HTTP 403 (candidate alternate name) |
| https://www.icpsr.umich.edu/web/ICPSR/studies/29881/datasets/1/download/zip | HTTP 403 |
| https://api.census.gov/data/2009/cps/civic/nov?get=GESTFIPS,PEQ5A,PWNRWGT&for=state:01 | HTTP 200, 8531 bytes, HTML title Missing Key; not data |

Public NBER index and supplements page were accessible, but no nov09 link was found in their fetched HTML. Library title searches for 29881 and 2009 CPS returned no matches; this does not prove file absence.

## Benchmark exclusion
Opportunity Index 2013 methods explicitly use pooled CPS years: 2011 index uses 2008+2009; 2012 uses 2009+2010; 2013 uses 2010+2011.
Source: https://opportunityindex.org/wp-content/uploads/2013/08/OppIndex2013FINALMethodsSources-2.pdf
These values must not be used as 2009 single-year estimates or direct single-year national validation.

## Completion gate / required input
Acquire actual ICPSR 29881 respondent data (not a documentation-only ZIP), the original Census fixed-width file, or an IPUMS CPS November 2009 civic extract with YEAR, MONTH, STATEFIP, AGE, CESUPPWT, CEORGCOM, CEORGCIV, CEORGSPORT, CEORGRELIG, CEORGOTHER and sample/person/interview identifiers needed for universe checks.
Preserve raw bytes and SHA256; run a 2009-only extraction; verify sample/response counts, weighted denominator and DC QA; save state output, code and logs; then assess COMPLETE. No COMPLETE claim is supported now.
