import pandas as pd
from conformist import OutputDir, PredictionDataset, \
    PredictionDataPreprocessor
from .constants import ALLCATCHR_TO_ALLIUM_SUBTYPE_DICT, \
    ALLIUM_SUBTYPES, EXCLUDE_ALLIUM_SUBTYPES


class AllcatchrDataPreprocessor(PredictionDataPreprocessor):
    def __init__(self,
                 predictions_tsv,
                 dataset_name,
                 id_col,
                 known_class_df=None,
                 csv_delimiter='\t'):

        super().__init__('allcatchr', predictions_tsv,
                         dataset_name, id_col, 'Prediction',
                         known_class_df, csv_delimiter)

        # Process the probabilities
        proba_df = pd.DataFrame()
        proba_df[id_col] = self.df_raw[id_col]

        # For each column starting with 'ML_', take the class name 'ML_' + the substring after 'ML_'
        # Then, find the column NN_ + the substring after 'ML_'
        # Take the mean of these two columns and assign it to the new column called class name
        class_names = []
        for col in self.df_raw.columns:
            if col.startswith('ML_'):
                class_name = col[3:]
                if class_name not in class_names:
                    class_names.append(class_name)
                nn_col = f'NN_{class_name}'
                proba_df[class_name] = \
                    (self.df_raw[col] + self.df_raw[nn_col]) / 2

        # For each column, if the name exists in the dict, rename it accordingly.
        # Otherwise, report it and drop it
        cols_to_rename = {id_col: PredictionDataset.ID_COL}
        cols_to_drop = []
        for col in class_names:
            if col in ALLCATCHR_TO_ALLIUM_SUBTYPE_DICT:
                cols_to_rename[col] = ALLCATCHR_TO_ALLIUM_SUBTYPE_DICT[col]
                print(f"Renaming {col} to {ALLCATCHR_TO_ALLIUM_SUBTYPE_DICT[col]}")
            elif col not in ALLIUM_SUBTYPES or col in EXCLUDE_ALLIUM_SUBTYPES:
                cols_to_drop.append(col)
                print(f"Unrecognized or excluded class: {col}")

        proba_df = proba_df.rename(columns=cols_to_rename)
        proba_df = proba_df.drop(columns=cols_to_drop)

        # Merge proba_df into self.df
        self.df = pd.merge(self.df,
                           proba_df,
                           on=PredictionDataset.ID_COL)

        # Rename all the classes in the predicted class column
        # Use cols_to_rename to rename the values
        self.df[PredictionDataset.PREDICTED_CLASS_COL] = \
            self.df[PredictionDataset.PREDICTED_CLASS_COL].map(cols_to_rename)

        # If we have a known class column, exclude the rows where the known class is in EXCLUDE_ALLIUM_SUBTYPES
        if known_class_df is not None:
            self.df = self.df[~self.df[PredictionDataset.KNOWN_CLASS_COL].isin(EXCLUDE_ALLIUM_SUBTYPES)]
