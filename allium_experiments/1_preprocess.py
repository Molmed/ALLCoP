import pandas as pd
import os
from lib.allium_data_preprocessor import AlliumDataPreprocessor
from lib.constants import RAW_PREDICTIONS_DIR, \
    FORMATTED_PREDICTIONS_FILE, \
    FORMATTED_PREDICTIONS_FILE_B_OTHER


raw_data_files = [
    f for f in os.listdir(RAW_PREDICTIONS_DIR) if f.endswith('.csv')]
dataframes = []
for data_file in raw_data_files:
    print(f'Processing {data_file}')
    # Dataset name is data_file before the first dot
    dataset_name = data_file.split('.')[0]
    data_file_path = os.path.join(RAW_PREDICTIONS_DIR, data_file)
    adp = AlliumDataPreprocessor(data_file_path,
                                 dataset_name)
    dataframes.append(adp.df)

# Merge the dataframes
merged_df = pd.concat(dataframes)

# Report all items where the known_class is empty
print('Items with empty known_class:')
print(merged_df[merged_df['known_class'].isnull()])

# Drop all rows where known_class is empty
merged_df = merged_df.dropna(subset=['known_class'])

# Report all items where known_class is "B-other"
print('Items with known_class as B-other:')
b_others = merged_df[merged_df['known_class'] == 'B-other']
print(b_others)

# Save the b_others
b_others.to_csv(FORMATTED_PREDICTIONS_FILE_B_OTHER,
                index=False)

# Remove b-others from merged_df
merged_df = merged_df[merged_df['known_class'] != 'B-other']

# Dump to csv
merged_df.to_csv(FORMATTED_PREDICTIONS_FILE, index=False)
