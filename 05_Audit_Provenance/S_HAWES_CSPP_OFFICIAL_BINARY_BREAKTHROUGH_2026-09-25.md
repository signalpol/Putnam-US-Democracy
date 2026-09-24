# Hawes numeric source breakthrough — CSPP official package

Verified 2026-09-25.

Official IPPSR/csppData repository contains binary file:
- data/correlates.rda
- Git blob SHA: 1819d63b706a84b40c7b49b42ea64d0edbecac81
- size from Git tree: 7,421,592 bytes

Official CSPP codebooks identify:
- soc_capital: Hawes et al. social capital measure, 1986–2009
- soc_capital_ma: Hawes et al. weighted moving-average social capital, 1984–2011

CRAN csppData package version 0.2.61 also distributes the correlates dataset and codebook. This gives a second official public distribution route independent of the legacy SPPQ Dataverse.

Important methodological rule:
CSPP soc_capital_ma is a weighted moving-average derivative. It must not be mislabeled as annual raw MRI observations. Preserve both soc_capital and soc_capital_ma separately.

Acquisition status:
The binary object is located and its Git object identity verified. Current GitHub connector exposes binary metadata but returns no decoded body for .rda. Extraction of numeric state-year values remains the next step; do not fabricate them.
