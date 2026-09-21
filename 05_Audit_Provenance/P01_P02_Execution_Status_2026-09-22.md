# P01/P02 Combined Proxy — Execution Status (2026-09-22)

## Verified source architecture
Target waves: 2008, 2009, 2010, 2011, 2013 CPS Civic Engagement supplements.

Raw variables:
- 2008 PEQ6
- 2009 PEQ6
- 2010 PEQ6
- 2011 PES7
- 2013 PES7

All measure officer OR committee service as one combined Yes/No construct. They must not be duplicated into separate P01 and P02 observations.

## Official file availability
Census technical-documentation pages verify the Civic Engagement supplements for all five target years.
Census dataset pages explicitly expose separate CPS Supplement data files for 2011 and 2013 (approximately 15 MB and 14 MB respectively), distinct from the Basic Monthly November CPS files.

## Execution guard
The estimator now fails closed unless the supplied frame contains:
1. the wave-specific Civic variable (PEQ6 or PES7),
2. the state identifier,
3. PWNRWGT,
4. substantive 1/2 Yes/No responses.

This prevents accidental use of a Basic Monthly CPS file that lacks the Civic supplement variables.

## Current execution status
NOT EXECUTED for the 250 target state-wave observations in this environment.
No state estimates are claimed until official supplement bytes are actually read and the 50-state assertions pass.

Canonical rule: no interpolation, no duplication into P01/P02, no fabricated observations.
