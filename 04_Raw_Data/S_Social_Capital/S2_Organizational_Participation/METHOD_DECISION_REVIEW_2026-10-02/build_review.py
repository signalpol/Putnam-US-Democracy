"""Assemble a decision review package; never label it FINAL or FROZEN."""
from pathlib import Path
import csv,json,hashlib,shutil,zipfile,datetime
R=Path(__file__).resolve().parent;D=R/'decision_review';D.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def csvout(name,rows):
 with (D/name).open('w',newline='') as h:
  w=csv.DictWriter(h,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for p in (R/'diagnostics').iterdir():shutil.copy2(p,D/p.name)
for p in [R/'compare_models.py',R/'model_stdout.log',R/'inputs/canonical_base.csv',R/'inputs/acquisition_followup.json']:shutil.copy2(p,D/p.name)
shutil.copy2(Path(__file__),D/'build_review.py')
base=list(csv.DictReader((D/'canonical_base.csv').open()))
drive=Path('/workspace/scratch/9eb6fec78fce/attachments/90830aad-d602-420b-96e8-1924e1ba55c8/S2_Organizational_Participation_CANONICAL_BASE_8_DIRECT_YEARS_2009_2023.csv')
dr=list(csv.DictReader(drive.open()))
di={(x['state'],int(x['year'])):x for x in dr}
errors=[(x['state'],x['year']) for x in base if float(x['s2_participation'])!=float(di[(x['state'],int(x['year']))]['s2_participation'])]
local=[]
paths={2009:Path('2009_api_run/S2_2009_50_STATES_DIRECT.csv'),2010:Path('2010_run/S2_Organizational_Participation_2010_DIRECT_v1.csv'),2011:Path('2011_run/S2_Organizational_Participation_2011_DIRECT_v1.csv'),2013:Path('2013_run/S2_Organizational_Participation_2013_DIRECT_v1.csv')}
for yr,p in paths.items():
 if p.exists():
  a=list(csv.DictReader(p.open()));indexed={x.get('state',x.get('state_abbr')):x for x in a};diff=[]
  for x in [x for x in base if int(x['year'])==yr]:
   o=indexed[x['state']];col='s2_participation' if 's2_participation' in o else 'value';original=float(o[col])/(100 if o.get('unit')=='percent' else 1);diff.append(abs(float(x['s2_participation'])-original))
  local.append(dict(year=yr,rows=len(a),max_absolute_difference=max(diff),rounding_tolerance=5.1e-11,PASS=max(diff)<=5.1e-11,source_file=str(p),source_sha256=sha(p)))
csvout('S2_INHERITED_DIRECT_VALUE_COMPARISON.csv',local)
qa=[dict(check='Inherited rows',observed=len(base),expected=400,status='PASS' if len(base)==400 else 'FAIL'),dict(check='Inherited states',observed=len({x['state'] for x in base}),expected=50,status='PASS'),dict(check='Inherited duplicate state-year',observed=len(base)-len({(x['state'],x['year']) for x in base}),expected=0,status='PASS'),dict(check='GitHub versus Drive parsed direct values',observed=len(errors),expected=0,status='PASS' if not errors else 'FAIL'),dict(check='Prior CPS raw-derived outputs preserved within base rounding',observed=sum(x['PASS'] for x in local),expected=4,status='PASS' if all(x['PASS'] for x in local) else 'FAIL'),dict(check='Final 1200-row canonical panel',observed='NOT GENERATED',expected=1200,status='BLOCKED_METHOD_DECISION'),dict(check='2008 raw acquisition',observed='NOT ACQUIRED',expected='Raw microdata or evidence of methodological impossibility',status='UNRESOLVED'),dict(check='Model selection',observed='M1 and M2 materially diverge; similar holdout',expected='PI target/regime decision',status='BLOCKED_METHOD_DECISION')]
csvout('S2_REVIEW_QA.csv',qa)
source=[]
urls={'cpsnov08c.pdf':'https://www2.census.gov/programs-surveys/cps/techdocs/cpsnov08c.pdf','variables.json':'https://api.census.gov/data/2008/cps/civic/nov/variables.json','cpssep17.pdf':'https://www2.census.gov/programs-surveys/cps/techdocs/cpssep17.pdf','cpssep23.pdf':'https://www2.census.gov/programs-surveys/cps/techdocs/cpssep23.pdf','usmisc2006-soccap.pdf':'https://ropercenter.cornell.edu/sites/default/files/pdf/usmisc2006-soccap.pdf','canonical_base.csv':'https://raw.githubusercontent.com/signalpol/Putnam-US-Democracy/main/04_Raw_Data/S2_Organizational_Participation/S2_Organizational_Participation_CANONICAL_BASE_8_DIRECT_YEARS_2009_2023.csv'}
for n,u in urls.items():
 p=R/'inputs'/n
 if p.exists():source.append(dict(file=n,url=u,bytes=p.stat().st_size,sha256=sha(p),role='BASE' if n=='canonical_base.csv' else 'DOCUMENTATION_ONLY',packaged=n=='canonical_base.csv'))
source.append(dict(file='Drive canonical base CSV export',url='https://docs.google.com/spreadsheets/d/1HYa7Uj4NP8NrrNWzpM1INT4gSr0EoUpQ8HIzly8bnVI/edit',bytes=drive.stat().st_size,sha256=sha(drive),role='INDEPENDENT_BASE_COMPARISON',packaged=False))
csvout('S2_SOURCE_REGISTRY.csv',source)
(D/'S2_MEASUREMENT_EQUIVALENCE_AUDIT.md').write_text('''# S2 measurement review — decision required

This is a provisional audit, not a claim that all wave documentation is verified.

| Wave | Indicator | Minimum age | Operational sample / rotation | Weight / SE evidence | Status |
|---|---|---|---|---|---|
|2008|PEQ5A–E; any participation across five categories|15+|All applicable civilian household persons; self or proxy|PWNRWGT, revised November 2010; raw/replicates not acquired|DOCUMENT VERIFIED / RAW UNRESOLVED|
|2009|PEQ5A–E; any participation|18+|Outgoing MIS 4/8, supplement interview|PWNRWGT; inherited SE not verified|Inherited direct package|
|2010|PEQ5A–E; any participation|18+|Raw all eight MIS; self/proxy reporter 15+|PWNRWGT; inherited SE not verified|Wording and universe break from 2009 preserved|
|2011|PES5A–E; any participation|18+|Raw all eight MIS; outgoing-only document conflict|PWNRWGT; verified 160 NR replicates, 4/160|UNKNOWN — DOCUMENT/RAW CONFLICT for formal rotation|
|2013|PES5A–E; any participation|18+|Raw MIS 3/4/7/8; abstract/overview conflict|PWNRWGT; verified 160 NR replicates, 4/160|UNKNOWN — DOCUMENT/RAW CONFLICT for formal rotation|
|2017|PES15; any membership|16+|Full CPS supplement; attempted self, proxy permitted|PWNRWGT in Census codebook; archived rate SE absent|Census document independently read; archived denominator details not yet independently verified|
|2019|Archived organizational membership rate|Not independently verified in this run|UNKNOWN|Archived rate; SE absent|2019 documentation acquisition unresolved; do not infer identical design|
|2021|Archived organizational membership rate|Not independently verified in this run|UNKNOWN|Archived rate; SE absent|2021 documentation acquisition unresolved; do not infer identical design|
|2023|PES15; any membership|16+|Full CPS, randomly selected household members; self attempted and proxy allowed|PWNRWGT except specified self-only variables; archived rate SE absent|Census document independently read; archived denominator details not yet independently verified|

Early categories: school/neighborhood/community; service/civic; sports/recreation; religious excluding service attendance; other. CEV PES15 does not enumerate these categories. Participation and belonging are different question predicates. Reference windows change from November to September; minimum age changes; respondent selection changes. No wave in the base applies both predicates concurrently. The base contains no empirical cross-regime calibration anchor.

Codes in 2008 and 2023 documentation: 1 yes, 2 no; -1 NIU, -2 DK, -3 refused, -9 no answer. The 2017 layout additionally lists 0 zero for PES15, requiring archived denominator clarification. A shared variable name or weight label does not establish measurement equivalence.

2000 SCCBS and 2006 SCCS include national/community samples rather than 50 independently representative state samples. These are auxiliary evidence, not 50-state DIRECT observations. This is not proof that every conceivable 2000–2007 source is absent.

2008: Census directory and candidate paths did not provide microdata; NBER candidate files returned 403; public API returned Missing Key HTML rather than observations. Weiss materials reviewed point to IPUMS and did not yield a raw replication file. ICPSR upload has documentation only. These are acquisition limitations, not evidence of methodological impossibility. No 2008 direct values are invented.
''')
(D/'S2_MODEL_VALIDATION_REPORT.md').write_text('''# Model comparison and research decision

Only the inherited 400 direct values were used. Source estimates were never replaced. Diagnostic annual predictions are not canonical estimates.

M0: Gaussian logit mixed model, random state intercept, common linear trend, independently estimated error variance for observations without verified SE.
M1: M0 plus state and common temporal Gaussian processes, exponential covariance with fixed six-year length scale.
M2: M1 plus CEV measurement-regime offset. Both model fitting and prediction use GLS, conditional covariance and likelihood maximization from two starts.

Known 2011/2013 SEs enter through the delta-method logit variance. Other wave SEs remain unknown; fitted nuisance error is model-based, not design-based. Intervals condition on estimated covariance parameters, omit full hyperparameter uncertainty, and do not validate nine-year extrapolation. Holdout coverage evaluates withheld direct estimates, not unobserved true participation.

Five complete-wave holdouts (2009/2011/2013/2019/2021), 250 state-wave predictions per candidate, were actually executed. M1 RMSE 0.040723, MAE 0.032457, coverage 94.8%; M2 RMSE 0.040160, MAE 0.032932, coverage 95.6%. M2 improves RMSE by only 0.000563 (0.0563 percentage points). AIC slightly favors M2 (-238.51 versus -237.62); BIC favors M1 (-213.67 versus -210.57). Both optimizations converged; gradients are small. A full numerical Hessian, process length-scale sensitivity and hyperparameter uncertainty have not been verified, so these are not approved final specifications.

Despite similar holdout performance, model annual diagnostic averages differ materially: 2000 M1 46.44%, M2 39.93% (6.52pp); 2015 M1 33.83%, M2 38.22% (4.40pp). The common logit trend per decade is -0.38782 for M1 versus -0.09015 for M2. M2 regime offset is -0.38713 with conditional SE 0.20616. Its nominal interval includes zero. Temporal change and regime offset are weakly separable under these process assumptions and are not nonparametrically identified by these nonoverlapping waves.

M2 predictions include the observed-scale CEV offset after 2017. They are not a silently regime-adjusted latent series. A common-target counterfactual would require choosing an anchor and interpreting or constraining that offset. Keeping every direct value unchanged while calling a mixed-predicate annual series measurement invariant would be misleading.

The user's sole research-decision STOP condition is met: two plausible temporal/regime treatments have similar predictive evidence but produce materially different historical levels and decline. PI decision required: choose a descriptive mixed-regime annual construct with explicit discontinuity, or authorize a common-target calibration with substantive anchoring assumptions. The latter also requires clarifying how unchanged direct values coexist with separately harmonized latent estimates.

No FINAL/FROZEN package or 1200-row canonical panel has been declared. The next authorized work after this decision includes resolved 2008 status, full wave documentation, Hessian/length-scale/offset sensitivity, approved specification, canonical QA and final dual-store verification.
''')
(D/'README.md').write_text('''# S2 METHOD DECISION REVIEW — NOT FINAL / NOT FROZEN

Run the preserved `compare_models.py` from the directory above `inputs/canonical_base.csv`; alternatively copy packaged `canonical_base.csv` into `inputs/`. Dependencies: Python, numpy, scipy. No new raw extraction of 2009–2013 was performed. The original base is immutable; its SHA256 is in MODEL_RUN_MANIFEST.json. The 3600 diagnostic predictions are three alternative 1200-row model outputs, not a final panel. No canonical annual values are approved.

Decision: measurement-regime treatment changes substantive historical results and cannot be selected confidently from holdout performance. Review S2_MODEL_VALIDATION_REPORT.md. Acquisition failure does not prove 2008 data are methodologically unusable.

ZIP hash and remote verification are recorded externally, avoiding self-referential hashes. SHA256SUMS.txt excludes itself. No Census key, workflows, or messages to third parties are used.
''')
files=sorted(p for p in D.iterdir() if p.name!='SHA256SUMS.txt')
(D/'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.name}\n' for p in files))
z=R/'S2_METHOD_DECISION_REVIEW_2026-10-02.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as h:
 for p in sorted(D.iterdir()):h.write(p,p.name)
print(json.dumps(dict(files=len(list(D.iterdir())),zip_bytes=z.stat().st_size,zip_sha256=sha(z),github_drive_parsed_mismatches=len(errors),prior_comparison=local),indent=2))
