from conformist import FNRCoP, PredictionDataset, \
    ValidationTrial

from lib.constants import FORMATTED_PREDICTIONS_FILE, OUTPUT_DIR
from lib.prediction_comparison import PredictionComparison

# Here, we use St. Judes data for calibration and then get prediction
# sets for all of our validation cohorts
# Read in formatted predictions
apd = PredictionDataset(predictions_csv=FORMATTED_PREDICTIONS_FILE,
                        dataset_col_name='dataset')

# Split the dataset into calibration and validation
calibration = apd.df[apd.df['dataset'] == 'jude']
validation = apd.df[apd.df['dataset'] != 'jude']

cal_pd = PredictionDataset(df=calibration, dataset_col_name='dataset')
val_pd = PredictionDataset(df=validation, dataset_col_name='dataset')

# Print sizes of both datasets
print(f'Calibration dataset size: {cal_pd.df.shape[0]}')
print(f'Validation dataset size: {val_pd.df.shape[0]}')

alphas = [0.075, 0.1, 0.15]
pc = PredictionComparison(OUTPUT_DIR, cal_pd, val_pd, alphas)

for alpha in alphas:
    mcp = FNRCoP(cal_pd, alpha=alpha)
    mcp.calibrate()

    # Remove dot from alpha
    alpha_str = str(alpha).replace('.', '')
    output_dir = f'{OUTPUT_DIR}/prediction_reports_{alpha_str}'

    formatted_predictions = mcp.predict(val_pd,
                                        output_dir,
                                        validate=True)

    # Get all formatted_predictions with a comma in prediction_sets
    multiclass_sets = formatted_predictions[
        formatted_predictions['prediction_sets'].str.contains(',')]

    # Dump to csv
    multiclass_sets.to_csv(
        f'{output_dir}/multiclass_sets.csv', index=False)
