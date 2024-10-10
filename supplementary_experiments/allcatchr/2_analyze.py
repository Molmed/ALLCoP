from conformist import AlphaSelector, FNRCoP, PredictionDataset, ModelVsCopFNR

# Constants
from lib.constants import (OUTPUT_ALLCATCHR_DIR,
                           FORMATTED_PREDICTIONS_ALLCATCHR,
                           FORMATTED_PREDICTIONS_ALLCATCHR_TALL,
                           DISPLAY_SUBTYPES_DICT)

# Read in formatted predictions
apd = PredictionDataset('KRALI_FINLAND_GEO',
                        predictions_csv=FORMATTED_PREDICTIONS_ALLCATCHR,
                        display_classes=DISPLAY_SUBTYPES_DICT)

# Get class counts and prediction heatmap
apd.run_reports(OUTPUT_ALLCATCHR_DIR)

# Alpha selection
asel = AlphaSelector(apd, FNRCoP, OUTPUT_ALLCATCHR_DIR)
asel.run()
asel.run_reports()

# Compare model and FNRCoP performance
avaf = ModelVsCopFNR(apd, FNRCoP, OUTPUT_ALLCATCHR_DIR)
avaf.run()
avaf.run_reports()

# Validation trial and reports
mcp = FNRCoP(apd, alpha=0.1)
trial = mcp.do_validation_trial(n_runs=10000)
trial.run_reports(OUTPUT_ALLCATCHR_DIR, display_classes=DISPLAY_SUBTYPES_DICT)

# What happens when you run the T-ALLs through the conformal predictor?
tall_pd = PredictionDataset('TALL',
                            predictions_csv=FORMATTED_PREDICTIONS_ALLCATCHR_TALL)

mcp = FNRCoP(apd, alpha=0.1)
mcp.calibrate()
output_dir = f'{OUTPUT_ALLCATCHR_DIR}/tall'
formatted_predictions, run = mcp.predict(tall_pd, output_dir, validate=True)
