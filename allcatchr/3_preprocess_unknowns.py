import pandas as pd
from lib.allcatchr_data_preprocessor import AllcatchrDataPreprocessor

from lib.constants import (PHENOTYPE_CSV,
                           ALLCATCHR_PREDICTIONS_KRALI_COHORT,
                           ALLCATCHR_PREDICTIONS_FINLAND_COHORT,
                           JUDE_UNKNOWNS,
                           ALLCATCHR_PREDICTIONS_JUDE_COHORT,
                           OUTPUT_ALLCATCHR_DIR,
                           FORMATTED_PREDICTIONS_DIR)


# ST JUDE DATA PROCESSING #
japd = AllcatchrDataPreprocessor(ALLCATCHR_PREDICTIONS_JUDE_COHORT,
                                 'JUDE_UNKNOWN',
                                 id_col='sample')

# Filter only those whose id matches the JUDE_UNKNOWNS
japd.df = japd.df[japd.df['id'].isin(JUDE_UNKNOWNS)]


# Phenotypes for the others
known_subtypes = pd.read_csv(PHENOTYPE_CSV)

# KRALI UNKNOWNS
kapd = AllcatchrDataPreprocessor(ALLCATCHR_PREDICTIONS_KRALI_COHORT,
                                 'KRALI_UNKNOWN',
                                 id_col='sample',
                                 known_class_df=known_subtypes)

# Filter for only unknowns
kapd.df = kapd.df[kapd.df['known_class'] == 'B-other']

# Append
japd.append_dataset(kapd)

# FINLAND UNKNOWNS
fapd = AllcatchrDataPreprocessor(ALLCATCHR_PREDICTIONS_FINLAND_COHORT,
                                 'FINLAND_UNKNOWN',
                                 id_col='sample',
                                 known_class_df=known_subtypes)

# Filter only unknowns
fapd.df = fapd.df[fapd.df['known_class'] == 'B-other']

# Append
japd.append_dataset(fapd, 'UNKNOWNS')

# Drop known_class
japd.df.drop(columns='known_class', inplace=True)

# EXPORT
japd.save(OUTPUT_ALLCATCHR_DIR)
japd.export(FORMATTED_PREDICTIONS_DIR)
