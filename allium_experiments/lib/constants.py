import os

# Grab all files in the data directory
# Get current script dir
script_dir = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(script_dir, '../data')
RAW_PREDICTIONS_DIR = os.path.join(DATA_DIR, 'raw_predictions')

FORMATTED_PREDICTIONS_FILE = \
    os.path.join(DATA_DIR, 'formatted_predictions.csv')
FORMATTED_PREDICTIONS_FILE_B_OTHER = \
    os.path.join(DATA_DIR, 'formatted_predictions_b_other.csv')

OUTPUT_DIR = os.path.join(script_dir, '../../output')
