# DDB Acquisition Route Decision — 2026-09-24

## Verified facts
1. Putnam's public DDB archive contains the historical release, not the post-1998 proprietary files.
2. Post-1998 DDB Life Style microdata definitely existed and were used in peer-reviewed research through at least 2006.
3. Chris Herbst explicitly credits Chris Callahan at DDB Needham for providing 1999-2005 Life Style Survey data.
4. Other research credits DDB-Chicago personnel including Chris Callahan and Marty Horn for direct data access.
5. Published work using these data states that respondent state of residence is present and uses state fixed effects / state-year variables.
6. A 2023 secondary analysis reports being unable to obtain the 1999-2005 DDB data, confirming that these files are not simply available from Putnam's public download.

## Decision
Status of P11/P12/P14:
DATA_EXISTED_AND_STATE_GEOGRAPHY_EXISTED, BUT PUBLIC_MICRODATA_NOT_LOCATED.

This is an access problem, not a construct problem and not a state-geography problem.

## Acquisition hierarchy
A. Search replication repositories / author deposits for legally redistributable 1999-2006 DDB files.
B. Search institutional repositories tied to published users of the data.
C. If A/B fail, pursue a direct academic-data request to DDB Worldwide for only the required variables and years:
   YEAR, state, survey weight, P11 visfrd, P12 enthome, P14 most-people-honest, plus sampling/design fields needed for state estimation.
D. If DDB cannot release microdata, request state-year weighted tabulations for those exact items.
E. If neither microdata nor exact tabulations are obtainable, strict layer records missing values; modern substitutes remain outside strict replication.

## Non-negotiable
Do not reconstruct state-year observations from published regression coefficients, figures, or approximate chart readings.
Do not label a modern similar question as strict Putnam.
