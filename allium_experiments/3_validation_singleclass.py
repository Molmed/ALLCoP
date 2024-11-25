from conformist import FNRCoP, PredictionDataset, \
    ValidationTrial

from lib.constants import FORMATTED_PREDICTIONS_FILE_SINGLECLASS, \
    OUTPUT_DIR
from lib.prediction_comparison import PredictionComparison

# Here, we use St. Judes data for calibration and then get prediction
# sets for all of our validation cohorts
# Read in formatted predictions
apd = PredictionDataset(predictions_csv=FORMATTED_PREDICTIONS_FILE_SINGLECLASS,
                        dataset_col_name='dataset')

# Split the dataset into calibration and validation
jude_dataset_name = 'St. Jude Cloud (SJC-DS-1001, SJC-DS-1009)'
calibration = apd.df[apd.df['dataset'] == jude_dataset_name]
validation = apd.df[apd.df['dataset'] != jude_dataset_name]

cal_pd = PredictionDataset(df=calibration, dataset_col_name='dataset')
val_pd = PredictionDataset(df=validation, dataset_col_name='dataset')

# Print sizes of both datasets
print(f'Calibration dataset size: {cal_pd.df.shape[0]}')
print(f'Validation dataset size: {val_pd.df.shape[0]}')

OUTPUT_DIR_VAL = f'{OUTPUT_DIR}/validation_singleclass'

alphas = [0.075, 0.1, 0.15]
pc = PredictionComparison(OUTPUT_DIR_VAL, cal_pd, val_pd, alphas)
pc.visualize()

all_formatted_predictions = {}
all_validation_runs = {}
for alpha in alphas:
    mcp = FNRCoP(cal_pd, alpha=alpha)
    mcp.calibrate()

    # Remove dot from alpha
    alpha_str = str(alpha).replace('.', '')
    output_dir = f'{OUTPUT_DIR_VAL}/prediction_reports_{alpha_str}'

    formatted_predictions, validation_run = mcp.predict(val_pd,
                                                        output_dir,
                                                        validate=True)
    all_formatted_predictions[alpha] = formatted_predictions
    all_validation_runs[alpha] = validation_run.run_reports(output_dir)

# Merge all formatted predictions
pc.merge_prediction_sets(all_formatted_predictions)
pc.merge_stats(all_validation_runs)
