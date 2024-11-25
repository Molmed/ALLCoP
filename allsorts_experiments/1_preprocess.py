import pandas as pd
import os
from lib.allsorts_data_preprocessor import AllsortsDataPreprocessor
from lib.constants import RAW_PREDICTIONS_DIR, \
    FORMATTED_PREDICTIONS_FILE_ALL, \
    DATASET_METADATA, \
    PHENOTYPES_DIR

print('Preprocessing raw predictions...')

subtypes_to_exclude = ['Control', 'NUTM1-r', 'low hyperdiploid', 'T-ALL']

dataframes = []
for dataset in DATASET_METADATA:
    print(f'Processing {dataset["id"]}')
    # Dataset name is data_file before the first dot
    dataset_filename = f"{dataset['file_prefix']}.predictions.csv"
    data_file_path = os.path.join(RAW_PREDICTIONS_DIR, dataset_filename)
    pheno_file_path = os.path.join(PHENOTYPES_DIR,
                                   f"{dataset['file_prefix']}.pheno.csv")

    # Check if path exists
    if not os.path.exists(data_file_path):
        print(f'File not found: {data_file_path}')
        continue

    if not os.path.exists(pheno_file_path):
        print(f'File not found: {pheno_file_path}')
        continue

    adp = AllsortsDataPreprocessor(data_file_path,
                                   dataset['label'],
                                   subtypes_to_exclude=subtypes_to_exclude,
                                   pheno_file_path=pheno_file_path)
    dataframes.append(adp.df)

# Merge the dataframes
merged_df = pd.concat(dataframes)

# Drop all rows where known_class is empty string
merged_df = merged_df[merged_df['known_class'] != '']

# Drop all rows where known_class begins with "UNRECOGNIZED"
merged_df = merged_df[~merged_df['known_class'].str.startswith('UNRECOGNIZED')]

# Remove the T-ALL subtype from the dataset
merged_df = merged_df[merged_df['known_class'] != 'T-ALL']

# Remove b-others from merged_df
merged_df = merged_df[merged_df['known_class'] != 'B-other']

# Remove all excluded classes
merged_df = merged_df[~merged_df['known_class'].isin(subtypes_to_exclude)]

# Dump all items except empty known class to csv
print('All items with known and recognized subtype:')
print(merged_df)
merged_df.to_csv(FORMATTED_PREDICTIONS_FILE_ALL, index=False)
