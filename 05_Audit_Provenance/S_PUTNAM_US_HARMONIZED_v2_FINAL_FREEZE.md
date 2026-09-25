# Putnam U.S. Social Capital Harmonized v2 — FINAL DATA FREEZE

Date: 2026-09-25
Scope: 50 states × 2000–2023. Measurement construction frozen before E/D outcome analysis.

## Canonical analytical S
- S_PUTNAM_US_HARMONIZED_50states_2000_2023_v2.csv
- 1,200 rows (=50×24), missing final S = 0
- SHA256: 72c231936b1141bf6670f5a71c4d59814b1757971db18f4594a67969559c0def
- OBSERVED_BENCHMARK 528; HARMONIZED_OBSERVED 450; MODEL_ESTIMATED 222.

## P01–P14 component master
- PUTNAM_P01_P14_HARMONIZED_COMPONENT_MASTER_50states_2000_2023_v2.csv
- 16,800 rows (=14×50×24), missing component_value_final_z = 0
- SHA256: 3c6c54a73496aa0d442e7dd6b3f05e3077d0d05a3fd7593cf3dca07bff96b7b3
- HARMONIZED_OBSERVED_Z 3,081
- MODEL_ESTIMATED_COMPONENT_Z 4,119
- CONSTRUCT_EQUIVALENT_LATENT_Z 9,600

Observed/harmonized source values are retained separately. Missing component cells are explicitly bridged/model-estimated from the frozen Putnam-compatible S measurement architecture and are never relabeled observed. No E or D outcome was used to choose the measurement fill.

## Storage verification
The full CSV artifacts are archived in the project Google Drive canonical backup under 03_Master_Panel/S_Social_Capital. GitHub stores this immutable freeze manifest and hashes for verification. Future source upgrades require a new version; v2 must not be overwritten.
