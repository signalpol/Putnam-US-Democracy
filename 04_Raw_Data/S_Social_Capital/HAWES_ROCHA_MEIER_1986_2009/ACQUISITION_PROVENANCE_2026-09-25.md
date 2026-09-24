# Hawes SPPQ numeric-data acquisition provenance — 2026-09-25

## Canonical identifiers
- SPPQ replication DOI: 10.15139/S3/SMKJFZ
- Numeric file named by archived SPPQ inventory: HawesSPPQ_ReplicationData.tab
- Archived replication Stata file: HawesSPPQ_ReplicationFile_V2.do
- Social-capital variable used by the replication: SC8609_ma
- Panel keys declared by authors' replication code: fips year

## Independent public derivative confirmation
CauSciBench identifies its converted CSV as hawes_social_capital.csv and documents the source study as 1986–2009, with SC8609_ma = Social Capital Index. Its replication code uses statename as panel entity and year as time.

## Acquisition status
- Authors' Stata replication code: ACQUIRED and stored in this repository.
- Exact numeric tab file: exact filename and DOI located, but byte-level acquisition is still pending because the legacy Dataverse host is not serving the file through the current retrieval path.
- Do NOT mark the numeric data ACQUIRED until bytes are fetched and row/key validation is completed.

## CauSciBench metadata record
```csv
119,"Social capital, racial context, and incarcerations in the American states","""This study examines the differential effects of social capital on policy equity in state outcomes between 1986 and 2009. Specifically, it explores the relationship between social capital and incarceration rates in the American states paying particular attention to racial disparities in incarceration rates. State-level incarceration rates from 1986 to 2009 were obtained from the Bureau of Justice Statistics’ National Prisoners Statistics study. social capital is measured using an index created by Hawes, Rocha, and Meier (2013) using factor analysis of 22 items that capture the behavioral components of social capital. This index primarily relies on state-level data from a market research firm (MediaMark, Inc.) that conducts large annual surveys that include items related to organizational membership, volunteerism, and civic engagement.

Data Variables:
statename: State Name
year: Year
fips: FIPS State Code
fipsyear: FIPS Code + Year
VCRate_Total: Total Violent Crimes per 100,000 population
PCRate_Total: Total Property Crimes per 100,000 population
divorcerate: Divorce per 1,000 population
women_leg: Percent Females in State Legislature
SC8609_ma: Social Capital Index
pop_pctblk: Percent Black Population
felonspc: Voting-Ineligible Felons per 100,000
bwpovratio: Poverty Inequality (Black/White Ratio)
bwcolratio: Education Inequality (Black/White Ratio)
pov_rtfull: Poverty Rate
unemp: Unemployment Rate
govideo: Government Ideology
totdempct: Proportion of Democrats in Entire Legislature
racialdiversity: Racial Diversity (Blau Index)
gsppc_k: GSP per Capita (in 2007 $1000)
eduattain_ma: Percent with College Degree
SC_RD: Social Capital X Racial Diversity
jprison_totalrt: Total Inmates per 100,000 population
prison_whtrt: White Inmates per 100,000 population
prison_blkrt: Black Inmates per 100,000 population
prison_BWratio: Black/White Incarceration Ratio
ln_prison_BWratio: Logged Black/White Incarceration Ratio
ln_pctblk: Logged Percent Black Population
ln_SC_PBLK: Social Capital X ln(% Black)
threestrikes: Three Strikes Law (Yes/No)
GTClear: Trial Court Clearance Rate
darrest2: Drug Arrests / Population
blk_leg: Percent African Americans in State Legislature""",hawes_social_capital.csv,"Does an increase in social capital increase the ratio of Black/White prisoners, while accounting for other relevant factors?",did,1.038,0.415,SC8609_ma,prison_BWratio,"VCRate_Total,PCRate_Total,divorcerate,women_leg,pop_pctblk,felonspc,bwpovratio,bwcolratio,unemp,racialdiversity,govideo,threestrikes,blk_leg,totdempct,eduattain_ma,SC_RD",,,year,statename,,0,0
```
