import pandas as pd
from lib.jude_phenotype_parser import JudePhenotypeParser
from lib.allium_data_preprocessor import AlliumDataPreprocessor

# Constants
from lib.constants import (ALLIUM_PREDICTIONS_JUDE_COHORT,
                           ALLIUM_PREDICTIONS_FINLAND_COHORT,
                           ALLIUM_PREDICTIONS_TOTXVI_COHORT,
                           ALLIUM_PREDICTIONS_HOLDOUT_COHORT,
                           ALLIUM_PREDICTIONS_REPLICATES_COHORT,
                           ALLIUM_PREDICTION_LILLJEBJORN_COHORT,
                           JUDE_PHENOTYPE_TSV,
                           VALIDATION_PHENOTYPE_CSV,
                           VALIDATION_PHENOTYPE_LILLJEBJORN_CSV,
                           OUTPUT_DIR,
                           FORMATTED_PREDICTIONS_DIR)

# PARSE JUDE PHENOTYPE DATA #
# The phenotypes in the predictions file weren't quite right,
# so we need to re-parse the phenotype data from the St. Jude
# and export the ALLIUM-ified subtypes
jpp = JudePhenotypeParser(JUDE_PHENOTYPE_TSV, OUTPUT_DIR)

# PRINT SUMMARY OF PARSED PHENOTYPES #
jpp.print_summary()

# ST JUDE DATA PROCESSING #
japd = AlliumDataPreprocessor(ALLIUM_PREDICTIONS_JUDE_COHORT,
                              'JUDE',
                              id_col='sample_name',
                              predicted_class_col='GEX_subtype_V2',
                              known_class_df=jpp.df)

# EXPORT THE ALLIUM DATASET WITH JUDE PHENOTYPES MERGED IN #
japd.save(OUTPUT_DIR)
japd.export(FORMATTED_PREDICTIONS_DIR)

# NOW FORMAT ALL THE VALIDATION SETS
known_subtypes = pd.read_csv(VALIDATION_PHENOTYPE_CSV)

apd = AlliumDataPreprocessor(ALLIUM_PREDICTIONS_FINLAND_COHORT,
                             'FINLAND',
                             id_col='EGAID',
                             known_class_df=known_subtypes)

apdg = AlliumDataPreprocessor(ALLIUM_PREDICTIONS_TOTXVI_COHORT,
                              'TOTXVI',
                              id_col='Sample SJ ID',
                              known_class_df=known_subtypes)
apd.append_dataset(apdg)

apdh = AlliumDataPreprocessor(ALLIUM_PREDICTIONS_HOLDOUT_COHORT,
                              'KRALI_HOLDOUT',
                              id_col='public_id',
                              known_class_df=known_subtypes)
apd.append_dataset(apdh)

apdv = AlliumDataPreprocessor(ALLIUM_PREDICTIONS_REPLICATES_COHORT,
                              'KRALI_REPLICATES',
                              id_col='public_id',
                              known_class_df=known_subtypes)
apd.append_dataset(apdv)

known_subtypes_lilljebjorn = pd.read_csv(VALIDATION_PHENOTYPE_LILLJEBJORN_CSV)
apl = AlliumDataPreprocessor(ALLIUM_PREDICTION_LILLJEBJORN_COHORT,
                             'LILLJEBJORN',
                             id_col='public_id',
                             known_class_df=known_subtypes_lilljebjorn)
apd.append_dataset(apl, 'KRALI_FINLAND_TOTXVI_LILLJEBJORN')

# Remove the B-other rows
apd.df = apd.df[apd.df['known_class'] != 'B-other']

# Export them as one dataset
apd.save(OUTPUT_DIR)
apd.export(FORMATTED_PREDICTIONS_DIR)
