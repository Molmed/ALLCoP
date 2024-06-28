# TODO: how about simplecop as well?
from conformist import AlphaSelector, FNRCoP, PredictionDataset, ModelVsCopFNR

# Constants
from lib.constants import (OUTPUT_ALLSORTS_DIR,
                           FORMATTED_PREDICTIONS_ALLSORTS,
                           FORMATTED_PREDICTIONS_ALLSORTS_TALL,
                           DISPLAY_SUBTYPES_DICT)

# Read in formatted predictions
apd = PredictionDataset('KRALI_FINLAND_GEO',
                        predictions_csv=FORMATTED_PREDICTIONS_ALLSORTS,
                        display_classes=DISPLAY_SUBTYPES_DICT)

# Get class counts and prediction heatmap
apd.run_reports(OUTPUT_ALLSORTS_DIR)

# Alpha selection
asel = AlphaSelector(apd, FNRCoP, OUTPUT_ALLSORTS_DIR)
asel.run()
asel.run_reports()

# Compare model and FNRCoP performance
avaf = ModelVsCopFNR(apd, FNRCoP, OUTPUT_ALLSORTS_DIR)
avaf.run()
avaf.run_reports()

# Validation trial and reports
mcp = FNRCoP(apd, alpha=0.05)
trial = mcp.do_validation_trial(n_runs=10000)
trial.run_reports(OUTPUT_ALLSORTS_DIR, display_classes=DISPLAY_SUBTYPES_DICT)

# What happens when you run the T-ALLs through the conformal predictor?
tall_pd = PredictionDataset('TALL', predictions_csv=FORMATTED_PREDICTIONS_ALLSORTS_TALL)

mcp = FNRCoP(apd, alpha=0.1)
mcp.calibrate()
output_dir = f'{OUTPUT_ALLSORTS_DIR}/tall'
formatted_predictions, run = mcp.predict(tall_pd, output_dir, validate=True)
