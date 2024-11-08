from conformist import FNRCoP, PredictionDataset, \
    ValidationTrial

from lib.constants import FORMATTED_PREDICTIONS_FILE, \
    FORMATTED_PREDICTIONS_FILE_B_OTHER, OUTPUT_DIR

# Here, we use all known data for calibration and then get prediction
# sets for all of our validation cohorts
# Read in formatted predictions
cal_pd = PredictionDataset(predictions_csv=FORMATTED_PREDICTIONS_FILE,
                           dataset_col_name='dataset')

val_pd = PredictionDataset(predictions_csv=FORMATTED_PREDICTIONS_FILE_B_OTHER,
                           dataset_col_name='dataset')

print(f'Calibration dataset size: {cal_pd.df.shape[0]}')
print(f'Prediction dataset size: {val_pd.df.shape[0]}')

alphas = [0.075, 0.1, 0.15]
colors = ['#4f759b', '#5d5179', '#571f4e']

for alpha in alphas:
    # CALIBRATE CONFORMAL PREDICTOR #
    mcp = FNRCoP(cal_pd, alpha=alpha)
    mcp.calibrate()

    alpha_str = str(alpha).replace('.', '')
    output_dir = f'{OUTPUT_DIR}/b_other_{alpha_str}'

    # PREDICT #
    color = colors.pop(0)
    formatted_predictions = mcp.predict(val_pd,
                                        output_dir,
                                        upset_plot_color=color)
