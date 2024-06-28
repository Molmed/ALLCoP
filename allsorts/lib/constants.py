import yaml
from conformist import PredictionDataset
from allium.subtype import Subtype
from allium.modality import GEX

EXCLUDE_ALLIUM_SUBTYPES = ['low HeH', 'Control']
ALLIUM_SUBTYPES = [subtype for subtype in Subtype.subtypes(GEX)
                   if subtype not in EXCLUDE_ALLIUM_SUBTYPES]


EXPERIMENTS_DIR = 'experiments/allsorts'
LIB_DIR = f'{EXPERIMENTS_DIR}/lib'
DATA_DIR = 'experiments/data'
PREDICTIONS_DIR = f'{DATA_DIR}/raw_predictions'
PHENOTYPES_DIR = f'{DATA_DIR}/phenotypes'

# Display dict
DISPLAY_SUBTYPES_YML = 'experiments/lib/allium_to_icc_subtypes.yml'
with open(DISPLAY_SUBTYPES_YML, 'r') as f:
    DISPLAY_SUBTYPES_DICT = yaml.safe_load(f)

# Phenotypes
PHENOTYPE_CSV = f'{PHENOTYPES_DIR}/phenotypes_finland_totxvi_krali.csv'
ALLSORTS_TO_ALLIUM_SUBTYPE_YML = f'{LIB_DIR}/allsorts_to_allium_subtypes.yml'

# Read in line separated text file as list
JUDE_UNKNOWNS = f'{PHENOTYPES_DIR}/jude_unclassified.txt'
with open(JUDE_UNKNOWNS, 'r') as f:
    JUDE_UNKNOWNS = f.read().splitlines()

# Load subtype mapping
with open(ALLSORTS_TO_ALLIUM_SUBTYPE_YML, 'r') as f:
    ALLSORTS_TO_ALLIUM_SUBTYPE_DICT = yaml.safe_load(f)

# RAW PREDICTION DATASETS #
ALLSORTS_PREDICTIONS_FINLAND_COHORT = \
    f'{PREDICTIONS_DIR}/allsorts_predictions_finland.csv'
ALLSORTS_PREDICTIONS_TOTXVI_COHORT = \
    f'{PREDICTIONS_DIR}/allsorts_predictions_totxvi.csv'
ALLSORTS_PREDICTIONS_KRALI_COHORT = \
    f'{PREDICTIONS_DIR}/allsorts_predictions_krali.csv'
ALLSORTS_PREDICTIONS_JUDE_COHORT = \
    f'{PREDICTIONS_DIR}/allsorts_predictions_jude.csv'

# OUTPUT FILES #
OUTPUT_ALLSORTS_DIR = 'output/allsorts'
UNKNOWNS_EXPERIMENTS_OUTPUT_DIR = f'{OUTPUT_ALLSORTS_DIR}/unknowns'

# FORMATTED PREDICTION FILES
FORMATTED_PREDICTIONS_DIR = f'{DATA_DIR}/formatted_predictions'
FORMATTED_PREDICTIONS_ALLSORTS = \
    f'{FORMATTED_PREDICTIONS_DIR}/allsorts_predictions_KRALI_FINLAND_TOTXVI.csv'
FORMATTED_PREDICTIONS_ALLSORTS_TALL = \
    f'{FORMATTED_PREDICTIONS_DIR}/allsorts_predictions_TALL.csv'
FORMATTED_PREDICTIONS_UNKNOWNS = \
    f'{FORMATTED_PREDICTIONS_DIR}/allsorts_predictions_UNKNOWNS.csv'
