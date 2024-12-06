from conformist import AlphaSelector, \
    FNRCoP, PredictionDataset, ModelVsCopFNR
from lib.constants import FORMATTED_PREDICTIONS_FILE_ALL, \
    OUTPUT_DIR, \
    COLOR_PALETTE

# Create reports for entire dataset
apd = PredictionDataset(predictions_csv=FORMATTED_PREDICTIONS_FILE_ALL,
                        dataset_col_name='dataset')

# DATASET REPORTS
apd.create_reports_dir(f'{OUTPUT_DIR}/validation')
apd.visualize_class_counts_by_dataset(
    primary_class_only=True,
    custom_color_palette=COLOR_PALETTE,
    legend_top_padding=.2)

apd.visualize_prediction_stripplot(
    custom_color_palette=COLOR_PALETTE)
apd.softmax_summary()
apd.visualize_prediction_heatmap()
apd.visualize_model_sets(0.5, '#457b9d')

# Use single known subtype dataset for validation
# Alpha selection
asel = AlphaSelector(apd,
                     FNRCoP,
                     base_output_dir=OUTPUT_DIR,
                     n_runs_per_alpha=1000)
asel.run()
asel.run_reports()

# Compare Allium and FNRCoP performance
avaf = ModelVsCopFNR(apd, FNRCoP, OUTPUT_DIR, n_runs_per_alpha=1000)
avaf.run()
avaf.run_reports()

ALPHAS = [0.075, 0.1, 0.15]
n_runs = 1000

for ALPHA in ALPHAS:
    OUTPUT_DIR_VALIDATION = f'{OUTPUT_DIR}/validation_{ALPHA}'

    # Validation trial and reports
    mcp = FNRCoP(apd, alpha=ALPHA)
    trial = mcp.do_validation_trial(n_runs=n_runs, val_proportion=0.2)
    trial.run_reports(OUTPUT_DIR_VALIDATION)
    print(trial.mean_prediction_counts_by_class(trial.class_names, coocurring_only=True))
