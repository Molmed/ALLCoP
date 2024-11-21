import pandas as pd
import os
from lib.allium_data_preprocessor import AlliumDataPreprocessor
from lib.constants import RAW_PREDICTIONS_DIR, \
    FORMATTED_PREDICTIONS_FILE, \
    FORMATTED_PREDICTIONS_FILE_B_OTHER, \
    FORMATTED_PREDICTIONS_FILE_MULTICLASS, \
    FORMATTED_PREDICTIONS_FILE_ALL, \
    DATASET_METADATA

print('Preprocessing raw predictions...')

subtypes_to_exclude = ['Control', 'NUTM1-r', 'low hyperdiploid']

dataframes = []
for dataset in DATASET_METADATA:
    print(f'Processing {dataset}')
    # Dataset name is data_file before the first dot
    dataset_filename = f"{dataset['file_prefix']}.predictions.csv"
    data_file_path = os.path.join(RAW_PREDICTIONS_DIR, dataset_filename)
    adp = AlliumDataPreprocessor(data_file_path,
                                 dataset['label'],
                                 subtypes_to_exclude=subtypes_to_exclude)
    dataframes.append(adp.df)

# Merge the dataframes
merged_df = pd.concat(dataframes)

# Report all items where the known_class is empty
print('Items with empty known_class:')
print(merged_df[merged_df['known_class'].isnull()])

# Drop all rows where known_class is empty
merged_df = merged_df.dropna(subset=['known_class'])

# Dump all items except empty known class to csv
print('All items with recognized subtype or B-other:')
print(merged_df)
merged_df.to_csv(FORMATTED_PREDICTIONS_FILE_ALL, index=False)

# Report all the multiclass items, this means known_class will contain comma
print('Items with multiple known subtypes:')
multiclass_items = merged_df[merged_df['known_class'].str.contains(',')]
print(multiclass_items)

# Save the multiclass items
multiclass_items.to_csv(FORMATTED_PREDICTIONS_FILE_MULTICLASS,
                        index=False)

# Remove multiclass items from merged_df
merged_df = merged_df[~merged_df['known_class'].str.contains(',')]

# Report all items where known_class is "B-other"
print('Items with known_class as B-other:')
b_others = merged_df[merged_df['known_class'] == 'B-other']
print(b_others)

# Save the b_others
b_others.to_csv(FORMATTED_PREDICTIONS_FILE_B_OTHER,
                index=False)

# Remove b-others from merged_df
merged_df = merged_df[merged_df['known_class'] != 'B-other']

# Dump remaining to csv
print('Items with single known subtype:')
print(merged_df)
merged_df.to_csv(FORMATTED_PREDICTIONS_FILE, index=False)
