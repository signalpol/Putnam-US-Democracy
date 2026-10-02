# S5 Active Civic Participation — canonical analytical release

RUN_ID:S5_ACTIVE6_FINAL_20261002_v1. PrimaryActive6 approved by Research Director on2026-10-02. Canonical unit is latentActive6 fixed2017input-indexSD, never a participation percentage.

S5_FINAL_2000_2023.csv/XLSX contains1,200state-years(50states×24years). Every analytical row is MODEL_ESTIMATED, including years with item observations. direct_input_available and full_basket_input_available identify the evidence supplied to the model. No direct observed values are overwritten by latent values.

S5_DIRECT_OBSERVATIONS_FINAL.csv is the2,300-row DIRECT item table:2,000unchanged archivedCEV item rates+300earliercontact/consumption rates. Historical waves do not become DIRECT fullActive6scores. The separate fixed6-input composite is a model measurement target, not an original survey percentage.

S5_SENSITIVITY_PANELS.csv holds13model/basket specifications,each1,200rows,includingActive5withoutlocalvote andBroad10. PrimaryCIusesonlyActive6modelvariants, not alternateconstructs. S5_SE is conditionalGaussianlatent uncertainty. CIis a nominal95percent model/specification envelope; it is not empirically calibrated coverage for latent truth. Consult model report before historical inference. All2000–2016rows carry full-basketbackcast flags;2000–2009has no directiteminputs. Known primarymeasurement limitations remain visible after freezing bytes.

## Reproduce
Extract theZIP to a new directory and run `OPENBLAS_NUM_THREADS=1 python finalize_s5.py > execution.log 2>&1`.Python3+numpy+scipyrequired. All numericalinputs,code,optimizer outputs,input/code hashes and executiontimestamps are supplied. Numeric model output does not depend onExcel. No network required to rerun the numericalpanel. `assemble_s5.py`creates documentation and source registry from the same results. `build_workbook.mjs`uses@oai/artifact-tool;runwiththeextractionrootargument after finalize_s5.py creates workbook_data.json. OriginalCensus PDFs are identified by acquisitionURL/SHA;full extractedtext is embedded. Priorupstreamitem extractioncode/manifests are retained, but upstream rawpersonfiles are external officialsources, not packed here. The archivedCEV state-rate denominator/design-SE limitation is not resolved by downstream modeling.

SHA256SUMS coverspackage members exceptitself. The outerZIPhash and remoteverification are recordedexternally to avoidself-reference. GitHub storesnativeCSV,MD,scripts,XLSXandthecompleteZIP;embeddedinputsareinsideZIP. GoogleDrivecontainsnativeZIP. Neither sourceRAW nor previousreviewpackagesareoverwritten. NoGitHubActions.
