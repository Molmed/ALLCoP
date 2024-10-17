from conformist import AlphaSelector, \
    FNRCoP, PredictionDataset, ModelVsCopFNR
# from lib.dual_subtype_heatmap import DualSubtypeHeatmap
from lib.constants import FORMATTED_PREDICTIONS_FILE, OUTPUT_DIR

# Read in formatted predictions
apd = PredictionDataset(predictions_csv=FORMATTED_PREDICTIONS_FILE,
                        dataset_col_name='dataset')

print(apd.df)
# Get class counts and prediction heatmap
apd.run_reports(OUTPUT_DIR)

exit()
# Render dual-class heatmap
dsh = DualSubtypeHeatmap(apd, JUDE_EXPERIMENTS_OUTPUT_DIR, 'Subtype 1', 'Subtype 2')
dsh.visualize()

# Alpha selection
asel = AlphaSelector(apd, FNRCoP, JUDE_EXPERIMENTS_OUTPUT_DIR)
asel.run()
asel.run_reports()

# Compare Allium and FNRCoP performance
avaf = ModelVsCopFNR(apd, FNRCoP, JUDE_EXPERIMENTS_OUTPUT_DIR)
avaf.run()
avaf.run_reports()

# Validation trial and reports
mcp = FNRCoP(apd, alpha=0.2)
trial = mcp.do_validation_trial(n_runs=10000)
trial.run_reports(JUDE_EXPERIMENTS_OUTPUT_DIR,
                  display_classes=DISPLAY_SUBTYPES_DICT)
