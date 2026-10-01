# S2 2009 Census API direct estimates
2009 direct extraction and specified QA: COMPLETE. S2 entire 2000–2023 panel is not complete.
Source: https://api.census.gov/data/2009/cps/civic/nov
Run ID: S2_2009_20261001T100647Z
Execution UTC: 2026-10-01T10:06:47.055415+00:00 to 2026-10-01T10:07:11.580284+00:00
Execution KST: 2026-10-01 19:06:47 to 19:07:11
Code SHA256: 0f9a415d522f0e33d74c5f1b121007ea1edf5107b04d3ad364828863182f3b7c
Exit code: 0; QA 16/16 PASS.
Raw API input: respondents_2009.json, 1,683,471 bytes, 21,226 records.
Input SHA256: 3cd370b67bbf12bea58bfcc2edbb8ee0adfa5307a120c14cf21041571ddd0ae1
All request URLs in execution logs omit the credential. No key is included in artifacts.

## Outputs and interpretation
S2_2009_50_STATES_DIRECT.csv: exactly 50 unique states, 2009 only, DC excluded, percent units. Raw direct estimates, not harmonized values.
S2_2009_ITEM_COUNTS_50_STATES.csv: 300 rows, ANY plus five items per state; weighted Yes/No/missing counts, unweighted counts, denominators and proportions.
S2_2009_DC_QA.csv: DC separately, six measures.
S2_2009_NATIONAL_QA.csv: weighted national estimates with DC and without DC; not simple mean of state percentages.

Universe: PRTAGE>=18, HRMIS in 4/8, PRSUPINT=1, PRPERTYP=2, positive PWNRWGT. API weights are already in person units and were not divided by 10000. Raw-record weight sum matches the official population total rounded to thousands.
For individual items, Yes=1 and No=2 define valid denominators; NIU/DK/refused/N/A/missing are excluded.
ANY=1 if at least one group item is Yes; ANY=0 only if all five are No; otherwise missing. A Yes with an unknown other item remains a known participant. Missing is never recoded No.

National ANY among classified respondents: 36.1675118815% (50 states+DC) and 36.1490753282% (50 states only).
For 50 states+DC: 7,819 classified Yes, 12,988 classified No, 419 missing; weighted Yes 80,595,142.8584, weighted valid denominator 222,838,505.2376.
All-eligible denominator 227,346,149.5028 would produce a different descriptive ratio; it is not the canonical valid-response denominator.

## Validation and its limits
All five server weighted tabulations were compared with locally calculated Yes/No counts: 102 cells per item (51 state/DC areas), tolerance 0.51 persons for rounded server estimates. Extra territory rows in the API tables contain only zeros and were excluded; they are not part of the respondent data or canonical output.
External published official benchmark: Census 2009 technical documentation, Attachment13 PEQ5A unweighted frequencies and Attachment16 Illustration3 population and school/sports weighted Yes counts. Frequencies match exactly; weighted totals match within 500 persons for publication rounding.
Official documentation: https://www2.census.gov/programs-surveys/cps/techdocs/cpsnov09c.pdf
Published school 15.1% and sports 9.7% use all-eligible population; computed canonical item proportions use valid Yes/No responses, so these different denominators are explicitly distinguished.
No independent same-year same-denominator ANY percentage benchmark was verified. External validation does not claim such a comparison. Opportunity Index two-year pooled benchmarks were excluded.
QA.json contains each actual check and observed comparison, authenticated_execution_log.json contains input/output hashes, request timestamps and stage logs.

## Raw bytes and reproduction
The complete exact raw API response is losslessly archived as four respondents_2009.json.gz.b64.partNN files. Run restore_raw.py to join, decode and decompress, then verify the manifest SHA256.
The full variable metadata is publicly retrievable at https://api.census.gov/data/2009/cps/civic/nov/variables.json ; verified_variables.json preserves the required variable definitions. Metadata response SHA256: ceb4aa5eb2b1f6d91b403684b35f720e6f7c9f323b26153b49173c45f3fa9518.
extract_2009.py is the exact successfully executed code. An authenticated rerun requires a key provided locally at /tmp/s2-2009-private/key. This path is a runtime input, not a repository file.
An initial server-table comparison failed because of API zero-only territory rows; the successful version explicitly validates and skips them. No failed result was used as the final result.

Only 2009 artifacts were added. Existing CEV data and other years were not modified. STOP after saving and remote verification.
