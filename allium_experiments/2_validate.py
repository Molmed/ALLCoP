from conformist import AlphaSelector, \
    FNRCoP, PredictionDataset, ModelVsCopFNR
from lib.dual_subtype_heatmap import DualSubtypeHeatmap
from lib.constants import FORMATTED_PREDICTIONS_FILE, \
    FORMATTED_PREDICTIONS_FILE_ALL, \
    OUTPUT_DIR, \
    COLOR_PALETTE


OUTPUT_DIR_DATASET = f'{OUTPUT_DIR}/dataset'

# Create reports for entire dataset
apd = PredictionDataset(predictions_csv=FORMATTED_PREDICTIONS_FILE_ALL,
                        dataset_col_name='dataset')

# Get class counts and prediction heatmap
apd.run_reports(OUTPUT_DIR_DATASET,
                upset_plot_color='#457b9d',
                min_softmax_threshold=0.5,
                primary_class_only_in_class_counts=True,
                custom_color_palette=COLOR_PALETTE)

exit()

# TODO: DECIDE HOW TO RESEGMENT DATA FOR VALIDATION
# apd = PredictionDataset(predictions_csv=FORMATTED_PREDICTIONS_FILE,
#                         dataset_col_name='dataset')

# # Get class counts and prediction heatmap
# apd.run_reports(OUTPUT_DIR_DATASET,
#                 upset_plot_color='#457b9d',
#                 min_softmax_threshold=0.5,
#                 primary_class_only_in_class_counts=True,
#                 custom_color_palette=COLOR_PALETTE)

# Alpha selection
asel = AlphaSelector(apd, FNRCoP, OUTPUT_DIR_DATASET)
asel.run()
asel.run_reports()

# Compare Allium and FNRCoP performance
avaf = ModelVsCopFNR(apd, FNRCoP, OUTPUT_DIR_DATASET)
avaf.run()
avaf.run_reports()

# Render dual-class heatmap
dsh = DualSubtypeHeatmap(apd, OUTPUT_DIR_DATASET, 'Subtype 1', 'Subtype 2')
dsh.visualize()

ALPHAS = [0.075, 0.1, 0.15]

for ALPHA in ALPHAS:
    OUTPUT_DIR_VALIDATION = f'{OUTPUT_DIR}/validation_{ALPHA}'

    # Validation trial and reports
    mcp = FNRCoP(apd, alpha=ALPHA)
    trial = mcp.do_validation_trial(n_runs=10000)
    trial.run_reports(OUTPUT_DIR_VALIDATION)
