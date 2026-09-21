# P12 / P13 / P14 Source Disposition — 2026-09-22

## Scope
Canonical panel: 50 U.S. states, 2000–2023, no interpolation.

## P13 Generalized Trust

### Conceptually exact source
The General Social Survey (GSS) contains the canonical generalized-trust construct: whether most people can be trusted versus one cannot be too careful.

### Geography constraint
NORC states that state and county geographic identifiers are sensitive data and are available only under special contract. Public-use geography does not support a legitimate 50-state state-year series.

### 2000 Putnam/Saguaro bridge source
The 2000 Social Capital Community Benchmark Survey (SCCBS), designed by the Saguaro Seminar, includes the generalized-trust question. It contains a national sample of about 3,003 plus roughly 26,700 respondents in 42 communities across 29 states. Because the community sample does not cover all 50 states and is not a 50-state state-representative design, SCCBS must not be converted into a 50-state canonical observation set.

Canonical disposition:
- GSS TRUST = conceptually exact but state geography restricted.
- SCCBS 2000 = strong measurement/validation bridge, not a 50-state panel source.
- P13 canonical state-year cells remain missing unless restricted GSS geography or another demonstrably equivalent 50-state source is obtained.
- No region-to-state allocation, small-area fabrication, interpolation, or silent substitution.

## P12 Entertain at Home

Robert Putnam's research archive identifies the DDB Needham Life Style archive (1975–1999) and the item asking how many times during the past year the respondent entertained at home.

Canonical disposition:
- DDB item = original/historical measurement anchor.
- Its coverage predates the canonical 2000–2023 panel.
- Do not carry the historical state score forward into 2000–2023.
- P12 remains missing pending a modern, state-identifiable, measurement-equivalent source.

## P14 Perceived Honesty

Published documentation of the Putnam state social-capital measures identifies the DDB Needham/Market Facts item measuring agreement that “most people are honest.” The underlying surveys were accumulated over approximately 1975–1997/1999; published state measures cover the continental states rather than a 2000–2023 annual 50-state panel.

Canonical disposition:
- DDB honesty = original/historical measurement anchor.
- Do not substitute generalized trust (“most people can be trusted”) for perceived honesty; they are related but distinct indicators in the Putnam architecture.
- Do not extend historical DDB state values forward.
- P14 remains missing pending a modern, state-identifiable, measurement-equivalent source.

## Overall decision
P12, P13, and P14 are not to be filled merely to complete the 14-variable matrix. Structural missingness is preferable to fabricated measurement. Historical/original sources remain in the provenance layer and may be used for construct validation or sensitivity analysis, not as invented annual observations.
