from conformist import AlphaSelector, \
    FNRCoP, PredictionDataset, ModelVsCopFNR
from lib.dual_subtype_heatmap import DualSubtypeHeatmap
from lib.constants import FORMATTED_PREDICTIONS_FILE, OUTPUT_DIR

OUTPUT_DIR_VALIDATION = f'{OUTPUT_DIR}/validation'

# Read in formatted predictions
apd = PredictionDataset(predictions_csv=FORMATTED_PREDICTIONS_FILE,
                        dataset_col_name='dataset')


# Get class counts and prediction heatmap
apd.run_reports(OUTPUT_DIR_VALIDATION)

# Alpha selection
asel = AlphaSelector(apd, FNRCoP, OUTPUT_DIR_VALIDATION)
asel.run()
asel.run_reports()

# Compare Allium and FNRCoP performance
avaf = ModelVsCopFNR(apd, FNRCoP, OUTPUT_DIR_VALIDATION)
avaf.run()
avaf.run_reports()

# Validation trial and reports
mcp = FNRCoP(apd, alpha=0.15)
trial = mcp.do_validation_trial(n_runs=10000)
trial.run_reports(OUTPUT_DIR_VALIDATION)

# Render dual-class heatmap
dsh = DualSubtypeHeatmap(apd, OUTPUT_DIR_VALIDATION, 'Subtype 1', 'Subtype 2')
dsh.visualize()
