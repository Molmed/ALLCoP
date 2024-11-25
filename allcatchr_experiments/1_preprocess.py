import pandas as pd
import os
from lib.allcatchr_data_preprocessor import AllcatchrDataPreprocessor
from lib.constants import RAW_PREDICTIONS_DIR, \
    FORMATTED_PREDICTIONS_FILE_ALL, \
    DATASET_METADATA, \
    PHENOTYPES_DIR

print('Preprocessing raw predictions...')

subtypes_to_exclude = ['Control', 'NUTM1-r', 'low hyperdiploid']

dataframes = []
for dataset in DATASET_METADATA:
    print(f'Processing {dataset["id"]}')
    # Dataset name is data_file before the first dot
    dataset_filename = f"{dataset['file_prefix']}.predictions.tsv"
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

    adp = AllcatchrDataPreprocessor(data_file_path,
                                    dataset['label'],
                                    subtypes_to_exclude=subtypes_to_exclude,
                                    pheno_file_path=pheno_file_path)
    dataframes.append(adp.df)
exit()

# # Merge the dataframes
# merged_df = pd.concat(dataframes)

# # Report all items where the known_class is empty
# print('Items with empty known_class:')
# print(merged_df[merged_df['known_class'].isnull()])

# # Drop all rows where known_class is empty
# merged_df = merged_df.dropna(subset=['known_class'])

# # Dump all items except empty known class to csv
# print('All items with recognized subtype or B-other:')
# print(merged_df)
# merged_df.to_csv(FORMATTED_PREDICTIONS_FILE_ALL, index=False)

# # Report all the multiclass items, this means known_class will contain comma
# print('Items with multiple known subtypes:')
# multiclass_items = merged_df[merged_df['known_class'].str.contains(',')]
# print(multiclass_items)

# # Save the multiclass items
# multiclass_items.to_csv(FORMATTED_PREDICTIONS_FILE_MULTICLASS,
#                         index=False)

# # Remove multiclass items from merged_df
# merged_df = merged_df[~merged_df['known_class'].str.contains(',')]

# # Report all items where known_class is "B-other"
# print('Items with known_class as B-other:')
# b_others = merged_df[merged_df['known_class'] == 'B-other']
# print(b_others)

# # Save the b_others
# b_others.to_csv(FORMATTED_PREDICTIONS_FILE_B_OTHER,
#                 index=False)

# # Remove b-others from merged_df
# merged_df = merged_df[merged_df['known_class'] != 'B-other']

# # Dump remaining to csv
# print('Items with single known subtype:')
# print(merged_df)
# merged_df.to_csv(FORMATTED_PREDICTIONS_FILE_SINGLECLASS, index=False)
