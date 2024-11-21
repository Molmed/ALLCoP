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
    os.path.join(DATA_DIR, 'formatted_predictions_single_known_subtype.csv')
FORMATTED_PREDICTIONS_FILE_B_OTHER = \
    os.path.join(DATA_DIR, 'formatted_predictions_b_other.csv')
FORMATTED_PREDICTIONS_FILE_MULTICLASS = \
    os.path.join(DATA_DIR, 'formatted_predictions_dual_known_subtype.csv')
FORMATTED_PREDICTIONS_FILE_ALL = \
    os.path.join(DATA_DIR, 'formatted_predictions.csv')

OUTPUT_DIR = os.path.join(script_dir, '../../output')

COLOR_PALETTE = {'high hyperdiploid': '#0F4D92',
                 'low hyperdiploid': '#1f77b4',
                 'iAMP21': '#17becf',
                 'hypodiploid': '#ACE5EE',
                 'ETV6::RUNX1': '#2ca02c',
                 'ETV6::RUNX1-like': '#98df8a',
                 'T-ALL': '#CD5C5C',
                 'KMT2A-r': '#FF7F50',
                 'NUTM1-r': '#ffbb78',
                 'PAX5alt': '#FC8EAC',
                 'PAX5 P80R': '#FBCCE7',
                 'TCF3::PBX1': '#20B2AA',
                 'MEF2D-r': '#30D5C8',
                 'BCR::ABL1': '#9467bd',
                 'BCR::ABL1-like': '#c5b0d5',
                 'DUX4-r': '#004953',
                 'ZNF384-r': '#8A496B',
                 'multiclass': '#FFD166',
                 'B-other': '#d4cbb3'}
