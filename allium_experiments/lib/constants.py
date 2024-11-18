import os
import yaml

# Grab all files in the data directory
# Get current script dir
script_dir = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(script_dir, '../data')
RAW_PREDICTIONS_DIR = os.path.join(DATA_DIR, 'raw_predictions')

# Read the YAML file
with open(f'{script_dir}/datasets.yml', 'r') as file:
    dm = yaml.safe_load(file)  # Parse YAML content
    DATASET_METADATA = dm['datasets']

FORMATTED_PREDICTIONS_FILE = \
    os.path.join(DATA_DIR, 'formatted_predictions_known_subtype.csv')
FORMATTED_PREDICTIONS_FILE_B_OTHER = \
    os.path.join(DATA_DIR, 'formatted_predictions_b_other.csv')
FORMATTED_PREDICTIONS_FILE_ALL = \
    os.path.join(DATA_DIR, 'formatted_predictions_known_and_b_other.csv')

OUTPUT_DIR = os.path.join(script_dir, '../../output')
