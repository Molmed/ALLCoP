from conformist import FNRCoP, PredictionDataset, \
    ValidationTrial

from lib.constants import FORMATTED_PREDICTIONS_FILE, \
    FORMATTED_PREDICTIONS_FILE_B_OTHER, OUTPUT_DIR

OUTPUT_DIR_B_OTHER = f'{OUTPUT_DIR}/b_other'

# Here, we use all known data for calibration and then get prediction
# sets for all of our validation cohorts
# Read in formatted predictions
cal_pd = PredictionDataset(predictions_csv=FORMATTED_PREDICTIONS_FILE,
                           dataset_col_name='dataset')

val_pd = PredictionDataset(predictions_csv=FORMATTED_PREDICTIONS_FILE_B_OTHER,
                           dataset_col_name='dataset')

# CALIBRATE CONFORMAL PREDICTOR #
mcp = FNRCoP(cal_pd, alpha=0.10)
mcp.calibrate()

# PREDICT #
formatted_predictions = mcp.predict(val_pd, OUTPUT_DIR_B_OTHER)
