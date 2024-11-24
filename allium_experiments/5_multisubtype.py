from conformist import FNRCoP, PredictionDataset, \
    ValidationTrial

from lib.constants import FORMATTED_PREDICTIONS_FILE_SINGLECLASS, \
    FORMATTED_PREDICTIONS_FILE_MULTICLASS, \
    OUTPUT_DIR
from lib.prediction_comparison import PredictionComparison

# Here, we use all single-class data for calibration and then get prediction
# sets for all the multi-class data
cal_pd = PredictionDataset(
    predictions_csv=FORMATTED_PREDICTIONS_FILE_SINGLECLASS,
    dataset_col_name='dataset')
val_pd = PredictionDataset(
    predictions_csv=FORMATTED_PREDICTIONS_FILE_MULTICLASS,
    dataset_col_name='dataset')

# Print sizes of both datasets
print(f'Calibration dataset size: {cal_pd.df.shape[0]}')
print(f'Validation dataset size: {val_pd.df.shape[0]}')

alphas = [0.05, 0.075, 0.1, 0.15]
# pc = PredictionComparison(OUTPUT_DIR, cal_pd, val_pd, alphas)

for alpha in alphas:
    mcp = FNRCoP(cal_pd, alpha=alpha)
    mcp.calibrate()

    # Remove dot from alpha
    alpha_str = str(alpha).replace('.', '')
    output_dir = f'{OUTPUT_DIR}/prediction_multiclass_{alpha_str}'

    formatted_predictions = mcp.predict(val_pd,
                                        output_dir,
                                        validate=True)
