import os
import yaml

# Grab all files in the data directory
# Get current script dir
script_dir = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(script_dir, '../data')
RAW_PREDICTIONS_DIR = os.path.join(DATA_DIR, 'raw_predictions')
MAIN_LIB_DIR = os.path.join(script_dir, '../../lib')

# Read a constant from colors.py file
COLORS_FILE = os.path.join(MAIN_LIB_DIR, 'colors.py')
with open(COLORS_FILE, 'r') as file:
    exec(file.read())

# Read the YAML file
with open(f'{MAIN_LIB_DIR}/datasets.yml', 'r') as file:
    dm = yaml.safe_load(file)  # Parse YAML content
    DATASET_METADATA = dm['datasets']

FORMATTED_PREDICTIONS_FILE_ALL = \
    os.path.join(DATA_DIR, 'formatted_predictions_all.csv')
FORMATTED_PREDICTIONS_FILE_B_OTHER = \
    os.path.join(DATA_DIR, 'formatted_predictions_b_other.csv')
FORMATTED_PREDICTIONS_FILE_MULTICLASS = \
    os.path.join(DATA_DIR, 'formatted_predictions_multiclass.csv')
FORMATTED_PREDICTIONS_FILE_SINGLECLASS = \
    os.path.join(DATA_DIR, 'formatted_predictions_singleclass.csv')

OUTPUT_DIR = os.path.join(script_dir, '../../output')
