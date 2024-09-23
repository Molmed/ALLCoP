from conformist import FNRCoP, PredictionDataset

# Constants
from lib.constants import (UNKNOWNS_EXPERIMENTS_OUTPUT_DIR,
                           FORMATTED_PREDICTIONS_JUDE,
                           FORMATTED_PREDICTIONS_UNKNOWNS,
                           DISPLAY_SUBTYPES_DICT)

# Read in formatted predictions
apd = PredictionDataset('JUDE', predictions_csv=FORMATTED_PREDICTIONS_JUDE)
upd = PredictionDataset('UNKNOWNS',
                        predictions_csv=FORMATTED_PREDICTIONS_UNKNOWNS)

# Validation trial and reports
mcp = FNRCoP(apd, alpha=0.2) # Change to 0.1 to compare
mcp.calibrate()

# PREDICT #
formatted_predictions = mcp.predict(
    upd,
    UNKNOWNS_EXPERIMENTS_OUTPUT_DIR,
    validate=False,
    display_classes=DISPLAY_SUBTYPES_DICT,
    upset_plot_color="#287979")
