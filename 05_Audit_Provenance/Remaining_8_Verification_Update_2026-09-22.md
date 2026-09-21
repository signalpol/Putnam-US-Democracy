# Remaining-variable verification update — 2026-09-22

## P03 Civic & Social Organization Density
Status: **COLLECTOR BUILT / DATA EXTRACTION NOT YET EXECUTED**

Canonical modern replication definition:
`CBP NAICS 813410 establishments / Census resident population * 1,000`.

Classification: **PROXY — Putnam-compatible administrative replication**, not original Putnam data.

Official sources verified:
- Census County Business Patterns annual state datasets, 2000–2023.
- Example state ZIPs: `cbp00st.zip`, `cbp23st.zip`.
- Census Population Estimates: 2000–2010 intercensal state file; 2010–2020 state totals; 2020–2023 state totals.
- 50 states only; DC and territories excluded.
- No interpolation.

Reproducible collector:
`06_Analysis/collect_P03_CBP_813410.py`

Execution note: current local runtime could not reach Census FTP; Railway fallback could not provision another free-plan resource. Therefore no 1,200-row output is claimed yet.

## P13 Generalized Trust
Status: **QUESTION VERIFIED / PUBLIC 50-STATE PANEL NOT AVAILABLE**

The GSS contains the canonical generalized-trust question (`TRUST`; later `TRUSTV/TRUSTNV` variants). However, NORC states that geocoded identifiers including **state and county are sensitive data supplied only under special contract**. Therefore the public-use GSS cannot legitimately be used to construct the required 50-state × year P13 panel.

Decision:
- Do **not** manufacture state estimates from public GSS.
- Do **not** substitute region for state.
- Retain GSS TRUST as a conceptually exact national/validation source unless restricted geocoded access is obtained.

## P12 Entertain at Home / P14 Perceived Honesty
Status: **ORIGINAL HISTORICAL SOURCE LOCATED; MODERN 2000–2023 EQUIVALENT NOT ESTABLISHED**

Robert Putnam's Bowling Alone research archive states that the DDB Life Style archive and state-level social-capital measures are downloadable for scholarly/academic research. DDB coverage is 1975–1998 (the selected-question archive is described as 1975–1999 on the page).

Verified original constructs include:
- P12: number of times entertained at home in the last year.
- P14: agreement/perception that most people are honest (documented in Putnam-derived state social-capital work).

Decision:
- Preserve DDB as **historical/original measurement validation**, not as 2000–2023 canonical observations.
- Do not replace P14 with generalized trust; honesty and trust are related but distinct constructs.
- Continue search for a modern state-year equivalent; otherwise retain canonical missingness.
