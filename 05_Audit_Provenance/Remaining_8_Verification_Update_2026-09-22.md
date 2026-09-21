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


## P01/P02 Committee Service / Officer Service — CPS combined proxy
Status: **MEASUREMENT VERIFIED — MUST NOT BE DUPLICATED INTO P01 AND P02**

Official Census CPS Civic Engagement waves: 2008, 2009, 2010, 2011, 2013.
The 2013 Census API variable registry identifies `PES7` as “Officer or committee member.” The construct is therefore a combined leadership/service item rather than two independently observed measures.

Canonical handling:
- preserve one auxiliary series: `P01_P02_officer_committee_combined_proxy`;
- flag `PROXY_COMBINED`;
- do not copy the same estimate into both canonical P01 and P02;
- P01 and P02 remain separately missing unless a source that distinguishes committee service from officer service is obtained;
- non-wave years remain missing; no interpolation.

## P11 Visiting Friends
Status: **MODERN CPS PROXY VERIFIED; WORDING BRIDGE REQUIRED ACROSS WAVES**

The 2013 official Census variable registry identifies `PES13` as “See or hear from family/friends, how often.” This is substantively close to Putnam's visiting-friends construct but is broader (contact can include seeing or hearing) and therefore must be labeled PROXY rather than measurement-equivalent.

Later Volunteering and Civic Life waves (2017, 2019, 2021, 2023) require separate variable/wording harmonization before pooling. The 2023 instrument remains state-identifiable and supplies a supplement weight, but its item set/labels differ from 2013.

Canonical handling:
- retain wave-specific source variable and exact wording;
- derive state weighted estimates only for actual survey waves;
- do not interpolate non-wave years;
- do not silently pool wording changes.

## P04 Club Meetings
Status: **CPS PROXY CONSTRUCT CONFIRMED; EXACT VARIABLE/WAVE CROSSWALK STILL OPEN**

Contemporary documentation and CPS-based research confirm that the Civic Engagement instrument measured attendance at a meeting of a group or organization. This is a strong Putnam-compatible proxy for club-meeting participation, but exact wave-specific Census variable IDs and response coding must be crosswalked before state estimates are committed.

Canonical handling:
- classify as PROXY;
- preserve exact question wording and reference period by wave;
- no interpolation;
- do not confuse “public meeting to discuss issues” with “group/organization meeting.”
