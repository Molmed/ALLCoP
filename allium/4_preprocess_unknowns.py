import pandas as pd
from lib.jude_phenotype_parser import JudePhenotypeParser
from lib.allium_data_preprocessor import AlliumDataPreprocessor

# Constants
from lib.constants import (ALLIUM_PREDICTIONS_JUDE_COHORT,
                           ALLIUM_PREDICTIONS_KRALI_UNKNOWN_COHORT,
                           ALLIUM_PREDICTIONS_FINLAND_COHORT,
                           ALLIUM_PREDICTIONS_HOLDOUT_COHORT,
                           ALLIUM_PREDICTIONS_REPLICATES_COHORT,
                           JUDE_PHENOTYPE_TSV,
                           VALIDATION_PHENOTYPE_CSV,
                           OUTPUT_DIR,
                           FORMATTED_PREDICTIONS_DIR)

# PARSE JUDE PHENOTYPE DATA #
# The phenotypes in the predictions file weren't quite right,
# so we need to re-parse the phenotype data from the St. Jude
# and export the ALLIUM-ified subtypes
jpp = JudePhenotypeParser(JUDE_PHENOTYPE_TSV, OUTPUT_DIR, include_unknowns=True)

# ST JUDE DATA PROCESSING #
japd = AlliumDataPreprocessor(ALLIUM_PREDICTIONS_JUDE_COHORT,
                              'JUDE_UNKNOWN',
                              id_col='sample_name',
                              predicted_class_col='GEX_subtype_V2',
                              known_class_df=jpp.df)

# Filter only unknowns
japd.df = japd.df[japd.df['known_class'] == 'B-other']

# NOW FORMAT ALL THE VALIDATION SETS
known_subtypes = pd.read_csv(VALIDATION_PHENOTYPE_CSV)

# KRALI UNKNOWNS
kapd = AlliumDataPreprocessor(ALLIUM_PREDICTIONS_KRALI_UNKNOWN_COHORT,
                              'KRALI_UNKNOWN',
                              id_col='public_id',
                              known_class_df=known_subtypes)

# Append
japd.append_dataset(kapd)

# FINLAND UNKNOWNS
fapd = AlliumDataPreprocessor(ALLIUM_PREDICTIONS_FINLAND_COHORT,
                              'FINLAND',
                              id_col='EGAID',
                              known_class_df=known_subtypes)

# Filter only unknowns
fapd.df = fapd.df[fapd.df['known_class'] == 'B-other']

# Append
japd.append_dataset(fapd)

# KRALI HOLDOUTS AND REPLICATES
apdh = AlliumDataPreprocessor(ALLIUM_PREDICTIONS_HOLDOUT_COHORT,
                              'KRALI_HOLDOUT',
                              id_col='public_id',
                              known_class_df=known_subtypes)

# Filter only unknowns
apdh.df = apdh.df[apdh.df['known_class'] == 'B-other']

# Append
japd.append_dataset(apdh)


# Replicates
apdv = AlliumDataPreprocessor(ALLIUM_PREDICTIONS_REPLICATES_COHORT,
                              'KRALI_REPLICATES',
                              id_col='public_id',
                              known_class_df=known_subtypes)

# Filter only unknowns
apdv.df = apdv.df[apdv.df['known_class'] == 'B-other']

# Append
japd.append_dataset(apdv, 'UNKNOWNS')

# Drop known_class
japd.df.drop(columns='known_class', inplace=True)

# EXPORT THE ALLIUM DATASET WITH JUDE PHENOTYPES MERGED IN #
japd.save(OUTPUT_DIR)
japd.export(FORMATTED_PREDICTIONS_DIR)
