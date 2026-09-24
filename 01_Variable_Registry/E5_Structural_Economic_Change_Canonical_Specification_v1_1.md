# E5 Structural Economic Change — Canonical Specification v1.1
Date: 2026-09-24

## Construct
E5 measures state-level structural economic change. It is not a generic prosperity measure.

## Primary measure
Manufacturing value-added share of state GDP, annual:
E5_MFG_VA_SHARE_st = Manufacturing current-dollar value added_st / All-industry current-dollar GDP_st.

Primary official source: U.S. Bureau of Economic Analysis Regional GDP by state and industry.
Target: 50 states, 2000-2023.
BEA's state GDP-by-industry framework covers 1997-2023, so the full study period is inside the documented framework.

## Change measures
Retain separately:
1. E5_MFG_VA_SHARE — level.
2. E5_MFG_VA_SHARE_D1 — one-year percentage-point change.
3. E5_MFG_VA_SHARE_D5 — five-year percentage-point change where both endpoints are observed.
4. E5_MFG_VA_SHARE_CUM2000 — change from each state's 2000 baseline.

Do not collapse these into one index before estimation.

## Secondary measure
Manufacturing employment share is conceptually useful but is SECONDARY until a continuous, definition-consistent 2000-2023 state series is verified.
BEA SAEMP25 state/local industry employment tables were discontinued in 2024. Archived BEA data may be used only after coverage and NAICS continuity audit; alternatively a BLS state-industry employment series may be used after the same audit.
Never splice sources silently.

## Industry definition
Manufacturing must use the BEA manufacturing aggregate/industry label as published for each vintage. Preserve LineCode/industry code, description, unit, table, and vintage metadata.
Audit classification continuity before treating the series as invariant across 2000-2023.

## Interpretation
Level and change answer different questions:
- level: dependence/exposure to manufacturing;
- D1/D5/cumulative change: structural transformation or deindustrialization intensity.
Both enter empirical work separately.

## Validation gates
- 50 states only; DC/territories excluded.
- 2000-2023 target.
- 1,200 unique state-year keys for the primary level measure if source coverage is complete.
- denominator must be all-industry current-dollar state GDP from the same BEA vintage/table family.
- no interpolation.
- no mixing current-dollar numerator with real/chained-dollar denominator.
- raw files immutable; hashes and provenance recorded.
