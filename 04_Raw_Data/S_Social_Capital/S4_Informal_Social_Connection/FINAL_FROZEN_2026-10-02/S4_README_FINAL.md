# S4 Informal Social Connection — package 2026-10-02 (Putnam U.S. Democracy Project)
Main file: data/S4_FINAL_2000_2023.csv (and .xlsx) — 50 states × 2000–2023 = 1,200 rows.
DIRECT 300 (2011, 2013, 2017, 2019, 2021, 2023) · MODEL_ESTIMATED 900 (backcast 2000–2010 = 550, bridge 2014–2016 = 150, other gaps 2012/2018/2020/2022 = 200).
Inclusion of the 2000–2010 backcast follows the Director's 2026-10-02 instruction; it overrides the earlier "experimental only" status. The separate experimental file and the 2011–2023 candidate are kept unchanged in data/.
Sources: CPS Civic Engagement Supplement (Nov 2011, 2013) and CPS CEV (Sep 2017–2023), Census public-use microdata + 160 replicate weights; AmeriCorps 4r6x-re58 used only as reproduction benchmark (600/600 within 0.0005). See S4_SOURCE_REGISTRY.csv, docs/, qa/, logs/, code/.
Limitations: no overlap year between regimes; 2011 edge holdout under-coverage (0.83); backcast has no observational information; Friends/Family excluded from primary. Prior working package S4_GATE1_WORKING_PACKAGE_v1 is superseded for data use but retained.
Integrity: sha256sum -c SHA256SUMS.txt
