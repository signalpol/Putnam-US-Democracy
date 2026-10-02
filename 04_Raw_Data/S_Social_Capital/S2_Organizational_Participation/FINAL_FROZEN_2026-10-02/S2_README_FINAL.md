# S2 canonical analytical release — 2026-10-02

Run ID: S2_FINAL_20261002T002743Z. Two datasets must remain separate.

`S2_DIRECT_OBSERVED_2009_2023.csv`: 400 original direct proportions and unchanged SE cells. `S2_DIRECT_OBSERVATIONS_FINAL.csv` is its identical compatibility copy. Original observation_status/source_series remain intact. Verified design SE exists for 2011/2013; other source SE is blank.

`S2_FINAL_2000_2023.csv`: 1,200 common-scale latent state-year estimates, all MODEL_ESTIMATED with direct_observation=0. direct_input_available marks the 400 state-years supplying observations. This file is the canonical analytical S2 input. It contains no participation or membership percentages. 2000–2008 are BACKCAST; 2012 is model estimated. No raw values are mixed into this index.

## Model and normalization

Observed logit rate = common intercept + linear trend + state random intercept + common temporal GP + state temporal GP + CEV offset + sampling error. Known design variances are transformed with the delta method. Unknown variances are estimated as a nuisance variance. Exponential GP length is six years; lengths three/twelve and M1 no-break form sensitivity comparisons. M2 removes the CEV design offset in common-target latent prediction. Conditional model latent coordinate is centered at the mean of the 50 posterior 2013 state coordinates and divided by their population SD: center=-0.46481114077366287, SD=0.2117723683180168. The 2013 point index therefore has mean zero, SD one. Changing this anchor changes units, not source proportions. No bounded percentage interpretation is valid.

M2 is chosen to handle the verified wording break and the PI's common-scale target, not the negligible RMSE difference. Covariance/profile Hessian and initialization agreement pass. Constant CEV offset and unit loadings are assumptions; nonoverlapping waves cannot independently establish the cross-question calibration. Early CPS sample/wording differences are not fully calibrated. Unknown 2019/2021 documentation details remain recorded. Statistical completion is conditional on these assumptions.

SE and CI include six model/length sensitivities and approximate profile-Hessian uncertainty. CI is a conservative sensitivity envelope, not a calibrated 95% confidence interval. No historical direct calibration or nine-year backcast truth validation is claimed. See the validation report and full flags.

## Replication

Python 3 with numpy and scipy is required. Run `OPENBLAS_NUM_THREADS=1 python finalize_s2.py > replication_run.log 2>&1` from the extracted package. It reads canonical_base.csv and writes final_package/ plus workbook_data.json. Script input/code/output hashes and timestamps are recorded in S2_RUN_MANIFEST.json. A clean-directory rerun was machine-compared on all latent numeric fields and direct source strings. Excel is a formatted view: `build_workbook.mjs` uses @oai/artifact-tool in the Codex primary runtime; run with the extraction root as its argument. No numerical model calculations depend on Excel.

Frozen means this version's bytes are fixed; it does not mean remaining measurement limitations disappeared. Original direct acquisition packages are preserved in the repository. No Actions workflow was invoked.

## Binary storage and verification

The connected GitHub writer accepts UTF-8 files only. Binary ZIP and XLSX are stored there as lossless `.base64` transports alongside readable CSV/scripts. `decode_binary.py` reconstructs the original binary bytes. Binary SHA256s are in BINARY_MANIFEST.json. Google Drive stores the original ZIP. Verification decodes re-downloaded GitHub transports and compares bytes/size/SHA256 against local and re-downloaded Drive files. SHA256SUMS.txt covers package files except itself. ZIP SHA is external to avoid self-reference.
