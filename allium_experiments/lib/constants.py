import yaml
from conformist import PredictionDataset
from allium import Subtype
from allium import GEX

EXCLUDE_ALLIUM_SUBTYPES = ['low HeH', 'Control']
ALLIUM_SUBTYPES = [subtype for subtype in Subtype.subtypes(GEX)
                   if subtype not in EXCLUDE_ALLIUM_SUBTYPES]

# Column names
KNOWN_CLASSES_COL = PredictionDataset.KNOWN_CLASS_COL
KNOWN_PRIMARY_CLASS_COL = f'{KNOWN_CLASSES_COL}_1'
KNOWN_SECONDARY_CLASS_COL = f'{KNOWN_CLASSES_COL}_2'

# DEFINE ALLIUM PREDICTION FILES #
ALLIUM_DIR = 'allium_experiments'
ALLIUM_LIB_DIR = f'{ALLIUM_DIR}/lib'
DATA_DIR = 'data'
ALLIUM_PREDICTIONS_DIR = f'{DATA_DIR}/raw_predictions'
ALLIUM_PHENOTYPES_DIR = f'{DATA_DIR}/phenotypes'

# St. Jude data
ALLIUM_PREDICTIONS_JUDE_COHORT = \
    f'{ALLIUM_PREDICTIONS_DIR}/allium_predictions_stjude.csv'
JUDE_PHENOTYPE_TSV = f'{ALLIUM_PHENOTYPES_DIR}/phenotypes_jude.tsv'
JUDE_TO_ALLIUM_SUBTYPE_YML = f'{ALLIUM_LIB_DIR}/jude_to_allium_subtypes.yml'
VALIDATION_PHENOTYPE_CSV = \
    f'{ALLIUM_PHENOTYPES_DIR}/phenotypes_finland_totxvi_krali.csv'
VALIDATION_PHENOTYPE_LILLJEBJORN_CSV = \
    f'{ALLIUM_PHENOTYPES_DIR}/phenotypes_lilljebjorn.csv'
VALIDATION_PHENOTYPE_TRAN_CSV = \
    f'{ALLIUM_PHENOTYPES_DIR}/phenotypes_tran.csv'

# Load subtype mapping
with open(JUDE_TO_ALLIUM_SUBTYPE_YML, 'r') as f:
    JUDE_TO_ALLIUM_SUBTYPE_DICT = yaml.safe_load(f)

# Display dict
DISPLAY_SUBTYPES_YML = f'{ALLIUM_LIB_DIR}/allium_to_icc_subtypes.yml'
with open(DISPLAY_SUBTYPES_YML, 'r') as f:
    DISPLAY_SUBTYPES_DICT = yaml.safe_load(f)

# OUTPUT FILES #
OUTPUT_DIR = 'output/allium'
JUDE_EXPERIMENTS_OUTPUT_DIR = f'{OUTPUT_DIR}/jude'
UNKNOWNS_EXPERIMENTS_OUTPUT_DIR = f'{OUTPUT_DIR}/unknowns'

# FORMATTED PREDICTION FILES
FORMATTED_PREDICTIONS_DIR = f'{DATA_DIR}/formatted_predictions'
FORMATTED_PREDICTIONS_JUDE = \
    f'{FORMATTED_PREDICTIONS_DIR}/allium_predictions_JUDE.csv'

# VALIDATION DATASETS #
ALLIUM_PREDICTIONS_FINLAND_COHORT = \
    f'{ALLIUM_PREDICTIONS_DIR}/allium_predictions_finland.csv'
ALLIUM_PREDICTIONS_TOTXVI_COHORT = \
    f'{ALLIUM_PREDICTIONS_DIR}/allium_predictions_totxvi.csv'
ALLIUM_PREDICTIONS_HOLDOUT_COHORT = \
    f'{ALLIUM_PREDICTIONS_DIR}/allium_predictions_krali_holdout.csv'
ALLIUM_PREDICTIONS_REPLICATES_COHORT = \
    f'{ALLIUM_PREDICTIONS_DIR}/allium_predictions_krali_replicates.csv'
ALLIUM_PREDICTIONS_KRALI_UNKNOWN_COHORT = \
    f'{ALLIUM_PREDICTIONS_DIR}/allium_predictions_krali_unknown_subtype.csv'
ALLIUM_PREDICTION_LILLJEBJORN_COHORT = \
    f'{ALLIUM_PREDICTIONS_DIR}/allium_predictions_lilljebjorn.csv'
ALLIUM_PREDICTION_TRAN_COHORT = \
    f'{ALLIUM_PREDICTIONS_DIR}/allium_predictions_tran.csv'
FORMATTED_PREDICTIONS_VALIDATION = \
    f'{FORMATTED_PREDICTIONS_DIR}/allium_predictions_KRALI_FINLAND_TOTXVI_LILLJEBJORN_TRAN.csv'
FORMATTED_PREDICTIONS_UNKNOWNS = \
    f'{FORMATTED_PREDICTIONS_DIR}/allium_predictions_UNKNOWNS.csv'
FORMATTED_PREDICTIONS_LILLJEBJORN = \
    f'{FORMATTED_PREDICTIONS_DIR}/allium_predictions_LILLJEBJORN.csv'
FORMATTED_PREDICTIONS_TRAN = \
    f'{FORMATTED_PREDICTIONS_DIR}/allium_predictions_TRAN.csv'

UPSET_PLOT_SOURCE = \
    f'{FORMATTED_PREDICTIONS_DIR}/upset_allcop_allium.csv'
