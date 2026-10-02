from pathlib import Path
import csv,json,hashlib,zipfile,base64,shutil
R=Path(__file__).resolve().parent;O=R/'final_package'
def rows(n):return list(csv.DictReader((O/n).open()))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,rr):
 with (O/n).open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rr[0]));w.writeheader();w.writerows(rr)
run=json.loads((O/'S2_RUN_MANIFEST.json').read_text());q=rows('S2_QA_FINAL.csv');comp=rows('S2_MODEL_COMPARISON.csv');hold=rows('S2_HOLDOUT_SUMMARY.csv');param=json.loads((O/'S2_MODEL_PARAMETERS.json').read_text())
primary=[x for x in comp if x['specification']=='M2_L6'][0]
validation=['# S2 model validation','',f"Run {run['run_id']}. Model engine exit code {run['exit_code']}; {len(q)}/{len(q)} structural/method-status QA checks PASS.", '', '| Model | Holdout RMSE (proportion) | MAE | Mean bias | Coverage |','|---|---|---|---|---|']
for x in hold:validation.append(f"|{x['model']}|{x['RMSE']}|{x['MAE']}|{x['mean_bias']}|{x['coverage']}|")
validation+=['','All five wave holdouts (2009, 2011, 2013, 2019, 2021) and both optimizer starts were actually executed. Coverage concerns prediction of withheld observed rates. Holdout intervals add the known delta-method sampling variance for 2011/2013, and the estimated nuisance sampling variance for other waves. Earlier review coverage used a shared nuisance variance for all holdouts; this final run corrects that distinction. These are not validation of backcast truth.','',f"Selected covariance profile Hessian minimum eigenvalue: {primary['hessian_min_eigenvalue']}; condition number: {primary['hessian_condition']}; two-start NLL difference: {primary['start_nll_difference']}. The coefficient covariance is the inverse GLS information matrix. Positive Hessian is local conditional identification, not empirical identification of the bridge without temporal assumptions.",'','M2_L6 is selected because the independent official wording audit establishes a participation/membership break and the PI explicitly chose a common latent analytical series. Its small RMSE advantage is not the selection rationale. M0, M1 and M2 are bounded alternatives; AIC weakly favors M2, BIC favors M1. M1/M2 lengths 3, 6 and 12 all enter sensitivity uncertainty; no unrestricted specification search was used.','',f"Primary CEV intercept shift {primary['CEV_offset']} with conditional GLS SE {primary['CEV_offset_conditional_SE']}. The near-zero lower-information bridge is conditional on fixed unit loadings and a common exponential time covariance. No concurrent cross-question anchor exists. Posterior scale correction sets the CEV observation-design offset to zero in latent predictions, rather than leaving the observed-scale offset in annual output.",'','Profile-Hessian covariance propagation uses 32 bounded multivariate-normal parameter draws, seed 20261002. For each, GLS coefficients are reestimated. The model SE adds conditional latent variance, variance of drawn posterior means, and mean squared deviation across six sensitivity predictions around the primary mean. This is a conservative model-uncertainty measure, not a survey design SE or a Bayesian model probability mixture. CI fields envelope both the resulting mean ±1.96 SE and the six conditional intervals; nominal 95% frequentist coverage is not asserted. The 2013 anchor is held fixed, so anchor uncertainty is not fully integrated.','', 'Holdout coefficient/offset stability is retained for every state and wave in S2_HOLDOUT_VALIDATION.csv. State residual patterns are in S2_STATE_HOLDOUT_RESIDUALS.csv. Backcast and gap values have explicit flags; all rows retain bridge assumptions and incomplete early design calibration.']
(O/'S2_MODEL_VALIDATION_REPORT.md').write_text('\n'.join(validation)+'\n')
hh=rows('S2_HOLDOUT_VALIDATION.csv');rr=[]
for st in sorted(set(x['state'] for x in hh)):
 a=[float(x['residual']) for x in hh if x['state']==st and x['model']=='M2'];rr.append(dict(state=st,n=len(a),mean_bias=sum(a)/len(a),MAE=sum(abs(x) for x in a)/len(a),RMSE=(sum(x*x for x in a)/len(a))**.5))
write('S2_STATE_HOLDOUT_RESIDUALS.csv',rr)
audit=(O/'S2_MEASUREMENT_EQUIVALENCE_AUDIT.md').read_text().replace('# S2 measurement review — decision required','# S2 measurement equivalence audit — final analytical release').replace('This is a provisional audit, not a claim that all wave documentation is verified.','Evidence status remains explicit for every wave. Common-scale estimation is authorized by the PI; this does not establish strict empirical measurement invariance.')
audit+='\n## Authorized analytical decision\n\nThe primary dataset is a separate latent analytical index. The 400 observed proportions remain unchanged. The fixed unit-loading/common CEV-offset measurement model is a declared harmonization assumption. Unknown or conflicting wave designs remain uncertainty flags. The 2008 status is NO DIRECT OBSERVATION AVAILABLE IN CURRENT EVIDENCE, not an assertion that microdata do not exist.\n'
(O/'S2_MEASUREMENT_EQUIVALENCE_AUDIT.md').write_text(audit)
(O/'S2_README_FINAL.md').write_text(f'''# S2 canonical analytical release — 2026-10-02

Run ID: {run['run_id']}. Two datasets must remain separate.

`S2_DIRECT_OBSERVED_2009_2023.csv`: 400 original direct proportions and unchanged SE cells. `S2_DIRECT_OBSERVATIONS_FINAL.csv` is its identical compatibility copy. Original observation_status/source_series remain intact. Verified design SE exists for 2011/2013; other source SE is blank.

`S2_FINAL_2000_2023.csv`: 1,200 common-scale latent state-year estimates, all MODEL_ESTIMATED with direct_observation=0. direct_input_available marks the 400 state-years supplying observations. This file is the canonical analytical S2 input. It contains no participation or membership percentages. 2000–2008 are BACKCAST; 2012 is model estimated. No raw values are mixed into this index.

## Model and normalization

Observed logit rate = common intercept + linear trend + state random intercept + common temporal GP + state temporal GP + CEV offset + sampling error. Known design variances are transformed with the delta method. Unknown variances are estimated as a nuisance variance. Exponential GP length is six years; lengths three/twelve and M1 no-break form sensitivity comparisons. M2 removes the CEV design offset in common-target latent prediction. Conditional model latent coordinate is centered at the mean of the 50 posterior 2013 state coordinates and divided by their population SD: center={param['anchor']['center']}, SD={param['anchor']['scale']}. The 2013 point index therefore has mean zero, SD one. Changing this anchor changes units, not source proportions. No bounded percentage interpretation is valid.

M2 is chosen to handle the verified wording break and the PI's common-scale target, not the negligible RMSE difference. Covariance/profile Hessian and initialization agreement pass. Constant CEV offset and unit loadings are assumptions; nonoverlapping waves cannot independently establish the cross-question calibration. Early CPS sample/wording differences are not fully calibrated. Unknown 2019/2021 documentation details remain recorded. Statistical completion is conditional on these assumptions.

SE and CI include six model/length sensitivities and approximate profile-Hessian uncertainty. CI is a conservative sensitivity envelope, not a calibrated 95% confidence interval. No historical direct calibration or nine-year backcast truth validation is claimed. See the validation report and full flags.

## Replication

Python 3 with numpy and scipy is required. Run `OPENBLAS_NUM_THREADS=1 python finalize_s2.py > replication_run.log 2>&1` from the extracted package. It reads canonical_base.csv and writes final_package/ plus workbook_data.json. Script input/code/output hashes and timestamps are recorded in S2_RUN_MANIFEST.json. A clean-directory rerun was machine-compared on all latent numeric fields and direct source strings. Excel is a formatted view: `build_workbook.mjs` uses @oai/artifact-tool in the Codex primary runtime; run with the extraction root as its argument. No numerical model calculations depend on Excel.

Frozen means this version's bytes are fixed; it does not mean remaining measurement limitations disappeared. Original direct acquisition packages are preserved in the repository. No Actions workflow was invoked.

## Binary storage and verification

The connected GitHub writer accepts UTF-8 files only. Binary ZIP and XLSX are stored there as lossless `.base64` transports alongside readable CSV/scripts. `decode_binary.py` reconstructs the original binary bytes. Binary SHA256s are in BINARY_MANIFEST.json. Google Drive stores the original ZIP. Verification decodes re-downloaded GitHub transports and compares bytes/size/SHA256 against local and re-downloaded Drive files. SHA256SUMS.txt covers package files except itself. ZIP SHA is external to avoid self-reference.
''')
(O/'decode_binary.py').write_text("from pathlib import Path\nimport base64\nfor p in Path('.').glob('*.base64'):\n out=p.with_suffix('');out.write_bytes(base64.b64decode(p.read_bytes(),validate=True));print(out)\n")
original=rows('S2_FINAL_2000_2023.csv');replayed=list(csv.DictReader((R/'replay_input/final_package/S2_FINAL_2000_2023.csv').open()));cols=['state','year','S2_estimate','S2_SE','CI_lower','CI_upper','observation_type','backcast_flag','uncertainty_flag']
mismatch=sum(any(a[k]!=b[k] for k in cols) for a,b in zip(original,replayed));assert len(replayed)==1200 and mismatch==0
observed=rows('S2_DIRECT_OBSERVED_2009_2023.csv');rr=list(csv.DictReader((R/'replay_input/final_package/S2_DIRECT_OBSERVED_2009_2023.csv').open()));assert observed==rr
replay=json.loads((R/'replay_input/final_package/S2_RUN_MANIFEST.json').read_text())
(O/'S2_REPLICATION_CHECK.json').write_text(json.dumps(dict(latent_rows=1200,numeric_flag_mismatches=mismatch,direct_exact_rows=400,replication_run_id=replay['run_id'],started_utc=replay['started_utc'],ended_utc=replay['ended_utc'],exit_code=replay['exit_code'],compared_columns=cols,provenance_run_ids_differ_by_design=True),indent=2))
shutil.copy2(R/'decision_review/S2_INHERITED_DIRECT_VALUE_COMPARISON.csv',O/'S2_INHERITED_DIRECT_VALUE_COMPARISON.csv')
shutil.copy2(R/'inputs/acquisition_followup.json',O/'S2_2008_ACQUISITION_EVIDENCE.json')
shutil.copy2(Path(__file__),O/'assemble_package.py')
# Do not package temporary authoring inspect sidecar.
for p in O.glob('*.inspect.ndjson'):p.unlink()
(O/'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.name}\n' for p in sorted(O.iterdir()) if p.is_file() and p.name!='SHA256SUMS.txt'))
z=R/'S2_FINAL_FROZEN_2026-10-02.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as h:
 for p in sorted(O.iterdir()):h.write(p,p.name)
G=R/'github_upload';G.mkdir(exist_ok=True)
for p in O.iterdir():
 if p.suffix!='.xlsx':shutil.copy2(p,G/p.name)
bins=[]
for p in [z,O/'S2_FINAL_2000_2023.xlsx']:
 (G/(p.name+'.base64')).write_bytes(base64.b64encode(p.read_bytes()));bins.append(dict(file=p.name,bytes=p.stat().st_size,sha256=sha(p),transport=p.name+'.base64'))
(G/'BINARY_MANIFEST.json').write_text(json.dumps(bins,indent=2))
print(json.dumps(dict(run_id=run['run_id'],package_files=len(list(O.iterdir())),github_files=len(list(G.iterdir())),binary_manifest=bins,replication_mismatches=mismatch),indent=2))
