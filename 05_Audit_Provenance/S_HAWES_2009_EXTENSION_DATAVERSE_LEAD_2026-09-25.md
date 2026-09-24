# Hawes social-capital extension lead — 2017/2018 replication

Source: Hawes, Daniel P. & Austin Michael McCrea, Political Research Quarterly 71(2):347-360, DOI 10.1177/1065912917738576.

Critical empirical finding:
- article analyzes state-level longitudinal data through 2009
- final analysis covers 48 contiguous states
- social capital is factor analysis of 22 items, cited to Hawes, Rocha & Meier
- replication data: Harvard Dataverse DOI 10.7910/DVN/L1V6BP
- a public CauSciBench replication script identifies the social-capital field as SC8609_ma

Implication:
This is stronger evidence than the original 1986-2004 article that a Hawes-series measure was used through 2009. Next acquisition target is the Harvard Dataverse replication dataset itself.

Caution:
SC8609_ma is a moving-average construction. Preserve separately from unsmoothed/raw observed social-capital measurements; do not describe each annual value as an independent survey observation.

Storage target after acquisition:
04_Raw_Data/S_Social_Capital/HAWES_DYNAMIC/
- original replication artifact
- extracted state-year SC8609_ma
- provenance/codebook
- canonical 50-state x 2000-2023 grid, observed values only and NA elsewhere

No interpolation. Alaska/Hawaii treatment follows source and must be explicit.
