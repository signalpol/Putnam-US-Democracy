# S6 measurement audit — 2026-10-02

## Locked construct and existing design
The inherited RAW contains exactly1,200 count observations for NAICS813410, Civic and Social Organizations. No population denominator existed. The project registry P03 names civic/social organization density, and the earlier Research Director instruction fixes establishments/population ×1,000. This package derives that existing definition without adding industries.

S6_estimate = employer establishments in NAICS813410 / July1 resident population ×1,000. This administrative density is not a survey participation rate or a count of all informal associations. Employer locations are counted; multi-location organizations can contribute multiple establishments. Religious813110, advocacy8133, business/professional/labor/political8139 and nonemployer organizations remain outside the inherited813410 basket.

## NAICS continuity
| CBP years | Classification | Core813410 definition | Official evidence |
|---|---|---|---|
|2000–2002|1997|Member civic/social interests|Census1997 Sector81 archive, section813410|
|2003–2007|2002|SAME core definition|2002 economic census ec0281i03, AppendixB ppB2/B5|
|2008–2011|2007|SAME core definition and illustrative categories|Census2007 Definition File p549(PDFpage548)|
|2012–2016|2012|SAME core definition and illustrative categories|Census2012 Definition File pp492–493(PDFpages491–492)|
|2017–2023|2017|SAME core definition and illustrative categories|Census2017 Definition File p501(PDFpage500)|

All revisions define the class by promoting member civic/social interests. Illustrations include alumni, booster, ethnic, fraternal, grange, parent-teacher, scouting, social and veterans associations. Identical code alone was not the equivalence test: official definitions and category boundaries were compared. The official CBP methodology explicitly confirms2017–2023 uses2017NAICS;2022NAICS was not silently assigned to the2022/2023files. Full XLS crosswalk downloads were blocked403/404; definition evidence is available and this access limitation is preserved, not asserted as a successfully downloaded crosswalk.

## CBP changes and schema
StateZIP fipstate is state geography. Aggregate LFO '-' was selected once state LFO became available in2010; earlier files have no LFO field.2015 headers are uppercase and normalized only for parsing. The inherited API responses contain all-size/all-LFO aggregate selections. DC and territorial codes can occur in source files but are filtered by the inherited50-state whitelist.

2003 auxiliary-establishment treatment changed: previously non-managing auxiliaries were outside ordinary NAICS categories; subsequently they were assigned to the service industry performed. This is a real administrative comparability limitation flagged at2003; no estimated correction was applied. Establishment counts, employment and payroll are distinct fields.2007 noise infusion pertains to magnitude employment/payroll, not an invented SE on establishment totals.2017 publication requires at least3establishments; all1,200cells are published numeric counts, minimum57.2018 EMPFLAG discontinuation is not interpreted as establishment missingness. The2026 future-product noise-policy change does not revise the archived2000–2023 products used here.

## Population and normalization
All denominators are total resident population July1, both sexes/all ages, same state geography.2000–2009 uses2010intercensal;2010–2019 usesvintage2020postcensal;2020–2023 usesvintage2023postcensal. Official source bytes/SHA are locked in the registry. This is a transparent combination of locked Census vintages, not a claim of one current revised population vintage. Boundary flags mark2010/2020. The100-row population-vintage overlap audit quantifies both benchmark transitions; original denominators and rates are retained for independent recomputation.

## Verification and limitations
All1,200 inherited counts match independently acquired Census stateZIP counts and preserved Census API responses exactly. A fresh unkeyed2023CBP API call returned a MissingKey HTML page; it was not parsed as data. The officialZIP independent comparison completed despite that API limitation. Three countchanges above25percent are retained: Nevada2008/2012 and Hawaii2023. The densityminimum is Nevada2019 andmaximum NorthDakota2004; no trimming/winsorization.

S6 is DIRECT throughout. No interpolation, forward/back filling, neighboring-year substitution or statistical count modeling. Survey designSE/CI is not applicable; nonsampling undercoverage/classification error and population-estimate revision uncertainty remain. The densityproxy alone does not measure organization quality, access, informal organizations or actual utilization.

## Official references
- https://www.census.gov/programs-surveys/cbp/technical-documentation/methodology.html
- https://www.census.gov/programs-surveys/cbp/about/glossary.html
- https://www.census.gov/naics/resources/archives/sect81.html
- https://www2.census.gov/library/publications/economic-census/2002/other-services/industry-series/ec0281i03.pdf
- https://www.census.gov/naics/2007NAICS/2007_Definition_File.pdf
- https://www.census.gov/naics/2012NAICS/2012_Definition_File.pdf
- https://www.census.gov/naics/2017NAICS/2017_Definition_File.pdf
