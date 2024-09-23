import pandas as pd
from lib.allsorts_data_preprocessor import AllsortsDataPreprocessor

from lib.constants import (PHENOTYPE_CSV,
                           ALLSORTS_PREDICTIONS_KRALI_COHORT,
                           ALLSORTS_PREDICTIONS_FINLAND_COHORT,
                           JUDE_UNKNOWNS,
                           ALLSORTS_PREDICTIONS_JUDE_COHORT,
                           OUTPUT_ALLSORTS_DIR,
                           FORMATTED_PREDICTIONS_DIR)


# ST JUDE DATA PROCESSING #
japd = AllsortsDataPreprocessor(ALLSORTS_PREDICTIONS_JUDE_COHORT,
                                'JUDE_UNKNOWN',
                                id_col='id')

# Filter only those whose id matches the JUDE_UNKNOWNS
japd.df = japd.df[japd.df['id'].isin(JUDE_UNKNOWNS)]


# Phenotypes for the others
known_subtypes = pd.read_csv(PHENOTYPE_CSV)

# KRALI UNKNOWNS
kapd = AllsortsDataPreprocessor(ALLSORTS_PREDICTIONS_KRALI_COHORT,
                                'KRALI_UNKNOWN',
                                id_col='public_id',
                                known_class_df=known_subtypes)

# Filter for only unknowns
kapd.df = kapd.df[kapd.df['known_class'] == 'B-other']

# Append
japd.append_dataset(kapd)

# FINLAND UNKNOWNS
fapd = AllsortsDataPreprocessor(ALLSORTS_PREDICTIONS_FINLAND_COHORT,
                                'FINLAND_UNKNOWN',
                                id_col='EGAID',
                                known_class_df=known_subtypes)

# Filter only unknowns
fapd.df = fapd.df[fapd.df['known_class'] == 'B-other']

# Append
japd.append_dataset(fapd, 'UNKNOWNS')

# Drop known_class
japd.df.drop(columns='known_class', inplace=True)

# EXPORT
japd.save(OUTPUT_ALLSORTS_DIR)
japd.export(FORMATTED_PREDICTIONS_DIR)
