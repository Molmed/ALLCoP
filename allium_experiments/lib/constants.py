import os

# Grab all files in the data directory
# Get current script dir
script_dir = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(script_dir, '../data')
RAW_PREDICTIONS_DIR = os.path.join(DATA_DIR, 'raw_predictions')
