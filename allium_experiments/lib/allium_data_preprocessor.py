import pandas as pd
from conformist import PredictionDataset, PredictionDataPreprocessor
from allium_prepro.subtype_thesaurus import SubtypeThesaurus


class AlliumDataPreprocessor(PredictionDataPreprocessor):
    def __init__(self,
                 predictions_csv,
                 dataset_name,
                 id_col=PredictionDataset.ID_COL,
                 predicted_class_col='GEX_subtype_V2',
                 known_class_col='subtype',
                 subtypes_to_exclude=None):

        st = SubtypeThesaurus()
        self.ALLIUM_SUBTYPES = st.allium_subtypes()

        # If subtypes_to_exclude is not None, remove them from self.ALLIUM_SUBTYPES
        if subtypes_to_exclude:
            print(f'Excluding subtypes: {subtypes_to_exclude}...')
            self.ALLIUM_SUBTYPES = [subtype for subtype in self.ALLIUM_SUBTYPES if subtype not in subtypes_to_exclude]

        known_class_df = None
        if known_class_col:
            known_class_df = self._process_known_col(predictions_csv,
                                                     id_col,
                                                     known_class_col)

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
        cols_to_keep = [PredictionDataset.ID_COL] + [col for col in proba_df.columns if col in self.ALLIUM_SUBTYPES]
        proba_df = proba_df[cols_to_keep]

        # Make nans 0
        proba_df.fillna(0, inplace=True)

        # Merge proba_df into self.df
        self.df = pd.merge(self.df,
                           proba_df,
                           on=PredictionDataset.ID_COL)

    def _process_known_col(self,
                           predictions_csv, id_col, known_class_col):
        data = pd.read_csv(predictions_csv)
        known_class_df = data[[id_col, known_class_col]]
        # Rename known_class_col to PredictionDataset.KNOWN_CLASS_COL
        known_class_df = known_class_df.rename(
            columns={known_class_col: PredictionDataset.KNOWN_CLASS_COL})

        def _process_unknown_subtypes(x):
            subtypes = []
            for subtype in x.split(','):
                # If subtype starts with "UNRECOGNIZED", continue
                if subtype.startswith('UNRECOGNIZED'):
                    continue
                # If subtype not in ALLIUM_SUBTYPES, continue
                if subtype not in self.ALLIUM_SUBTYPES:
                    continue
                subtypes.append(subtype)
            # If subtypes empty, return ""
            if not subtypes:
                return None
            return ','.join(subtypes)

        # Loop through known_class_df and split known_class_col
        # into known_class and known_subtype
        known_class_df[PredictionDataset.KNOWN_CLASS_COL] = known_class_df[
            PredictionDataset.KNOWN_CLASS_COL].apply(_process_unknown_subtypes)

        return known_class_df

