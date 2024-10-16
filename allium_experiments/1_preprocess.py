import pandas as pd
import os
from lib.allium_data_preprocessor import AlliumDataPreprocessor

# Grab all files in the data directory
# Get current script dir
script_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(script_dir, 'data')
raw_predictions_dir = os.path.join(data_dir, 'raw_predictions')


raw_data_files = os.listdir(raw_predictions_dir)
dataframes = []
for data_file in raw_data_files:
    # Dataset name is data_file before the first dot
    dataset_name = data_file.split('.')[0]
    data_file_path = os.path.join(raw_predictions_dir, data_file)
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
b_others.to_csv(os.path.join(data_dir, 'formatted_predictions_b_other.csv'),
                index=False)

# Remove b-others from merged_df
merged_df = merged_df[merged_df['known_class'] != 'B-other']

# Dump to csv
merged_df.to_csv(
    os.path.join(data_dir, 'formatted_predictions.csv'), index=False)
