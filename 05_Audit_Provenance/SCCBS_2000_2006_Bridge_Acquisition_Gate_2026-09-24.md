# SCCBS 2000-2006 Bridge Acquisition Manifest / Gate
Date: 2026-09-24

## Official sources verified
Roper Center hosts official documentation for both surveys.

### SCCBS 2000
Design: national adult sample N=3,003 plus community samples across 29 states.
Important restriction: state FIPS and other sensitive geography are restricted-use fields.
Documentation is public; documentation+data require registration/access conditions.
Redistribution restrictions apply to Roper data; do not commit licensed microdata to public GitHub unless terms explicitly permit it.

Verified repeated/bridge item families in official codebook:
- CPUBMEET / PUBMEET / PUBMEET2: attendance/frequency at public meeting discussing town or school affairs.
- CVOLTIME / VOLTIMES / VOLTIME2: volunteer frequency/times.
These are useful for P07/P10 measurement bridging, not automatic 50-state canonical observations.

### SCCBS 2006
Design: national adult N=2,741 + community N=9,359 = 12,100.
Official Roper page states documentation+data require free registration for non-members and lists no restricted dataset.
Verified bridge item families:
- CPUBMEET / PUBMEET / merged public-meeting frequency.
- VOLTIME2 and related volunteer-frequency variables.
2006 contains trust and informal-sociability batteries, but each must pass wording/statistic equivalence before mapping to P11/P12/P13/P14.

## Storage rule
Because access/redistribution terms matter:
1. Public codebooks and this provenance manifest may be stored in public GitHub when permitted.
2. Licensed/registration-gated microdata MUST NOT be placed in public GitHub unless redistribution permission is explicit.
3. When lawfully acquired, raw microdata should go to private archival storage / project Drive with source terms and hash.
4. Only derived, non-disclosive statistics may enter public research products if terms permit.
5. S2 bridge outputs remain separate from S1 strict Putnam variables.

## Current acquisition status
- official landing pages: VERIFIED
- official codebooks: VERIFIED
- item families P07/P10: VERIFIED in documentation
- microdata bytes: NOT ACQUIRED in this execution environment
- 50-state coverage: NOT CLAIMED
- canonical P01-P14 replacement: PROHIBITED without equivalence gate

## Next gate after lawful microdata acquisition
- hash raw bytes
- preserve original file names
- identify weights
- reproduce national estimates
- identify genuinely statewide/community geographies
- construct 2000/2006 bridge estimates
- test item comparability/invariance
- never fill unobserved states.
