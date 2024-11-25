from conformist import AlphaSelector, \
    FNRCoP, PredictionDataset, ModelVsCopFNR
from lib.dual_subtype_heatmap import DualSubtypeHeatmap
from lib.constants import FORMATTED_PREDICTIONS_FILE_ALL, \
    FORMATTED_PREDICTIONS_FILE_SINGLECLASS, \
    OUTPUT_DIR, \
    COLOR_PALETTE

# Create reports for entire dataset
apd_all = PredictionDataset(predictions_csv=FORMATTED_PREDICTIONS_FILE_ALL,
                            dataset_col_name='dataset')

apd_all.create_reports_dir(f'{OUTPUT_DIR}/dataset_all')

apd_all.visualize_class_counts_by_dataset(
    primary_class_only=True,
    custom_color_palette=COLOR_PALETTE)

# Now create reports for single known subtype dataset
apd_filtered = PredictionDataset(
    predictions_csv=FORMATTED_PREDICTIONS_FILE_SINGLECLASS,
    dataset_col_name='dataset')

apd_filtered.create_reports_dir(f'{OUTPUT_DIR}/dataset_singleclass')

apd_filtered.visualize_prediction_stripplot(
    custom_color_palette=COLOR_PALETTE)
apd_filtered.softmax_summary()
apd_filtered.visualize_prediction_heatmap()
apd_filtered.visualize_model_sets(0.5, '#457b9d')

# Use single known subtype dataset for validation
# Alpha selection
asel = AlphaSelector(apd_filtered,
                     FNRCoP,
                     base_output_dir=OUTPUT_DIR,
                     n_runs_per_alpha=1000)
asel.run()
asel.run_reports()

# Compare Allium and FNRCoP performance
avaf = ModelVsCopFNR(apd_filtered, FNRCoP, OUTPUT_DIR, n_runs_per_alpha=10000)
avaf.run()
avaf.run_reports()

# Render dual-class heatmap
# dsh = DualSubtypeHeatmap(apd, OUTPUT_DIR_DATASET, 'Subtype 1', 'Subtype 2')
# dsh.visualize()

ALPHAS = [0.075, 0.1, 0.15]
n_runs = 10000

for ALPHA in ALPHAS:
    OUTPUT_DIR_VALIDATION = f'{OUTPUT_DIR}/validation_{ALPHA}'

    # Validation trial and reports
    mcp = FNRCoP(apd_filtered, alpha=ALPHA)
    trial = mcp.do_validation_trial(n_runs=n_runs, val_proportion=0.1)
    trial.run_reports(OUTPUT_DIR_VALIDATION)
