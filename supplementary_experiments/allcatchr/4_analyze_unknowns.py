from conformist import FNRCoP, PredictionDataset

# Constants
from lib.constants import (UNKNOWNS_EXPERIMENTS_OUTPUT_DIR,
                           FORMATTED_PREDICTIONS_ALLCATCHR,
                           FORMATTED_PREDICTIONS_UNKNOWNS,
                           DISPLAY_SUBTYPES_DICT)

# Read in formatted predictions
apd = PredictionDataset('KRALI_FINLAND_GEO', predictions_csv=FORMATTED_PREDICTIONS_ALLCATCHR)
upd = PredictionDataset('UNKNOWNS',
                        predictions_csv=FORMATTED_PREDICTIONS_UNKNOWNS)

# Validation trial and reports
mcp = FNRCoP(apd, alpha=0.1)
mcp.calibrate()

# PREDICT #
formatted_predictions = mcp.predict(
    upd,
    UNKNOWNS_EXPERIMENTS_OUTPUT_DIR,
    validate=False,
    display_classes=DISPLAY_SUBTYPES_DICT,
    upset_plot_color="#352c85")
