import pandas as pd
from conformist import PredictionDataset, PredictionDataPreprocessor
from .constants import ALLIUM_SUBTYPES


class AlliumDataPreprocessor(PredictionDataPreprocessor):
    def __init__(self,
                 predictions_csv,
                 dataset_name,
                 id_col=PredictionDataset.ID_COL,
                 predicted_class_col='GEX_subtype_V2',
                 known_class_df=None):

        super().__init__(model_name='allium',
                         predictions_csv=predictions_csv,
                         dataset_name=dataset_name,
                         id_col=id_col,
                         predicted_class_col=predicted_class_col,
                         known_classes_df=known_class_df)

        # Replace 'no_class' in predicted_class with empty string
        self.df[PredictionDataset.PREDICTED_CLASS_COL] = \
            self.df[PredictionDataset.PREDICTED_CLASS_COL].replace(
                'no_class', '')

        # Process all column names that end in ".classifier.proba"
        PREDICTED_PROBA_COL_SUFFIX = '.classifier.proba'

        # In raw df, id column is id_col. In df, it is PredictionDataset.ID_COL
        # Get proba columns from raw df by merging id_col on PredictionDataset.ID_COL
        proba_df = self.df_raw[[id_col] + [
            col for col in self.df_raw.columns if col.endswith(PREDICTED_PROBA_COL_SUFFIX)]]

        # Rename columns to remove ".classifier.proba" suffix
        proba_df.columns = [col.replace(PREDICTED_PROBA_COL_SUFFIX, '') for col in proba_df.columns]

        # Rename id_col to PredictionDataset.ID_COL
        proba_df = proba_df.rename(columns={id_col: PredictionDataset.ID_COL})

        # Retain only columns that are in ALLIUM_SUBTYPES
        cols_to_keep = [PredictionDataset.ID_COL] + [col for col in proba_df.columns if col in ALLIUM_SUBTYPES]
        proba_df = proba_df[cols_to_keep]

        # Make nans 0
        proba_df.fillna(0, inplace=True)

        # Merge proba_df into self.df
        self.df = pd.merge(self.df,
                           proba_df,
                           on=PredictionDataset.ID_COL)
