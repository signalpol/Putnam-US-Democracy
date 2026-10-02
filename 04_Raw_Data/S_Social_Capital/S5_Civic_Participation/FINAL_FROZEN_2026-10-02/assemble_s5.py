import pathlib,csv,json,shutil,hashlib,datetime,numpy as np
R=pathlib.Path(__file__).parent;P=R/'final_package';I=R/'inputs'
def rows(n):return list(csv.DictReader((P/n).open()))
def write(n,r):
 with (P/n).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=r[0]);w.writeheader();w.writerows(r)
panel=rows('S5_FINAL_2000_2023.csv');obs=rows('S5_DIRECT_OBSERVATIONS_FINAL.csv');ho=rows('S5_HOLDOUT_VALIDATION.csv');mc=rows('S5_MODEL_COMPARISON.csv');ov=rows('S5_S7_OVERLAP_SENSITIVITY.csv');lr=rows('S5_PARTIAL_ITEM_CALIBRATION.csv');manifest=json.loads((P/'S5_RUN_MANIFEST.json').read_text());rs=rows('S5_HOLDOUT_STATE_RESIDUALS.csv');full=[r for r in rs if r['basket']=='ACTIVE6' and r['model']=='M2' and int(r['year'])>=2017];e=np.array([float(r['residual']) for r in full]);cover=np.mean([int(r['covered']) for r in full]);summary=dict(cells=len(e),MAE=float(abs(e).mean()),RMSE=float(np.sqrt(np.mean(e**2))),mean_bias=float(e.mean()),coverage=float(cover));(P/'S5_HOLDOUT_SUMMARY.json').write_text(json.dumps(summary,indent=2))
(P/'S5_METHOD_DECISION_APPROVED.md').write_text('''# Approved methodological decision

Research Director instruction received2026-10-02,13:43KST, before this final fit.

Primary construct: Active Civic Participation. Active6 comprises local voting, contacting public officials, political donation, public meeting attendance, collective neighborhood action and political consumption. Broad10 is a sensitivity specification. Active5 excludes local voting to examine overlap with S7.

The Director specifies construct validity as the reason, rather than the size of an observed decline. This approval preceded final model fitting, but followed the earlier exploratory basket comparison. It is not represented as a blinded preregistration predating all exploratory results.
''')
(P/'S5_MODEL_VALIDATION_REPORT.md').write_text(f'''# S5 model and validation report

RUN_ID: {manifest['run_id']}. CodeSHA: {manifest['code_sha256']}. ExecutionUTC: {manifest['start_utc']} to{manifest['end_utc']};exit0. Numeric outputs and optimizer/Hessian results are preserved, not inferred from a model name.48fits:13full/sensitivity fits and35whole-wave holdouts, each with two optimization starts.

## Definition and scale
Active6 is the approved primary construct. The6 rates are standardized using each item's2017mean and SD across50states, averaged equally, then divided by the2017SD of that mean. This fixed anchor makes the full-basket input scores mean0/SD1 in2017. The primary latent posterior signal is expressed in those input-score units; its2017posterior mean and SD are not forced to0/1. No within-year standardization is performed. Local voting has a different eligible population from other actions; the target is a state-level domain index, not a respondent-level union probability or participation percentage.

## Partial-item measurement link
Only contacted-official and political-consumption historical rates are available for2010/2011/2013. Within the four CEV waves, regress the fixed Active6 index on an intercept and standardized contact/consumption rates. The empirical calibration explains{float(lr[0]['R_squared']):.3f} of the input-score variance, with residualSD{float(lr[0]['link_residual_SD']):.3f}. Applying these coefficients to CPS is an assumption of transport across age/universe/wording/mode differences, not proven scalar invariance. Historical projections are model-linked measurements, never DIRECT Active6 scores.350model-input cells=200complete CEV index cells+150partial historical projections. Original2,300item rates remain DIRECT in a separate observed file.

Historical designSEs, where verified, enter through a conservative upper bound for the covariance of the two weighted item estimates. Unknown2010designSE remains unknown; the modeled link residual and estimated noise do not relabel it as verified survey error. The coefficient covariance and link residual are carried intoM2. The primary link is estimated from overlapping CEV items; no overlap sample directly identifies a CPS-versus-CEV regime shift.

## Models
M0: Gaussian state random intercept and measurement noise. M1: M0 plus state-specific and common exponential temporal Gaussian processes. M2: M1 plus coefficient-calibration covariance and a shared CPS measurement shift withN(0,0.5²) prior, marginalized analytically. This proper prior identifies the otherwise weakly separated regime/time components conditionally. The0.5SD choice is a transparent working assumption;1SD, no-regime(M1), exclusion of historical measurements and temporal lengths3/12years are sensitivity cases. Primary temporal length6years was the bounded working specification inherited before the final fit. No unbounded model search.

Gaussian covariance is a² I_same_state +q² I_same_state exp(-|t-t'|/L)+c² exp(-|t-t'|/L); measurement noisee² and known/link covariance enter the observation covariance. A common intercept is profiled by GLS. Canonical prediction uses the target latent covariance, excluding observation noise, CPS shift and calibration error from the target itself. Their estimation uncertainty affects conditioning. The primary latentSE includes conditional posterior covariance and GLS mean uncertainty. Kernel hyperparameters and item scaling are plugged in, not fully Bayesian integrated.

M2 is selected because it explicitly handles the known measurement problem under the approved construct. Within Active6,AIC M0/M1/M2={float(mc[0]['AIC']):.3f}/{float(mc[1]['AIC']):.3f}/{float(mc[2]['AIC']):.3f};BIC={float(mc[0]['BIC']):.3f}/{float(mc[1]['BIC']):.3f}/{float(mc[2]['BIC']):.3f}. These are conditional criteria within the same basket/input set. Cross-basket criteria and CEV-only versus350-input criteria cannot select the construct. Small predictive differences do not independently identify the regime. Primary two-start likelihood agreement, positive finite-difference Hessian and analytic-gradient crosscheck pass. The CEV-only sensitivity has a state-time covariance at its lower bound, explicitly reported in raw output; it is not proof of an identified temporal process.

## Holdout
Every item in the heldout wave is removed from training. Item scaling and the two-item calibration are refitted using training CEV waves only. Holdout2017 uses2019as the earliest training anchor; no2017mean/SD leakage. Historical2010/2011/2013 folds validate partial-item projections, not unobserved full-basket truth. CEV2017/2019/2021/2023 folds validate complete fixed-basket scores.

Across200heldout CEV cells, primaryM2 pooledMAE={summary['MAE']:.6f},RMSE={summary['RMSE']:.6f},mean bias={summary['mean_bias']:.6f} training-anchorSD; prediction-interval coverage={summary['coverage']:.3%}. Predictive intervals include modeled residual noise and differ from latent-signalCI.35holdout fits converged; all state residuals, wave results and optimizer outputs are supplied. These retrospective missing-wave tests are not prospective forecasts, election-result tests or proofs of historical backcast accuracy.

## Uncertainty and backcast
CanonicalCI is the envelope of primary1.96×sensitivity-inclusive uncertainty and seven Active6 model/length/regime/history variants' conditional1.96SD intervals. This nominal95percent model/sensitivity envelope is not calibrated frequentist95percent coverage for latent truth. Broad10/Active5 are different construct definitions and are excluded from this primary uncertainty envelope; their full1,200-row panels are separate.

2000–2009 has no direct input item observation in current evidence.2010–2016 has only incomplete/bridged historical basket evidence. All pre2017rows are backcast relative to a complete Active6 basket. There is no50-state full-basket historical ground truth validating these early latent levels.{sum('BACKCAST_MODEL_SENSITIVITY' in r['validation_risk_flag'] for r in panel)}pre2017cells exceeded0.25SD across the bounded Active6 sensitivity cases and carry BACKCAST_MODEL_SENSITIVITY. The threshold is a diagnostic flag, not a significance test. No linear interpolation, forward/back fill or adjacent-year substitution.

## S7 overlap
S7 is read only from its verified final package, not modified. Its actual file defines general-election administrative VEP turnout (with declared source substitutions), whereas S5 uses self-reported participation in the last local election among eligible respondents. Electoral domain overlap exists; variables are not identical. Across1,200modeled state-years, S7correlation is{float(ov[0]['all_state_year_correlation_with_S7']):.6f} forActive6 and{float(ov[1]['all_state_year_correlation_with_S7']):.6f} forActive5. Within-state demeaned correlations are{float(ov[0]['within_state_demeaned_correlation_with_S7']):.6f} and{float(ov[1]['within_state_demeaned_correlation_with_S7']):.6f}. Correlation of modeled panels is not independent validation and cannot decide duplicate weighting in a later social-capital composite. Active5 sensitivity preserves the requested check without changing the approved Active6 primary.

## Replication reference
Rasmussen and Williams(2006),Gaussian Processes for Machine Learning,Chapter2, supplies Gaussian conditioning and marginal likelihood. https://gaussianprocess.org/gpml/chapters/RW2.pdf . Estimation assumptions and limitations above are project choices, not claims attributed to Census.
''')
(P/'S5_MEASUREMENT_EQUIVALENCE_AUDIT.md').write_text('''# S5 measurement equivalence audit

## Approved construct
Six active civic behaviors, individually preserved as original proportions. A state-level latent analytical scale is separate from these rates. No claim that the six behavior prevalences share identical individual universes, or that an any-one respondent rate was computed.

|Wave|Evidence|Basket equivalence|Universe/weight/reference|
|---|---|---|---|
|2010|Official raw two items; codebook and extraction manifest|PARTIAL|18+adult civilians, supplement interviews;PWNRWGT;past12months|
|2011|Official raw and NR160replicates|PARTIAL|18+;PWNRWGT;document/rawMISconflict retained|
|2013|Official raw and NR160replicates|PARTIAL|18+;PWNRWGT;document/rawMISconflict retained|
|2017|Archived10state rates match sourceworkbook; official questionnaire|DIRECT ITEM OBSERVATIONS;full6basket inputs|16+CEV;local voting18+eligible;PWNRWGT;past12months|
|2019|Newly acquired official cpssept19.pdf/text; archived rates unchanged|DIRECT ITEM OBSERVATIONS;full6basket inputs|FullCPS households, randomly selected civilian16+;same6variables/wording/coding;PWNRWGT|
|2021|Newly acquired official cpssept21.pdf/text; archived rates unchanged|DIRECT ITEM OBSERVATIONS;full6basket inputs|Same6questions andPWNRWGT;PWSRWGT reserved forPESWP1a-d, outsideActive6|
|2023|Official questionnaire/codebook; archived rates unchanged|DIRECT ITEM OBSERVATIONS;full6basket inputs|16+CEV,local votingeligible;PWNRWGT;past12months|

Census2019/2021documents resolve the earlier review's UNKNOWN documentation availability. This is a documentation update, not replacement of any archived rate. In all four CEV codebooks, Active6variables arePES11(local elections),PES13(contact),PES17(political donation over$25),PES12(publicmeeting),PES7(neighborhoodaction),PES14(politicalconsumption).Yes1/No2;localvote3ineligible excluded from the intended rate. NegativeNIU/DK/refusal/noanswer are not automaticallyNo. CEV asks for past12months, including the last local election. FullCPSsample supplement;self-response attempted and proxy allowed. Census/nonresponse selection universe can differ from an archived rate's final valid denominator.

The exact archived state-rate missing/valid denominator implementation, respondentNs and designSE were not independently reconstructed from CEV person microdata in this finalization. Original published/archived values remain unchanged and carry this limitation. Availability of replicate files does not create designSEs for an archived rate without replicating its estimator. Final latentSE is model uncertainty, never original surveySE.

Historical contact has similar action/reference period, but age18+and rotation/design differences remain. Political consumption shifts from social/political company values to political values/business practices. Thus PARTIAL cross-regime equivalence, not identity.2011abstract implies outgoing rotation while actual valid raw coverage includes all8MIS;2013valid raw coverage3/4/7/8 versus outgoing-only abstract. Formal restriction is UNKNOWN—DOCUMENT/RAW CONFLICT. Operational raw selection and itemvalidNs/denominators are preserved in observed rows and prior extraction logs. NR160and4/160designSE applies only to the historical2011/2013extractions whose full-weight matches were verified.

Typical-month political discussion, habitual voting frequency, committee/officer service and volunteer-conditioned meeting attendance are NON-EQUIVALENT/PARTIAL alternatives, not substituted.2000–2009: NO DIRECT S5 ITEM OBSERVATION AVAILABLE IN CURRENT EVIDENCE.2008/2009source non-acquisition is not evidence of nonexistence.2000/2006community surveys do not establish50representative independent state rates.2012/2014–2016lack full basket observations in this package. Missing years are explicitly model estimated.

S7reference defines administrative general-election VEP turnout;local-election self-report is an electoral-domain overlap but a distinct election/reference/denominator construct. Active5 removes localvote only as sensitivity. S1–S4/S6/S7were not modified.

Official2019source:https://www2.census.gov/programs-surveys/cps/techdocs/cpssept19.pdf
Official2021source:https://www2.census.gov/programs-surveys/cps/techdocs/cpssept21.pdf
Other official URLs and acquisition hashes appear in source registry and embedded input manifests.
''')
(P/'S5_README_FINAL.md').write_text('''# S5 Active Civic Participation — canonical analytical release

RUN_ID:S5_ACTIVE6_FINAL_20261002_v1. PrimaryActive6 approved by Research Director on2026-10-02. Canonical unit is latentActive6 fixed2017input-indexSD, never a participation percentage.

S5_FINAL_2000_2023.csv/XLSX contains1,200state-years(50states×24years). Every analytical row is MODEL_ESTIMATED, including years with item observations. direct_input_available and full_basket_input_available identify the evidence supplied to the model. No direct observed values are overwritten by latent values.

S5_DIRECT_OBSERVATIONS_FINAL.csv is the2,300-row DIRECT item table:2,000unchanged archivedCEV item rates+300earliercontact/consumption rates. Historical waves do not become DIRECT fullActive6scores. The separate fixed6-input composite is a model measurement target, not an original survey percentage.

S5_SENSITIVITY_PANELS.csv holds13model/basket specifications,each1,200rows,includingActive5withoutlocalvote andBroad10. PrimaryCIusesonlyActive6modelvariants, not alternateconstructs. S5_SE is conditionalGaussianlatent uncertainty. CIis a nominal95percent model/specification envelope; it is not empirically calibrated coverage for latent truth. Consult model report before historical inference. All2000–2016rows carry full-basketbackcast flags;2000–2009has no directiteminputs. Known primarymeasurement limitations remain visible after freezing bytes.

## Reproduce
Extract theZIP to a new directory and run `OPENBLAS_NUM_THREADS=1 python finalize_s5.py > execution.log 2>&1`.Python3+numpy+scipyrequired. All numericalinputs,code,optimizer outputs,input/code hashes and executiontimestamps are supplied. Numeric model output does not depend onExcel. No network required to rerun the numericalpanel. `assemble_s5.py`creates documentation and source registry from the same results. `build_workbook.mjs`uses@oai/artifact-tool;runwiththeextractionrootargument after finalize_s5.py creates workbook_data.json. OriginalCensus PDFs are identified by acquisitionURL/SHA;full extractedtext is embedded. Priorupstreamitem extractioncode/manifests are retained, but upstream rawpersonfiles are external officialsources, not packed here. The archivedCEV state-rate denominator/design-SE limitation is not resolved by downstream modeling.

SHA256SUMS coverspackage members exceptitself. The outerZIPhash and remoteverification are recordedexternally to avoidself-reference. GitHub storesnativeCSV,MD,scripts,XLSXandthecompleteZIP;embeddedinputsareinsideZIP. GoogleDrivecontainsnativeZIP. Neither sourceRAW nor previousreviewpackagesareoverwritten. NoGitHubActions.
''')
registry=list(csv.DictReader((I/'S5_SOURCE_REGISTRY_REVIEW.csv').open()));registry.extend([dict(source=f'Census{y}officialcodebook',url=f'https://www2.census.gov/programs-surveys/cps/techdocs/cpssept{str(y)[2:]}.pdf',role='ExactActive6questionnaire/universe/weight/codes',status='OFFICIAL_PDF_ACQUIRED_TEXT_EXTRACTED',hash=next(r['sha256'] for r in json.loads((I/'NEW_DOCUMENT_ACQUISITION.json').read_text()) if r['year']==y)) for y in [2019,2021]]);registry.extend([dict(source='S7finalreferenceCSV_extractedfrompackage',url='https://drive.google.com/file/d/1oYaY4h4ruomHRlvM5NeCV1m1E9YpphkT/view',role='Readonlyoverlapsensitivity;finaltabledefinitionverified',status='READ_ONLY',hash=hashlib.sha256((I/'S7_reference/S7_FINAL_2000_2023.csv').read_bytes()).hexdigest()),dict(source='PIActive6approval',url='Userinstruction2026-10-02T13:43KST',role='Constructdecisionbeforefinalmodel',status='USER_METHODOLOGICAL_DECISION',hash=''),dict(source='GPMLChapter2',url='https://gaussianprocess.org/gpml/chapters/RW2.pdf',role='Gaussianconditioning/marginal-likelihoodreference',status='PRIMARY_AUTHOR_REFERENCE',hash='')]);write('S5_SOURCE_REGISTRY.csv',registry)
for n in ['finalize_s5.py','assemble_s5.py']:(P/n).write_bytes((R/n).read_bytes())
# Inputs immutable; noPDFbinaryduplication needed to preserve exactfulltext+originalacquisitionhash.
(P/'inputs').mkdir(exist_ok=True)
for x in I.rglob('*'):
 if x.is_file() and x.suffix!='.pdf':dest=P/'inputs'/x.relative_to(I);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(x,dest)
(P/'upstream').mkdir(exist_ok=True)
for n in ['build_review.py','prepare_replication.py']:(P/'upstream'/n).write_bytes(((R/'upstream'/n) if (R/'upstream'/n).exists() else (R.parent/'s5_final/review_package'/n)).read_bytes())
(P/'S5_EXECUTION_LOG.txt').write_bytes((R/'execution.log').read_bytes())
print(json.dumps(summary))
