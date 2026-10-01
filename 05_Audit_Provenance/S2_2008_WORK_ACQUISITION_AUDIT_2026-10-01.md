# S2 2008 acquisition audit — 2026-10-01

Status: PARTIAL — ENGINE NOT EXECUTED. No state estimates were calculated. No 2009 extraction was started.

## Authorized scope
Build direct organizational-participation estimates for 50 states in 2008; exclude DC from canonical output. Preserve missing years, raw inputs, and existing outputs. No interpolation, adjacent-year substitution, or undocumented proxy substitution. Stop after 2008 for PI review.

## Independently checked evidence
The uploaded ICPSR_29644-V1(1).zip was materialized and opened. Members are the codebook, user guide, manifest, related literature, description/citation HTML and terms. There is no microdata member. The manifest lists 29644-0001-Data.dta with 150,799 records, 412 variables and MD5 51646208f6ae900787f0502652182ecf; this describes a listed file, not bytes acquired in this session.

The official Census 2008 documentation states 150,799 logical records, record length 1,014, survey universe civilian persons aged 15+, and use of PWNRWGT for supplement estimates.
Source: https://www2.census.gov/programs-surveys/cps/techdocs/cpsnov08c.pdf

IPUMS states 2008 questions were asked of age 15+, whereas subsequent available Civic Engagement samples use age 18+. CESUPPWT is the harmonized supplement weight.
Sources:
https://cps.ipums.org/cps/civic_engagement_sample_notes.shtml
https://cps.ipums.org/cps-action/variables/CESUPPWT

Census variables.json was read directly. PEQ5A through PEQ5E are the five organization items; 1=Yes, 2=No, -1=NIU, -2=Don't Know, -3=Refused, -9=N/A. PWNRWGT is marked as a weight and is the suggested weight for each item.
Source: https://api.census.gov/data/2008/cps/civic/nov/variables.json

An actual GET for GESTFIPS,PRTAGE,PEQ5A,PEQ5B,PEQ5C,PEQ5D,PEQ5E,PWNRWGT for state:01 returned HTTP 200 but HTML titled Missing Key. HTTP success is not a data acquisition success.

The repository extraction script at baseline c6e6382ca72637e25c32824f914c3edcf636123a lacks an age filter, uses complete cases for every five-item record, and executes all five historical years. It was inspected, not run. A verified any-Yes record with another item missing should be examined separately from an all-No record with missing items; a denominator rule requires explicit documentation and sensitivity checks.
Source: 06_Analysis/S2_extract_cps_2008_2013.py
Blob SHA: 91060e03b754f879ba0a63f7b9e5f7f732c032b3

## Source searches and actual access results
The Weiss et al. author publication listing was inspected. For this specific article the visible links are DOI and PDF; replication links nearby belong to other articles and cannot be attributed to this article. The manuscript says CPS data are available through IPUMS. No replication microdata were obtained.
https://krisvelasco.com/publications.html
https://pmc.ncbi.nlm.nih.gov/articles/PMC10857850/

NBER public-download candidate cpsnov08c.zip returned HTTP 403. Other candidate data formats and the dictionary request also returned 403. This does not establish that the file does not exist.
https://data.nber.org/cps/cpsnov08c.zip

Census 2008 dataset and supp directory listings were actually read. The supp listing exposed aug08pub formats, not civic microdata. Several candidate civic paths returned 404. Basic November data must not be substituted for the Civic Engagement supplement.

NCoC, Opportunity Index, Maryland Civic Health, AmeriCorps and replication-related searches were performed. No independently verified 50-state 2008 numeric table was acquired. Search results suggesting 35.1% national membership include mixed 2008/2009 reports; these are not yet accepted as single-year 2008 benchmarks.
https://ncoc.org/wp-content/uploads/2015/04/2010OhioCHI.pdf
https://dogood.umd.edu/research-impact/publications/maryland-civic-health-report-look-civic-engagement-maryland-and-us

## Concrete acquisition request
Preferred input: IPUMS CPS November 2008 extract with YEAR, MONTH, STATEFIP, AGE, CESUPPWT, CEORGCOM, CEORGCIV, CEORGSPORT, CEORGRELIG, CEORGOTHER, and identifying/sample/universe variables where available. Supply data and its generated codebook/import syntax together. Do not select other years. Do not prefilter or recode missing answers in the export.

Alternative input: actual ICPSR 29644 dataset 1 microdata, such as 29644-0001-Data.dta, with documentation. The documentation-only ZIP cannot produce estimates.

## Outstanding gates
Microdata acquisition; input hash; age/universe comparison with 2017–2023 official definition; eligibility/denominator rule; processing script and run manifest; 50-state weighted calculation; national estimate including separate DC treatment; independent single-year benchmark; reproducibility and output hash verification.

No CSV containing purported 2008 direct observations was created. No COMPLETE, VERIFIED dataset or model execution claim is made.
