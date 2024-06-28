import pandas as pd
from conformist import PredictionDataset, PredictionDataPreprocessor
from .constants import ALLSORTS_TO_ALLIUM_SUBTYPE_DICT, \
    ALLIUM_SUBTYPES, EXCLUDE_ALLIUM_SUBTYPES


class AllsortsDataPreprocessor(PredictionDataPreprocessor):
    def __init__(self,
                 predictions_csv,
                 dataset_name,
                 id_col,
                 known_class_df=None):

        super().__init__('allsorts', predictions_csv,
                         dataset_name, id_col, 'Pred', known_class_df)

        # Process the probabilities
        # Save the merged probabilities of 'High hyperdiploid' and 'Low hyperdiploid'
        heh_probas = self.df_raw['High hyperdiploid'] + self.df_raw['Low hyperdiploid']

        # The probability columns start at col 1 and go until the 'Pred' column
        proba_columns = self.df_raw.columns[1:self.df_raw.columns.get_loc('Pred')]

        # Move these into a new df
        proba_df = self.df_raw[[id_col] + [
            col for col in self.df_raw.columns if col in proba_columns]]

        # For each column, if the name exists in the dict, rename it accordingly.
        # Otherwise, report it and drop it
        cols_to_rename = {id_col: PredictionDataset.ID_COL}
        cols_to_drop = ['HeH']
        for col in proba_columns:
            if col in ALLSORTS_TO_ALLIUM_SUBTYPE_DICT:
                cols_to_rename[col] = ALLSORTS_TO_ALLIUM_SUBTYPE_DICT[col]
                print(f"Renaming {col} to {ALLSORTS_TO_ALLIUM_SUBTYPE_DICT[col]}")
            elif col not in ALLIUM_SUBTYPES or col in EXCLUDE_ALLIUM_SUBTYPES:
                cols_to_drop.append(col)
                print(f"Unrecognized or excluded class: {col}")
        proba_df = proba_df.rename(columns=cols_to_rename)
        proba_df = proba_df.drop(columns=cols_to_drop)
        proba_df['HeH'] = heh_probas

        # Merge proba_df into self.df
        self.df = pd.merge(self.df,
                           proba_df,
                           on=PredictionDataset.ID_COL)

        # Rename all the classes in the predicted class column
        # Multiple values are supported, so we have to map them one by one

        def map_classes(x):
            classes = []
            for i in x:
                if i == 'Unclassified':
                    return ''
                classes.append(ALLSORTS_TO_ALLIUM_SUBTYPE_DICT.get(i, i))
            return ','.join(classes)

        # For each row, split the predicted class by ',' and map each value
        self.df[PredictionDataset.PREDICTED_CLASS_COL] = \
            self.df[PredictionDataset.PREDICTED_CLASS_COL].str.split(',').map(
                lambda x: map_classes(x))

        # If we have a known class column, exclude the rows where the known class is in EXCLUDE_ALLIUM_SUBTYPES
        if known_class_df is not None:
            self.df = self.df[~self.df[PredictionDataset.KNOWN_CLASS_COL].isin(EXCLUDE_ALLIUM_SUBTYPES)]
