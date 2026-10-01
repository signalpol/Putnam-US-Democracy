# 2009 S2 Census Microdata API execution source
Primary source: https://api.census.gov/data/2009/cps/civic/nov
The user authorized replacing raw-file acquisition with Census API execution. ICPSR/NBER failures are no longer the acquisition blocker.
Status: PARTIAL. API acquisition probe EXECUTION FAILED (exit code 2); estimation ENGINE NOT EXECUTED. No estimates were created and no other years changed.

Run ID: S2_2009_CENSUS_API_20261001T095610Z
Start UTC: 2026-10-01T09:56:10.831481+00:00
End UTC: 2026-10-01T09:56:46.525028+00:00
Code SHA256: 708471cdf862b63eded8a59f6ca24284b919782919594e1771239b20ec017729

## Verified variables
Metadata request succeeded (HTTP 200 JSON). PEQ5A–PEQ5E, GESTFIPS, PRTAGE, HRMIS, PRSUPINT, PRPERTYP and PWNRWGT exist. PWNRWGT is marked is-weight. Q5 response codes: 1 Yes, 2 No, -1 NIU, -2 DK, -3 refused, -9 N/A.
Metadata input SHA256: ceb4aa5eb2b1f6d91b403684b35f720e6f7c9f323b26153b49173c45f3fa9518
The selected metadata is saved in verified_variables.json; full source URL and response hash are in execution_log.json.

## Actual no-key execution
One raw-record GET and five tabulate=weight(PWNRWGT) calls ran with NO key parameter.
All six returned HTTP 200 text/html, 8531 bytes, title Missing Key; response SHA256 c2f4687e09b80676de7f68dec92ebea395209616dbc6f895520e547c5f68c0f5.
raw_eligible_no_key.response preserves those identical response bytes.
No Census credential variable was found in the execution environment.
HTTP 200 is not a successful data acquisition when the response is an authentication-error HTML page.
The Census official Microdata API guide explicitly requires an API key for all data queries:
https://www2.census.gov/data/api-documentation/microdata-api-user-guide.pdf (API Key, page 5).
Free key registration: https://api.census.gov/data/key_signup.html

## Required estimation after authenticated access
Universe: civilian age18+, HRMIS 4/8, PRSUPINT=1, PRPERTYP=2; positive valid PWNRWGT.
Per item: weighted Yes and No counts and Yes/(Yes+No), excluding negative/missing codes.
Any participation: classify as 1 if at least one item is Yes; as 0 if all five are No; otherwise missing. Missing responses are never coded No. Retain counts/weights excluded under this rule. Marginal item counts alone cannot determine the union because group memberships overlap; retrieve joint responses or equivalent joint tabulations.
Canonical output must contain exactly 50 states, excluding DC; retain DC only separately for national QA.
Validate API weight scaling, universe/response frequencies, denominators, item proportions and any-participation bounds before publishing results.
The 2008+2009 Opportunity Index pooled estimate is not a valid 2009-only benchmark.
External benchmark QA NOT EXECUTED, because there is no estimated value to compare.
Acquire and use an activated Census API key; do not substitute raw-file failures or invented state values. Complete only 2009, save verified results, then STOP.

## Artifact scope
probe.py is an acquisition-only probe, not an executed estimation engine.
execution_log.json records actual URLs, timestamps, HTTP results, hashes and exit code.
No state data CSV or model results are present in this package.
