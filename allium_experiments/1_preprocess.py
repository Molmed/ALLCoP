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

print(merged_df)

# Dump to csv
merged_df.to_csv(
    os.path.join(data_dir, 'formatted_predictions.csv'), index=False)
