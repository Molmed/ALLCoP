import pandas as pd
from lib.allsorts_data_preprocessor import AllsortsDataPreprocessor

from lib.constants import (ALLSORTS_PREDICTIONS_FINLAND_COHORT,
                           ALLSORTS_PREDICTIONS_TOTXVI_COHORT,
                           ALLSORTS_PREDICTIONS_KRALI_COHORT,
                           PHENOTYPE_CSV,
                           OUTPUT_ALLSORTS_DIR,
                           FORMATTED_PREDICTIONS_DIR,
                           FORMATTED_PREDICTIONS_ALLSORTS_TALL)

known_subtypes = pd.read_csv(PHENOTYPE_CSV)

kapd = AllsortsDataPreprocessor(ALLSORTS_PREDICTIONS_KRALI_COHORT,
                                'KRALI',
                                id_col='public_id',
                                known_class_df=known_subtypes)

fapd = AllsortsDataPreprocessor(ALLSORTS_PREDICTIONS_FINLAND_COHORT,
                                'FINLAND',
                                id_col='EGAID',
                                known_class_df=known_subtypes)

gapd = AllsortsDataPreprocessor(ALLSORTS_PREDICTIONS_TOTXVI_COHORT,
                                'TOTXVI',
                                id_col='Sample SJ ID',
                                known_class_df=known_subtypes)
kapd.append_dataset(fapd)
kapd.append_dataset(gapd, 'KRALI_FINLAND_TOTXVI')

# Remove the B-other rows
kapd.df = kapd.df[kapd.df['known_class'] != 'B-other']

# Separate T-ALLs into separate df
t_all_df = kapd.df[kapd.df['known_class'] == 'T-ALL']
kapd.df = kapd.df[kapd.df['known_class'] != 'T-ALL']

kapd.save(OUTPUT_ALLSORTS_DIR)
kapd.export(FORMATTED_PREDICTIONS_DIR)

# Save T-ALLs separately
t_all_df.to_csv(FORMATTED_PREDICTIONS_ALLSORTS_TALL, index=False)
