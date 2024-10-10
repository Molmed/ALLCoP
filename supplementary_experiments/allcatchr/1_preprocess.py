import pandas as pd
from lib.allcatchr_data_preprocessor import AllcatchrDataPreprocessor

from lib.constants import (ALLCATCHR_PREDICTIONS_FINLAND_COHORT,
                           ALLCATCHR_PREDICTIONS_TOTXVI_COHORT,
                           ALLCATCHR_PREDICTIONS_KRALI_COHORT,
                           PHENOTYPE_CSV,
                           OUTPUT_ALLCATCHR_DIR,
                           FORMATTED_PREDICTIONS_DIR,
                           FORMATTED_PREDICTIONS_ALLCATCHR_TALL)

known_subtypes = pd.read_csv(PHENOTYPE_CSV)

kapd = AllcatchrDataPreprocessor(ALLCATCHR_PREDICTIONS_KRALI_COHORT,
                                 'KRALI',
                                 id_col='sample',
                                 known_class_df=known_subtypes)

fapd = AllcatchrDataPreprocessor(ALLCATCHR_PREDICTIONS_FINLAND_COHORT,
                                 'FINLAND',
                                 id_col='sample',
                                 known_class_df=known_subtypes)

gapd = AllcatchrDataPreprocessor(ALLCATCHR_PREDICTIONS_TOTXVI_COHORT,
                                 'TOTXVI',
                                 id_col='sample',
                                 known_class_df=known_subtypes)
kapd.append_dataset(fapd)
kapd.append_dataset(gapd, 'KRALI_FINLAND_TOTXVI')

# Remove the B-other rows
kapd.df = kapd.df[kapd.df['known_class'] != 'B-other']

# Separate T-ALLs into separate df
t_all_df = kapd.df[kapd.df['known_class'] == 'T-ALL']
kapd.df = kapd.df[kapd.df['known_class'] != 'T-ALL']

kapd.save(OUTPUT_ALLCATCHR_DIR)
kapd.export(FORMATTED_PREDICTIONS_DIR)

# Save T-ALLs separately
t_all_df.to_csv(FORMATTED_PREDICTIONS_ALLCATCHR_TALL, index=False)
