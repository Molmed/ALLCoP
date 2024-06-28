import yaml
from conformist import PredictionDataset
from allium.subtype import Subtype
from allium.modality import GEX

EXCLUDE_ALLIUM_SUBTYPES = ['low HeH', 'Control']
ALLIUM_SUBTYPES = [subtype for subtype in Subtype.subtypes(GEX)
                   if subtype not in EXCLUDE_ALLIUM_SUBTYPES]



EXPERIMENTS_DIR = 'experiments/allcatchr'
LIB_DIR = f'{EXPERIMENTS_DIR}/lib'
DATA_DIR = 'experiments/data'
PREDICTIONS_DIR = f'{DATA_DIR}/raw_predictions'
PHENOTYPES_DIR = f'{DATA_DIR}/phenotypes'

# Phenotypes
PHENOTYPE_CSV = f'{PHENOTYPES_DIR}/phenotypes_finland_totxvi_krali.csv'
ALLCATCHR_TO_ALLIUM_SUBTYPE_YML = f'{LIB_DIR}/allcatchr_to_allium_subtypes.yml'

# Read in line separated text file as list
JUDE_UNKNOWNS = f'{PHENOTYPES_DIR}/jude_unclassified.txt'
with open(JUDE_UNKNOWNS, 'r') as f:
    JUDE_UNKNOWNS = f.read().splitlines()

# Load subtype mapping
with open(ALLCATCHR_TO_ALLIUM_SUBTYPE_YML, 'r') as f:
    ALLCATCHR_TO_ALLIUM_SUBTYPE_DICT = yaml.safe_load(f)

# Display dict
DISPLAY_SUBTYPES_YML = 'experiments/lib/allium_to_icc_subtypes.yml'
with open(DISPLAY_SUBTYPES_YML, 'r') as f:
    DISPLAY_SUBTYPES_DICT = yaml.safe_load(f)

# RAW PREDICTION DATASETS #
ALLCATCHR_PREDICTIONS_FINLAND_COHORT = \
    f'{PREDICTIONS_DIR}/allcatchr_predictions_finland.tsv'
ALLCATCHR_PREDICTIONS_TOTXVI_COHORT = \
    f'{PREDICTIONS_DIR}/allcatchr_predictions_totxvi.tsv'
ALLCATCHR_PREDICTIONS_KRALI_COHORT = \
    f'{PREDICTIONS_DIR}/allcatchr_predictions_krali.tsv'
ALLCATCHR_PREDICTIONS_JUDE_COHORT = \
    f'{PREDICTIONS_DIR}/allcatchr_predictions_jude.tsv'

# OUTPUT FILES #
OUTPUT_ALLCATCHR_DIR = 'output/allcatchr'
UNKNOWNS_EXPERIMENTS_OUTPUT_DIR = f'{OUTPUT_ALLCATCHR_DIR}/unknowns'

# FORMATTED PREDICTION FILES
FORMATTED_PREDICTIONS_DIR = f'{DATA_DIR}/formatted_predictions'
FORMATTED_PREDICTIONS_ALLCATCHR = \
    f'{FORMATTED_PREDICTIONS_DIR}/allcatchr_predictions_KRALI_FINLAND_TOTXVI.csv'
FORMATTED_PREDICTIONS_ALLCATCHR_TALL = \
    f'{FORMATTED_PREDICTIONS_DIR}/allcatchr_predictions_TALL.csv'
FORMATTED_PREDICTIONS_UNKNOWNS = \
    f'{FORMATTED_PREDICTIONS_DIR}/allcatchr_predictions_UNKNOWNS.csv'
