# DDB STATE Geography — Direct Codebook Verification v1.0
Date: 2026-09-24

## Direct codebook evidence
The released DDB Life Style codebook documents:
- YEAR = year of survey
- WEIGHT = weight for sample adjustment
- STATE = variable 380, "State of interview"
- state codes covering the U.S. states.

This upgrades the geography finding from inference from published analyses to direct codebook verification.

## Independent empirical confirmation
Published research using individual DDB Life Style observations merges respondents with state-level policy/expenditure variables and estimates models indexed by individual i, state s, and year t. One such analysis uses DDB observations through 2004.

## Implication for P11 / P12 / P14
If lawful post-1998 DDB microdata are obtained, the required extraction architecture is already known:
YEAR + STATE + WEIGHT + exact Putnam item + any necessary design/demographic fields.

State-level estimation is technically feasible. The unresolved issue is access to post-1998 microdata, not the existence of state geography.

## Strict validation after acquisition
1. Verify STATE coding is present in each post-1998 file.
2. Verify exact wording/coding of visfrd, enthome, honesty.
3. Verify WEIGHT definition and any redesign.
4. Report unweighted and weighted n by state-year.
5. Do not publish state-year estimates below a pre-specified reliability threshold.
6. Consider multi-year pooling when annual state cells are too small; preserve raw irregular-wave structure and do not interpolate.
