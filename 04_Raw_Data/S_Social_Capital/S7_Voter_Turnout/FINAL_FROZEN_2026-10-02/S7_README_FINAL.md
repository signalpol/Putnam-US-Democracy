# S7 Voter Turnout / Electoral Participation - package 2026-10-02 (Putnam U.S. Democracy Project)
S7_FINAL_2000_2023.csv/.xlsx: 1,200 rows (50 states x 2000-2023). DIRECT 600 (general elections 2000-2022), MODEL_ESTIMATED 600 (odd years, latent participation propensity; 2023 = forecast).
Raw observed turnout preserved in observed_turnout_vep and S7_DIRECT_OBSERVATIONS_FINAL.csv. Source: UF Election Lab v1.2 (VEP). Model M2 (see S7_MODEL_VALIDATION_REPORT.md).
Limitations: edge holdout failure (2000 coverage 0.50); election-specific national shocks; 40 cells with highest-office numerator; Drive CANONICAL_RAW v1/v2 not audited. Existing v1/v2 were not modified.
Integrity: sha256sum -c SHA256SUMS.txt
