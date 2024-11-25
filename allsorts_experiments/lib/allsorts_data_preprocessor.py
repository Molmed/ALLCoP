import pandas as pd
from conformist import PredictionDataset, PredictionDataPreprocessor
from allium_prepro.subtype_thesaurus import SubtypeThesaurus


class AllsortsDataPreprocessor(PredictionDataPreprocessor):
    def __init__(self,
                 predictions_csv,
                 dataset_name,
                 pheno_file_path=None,
                 subtypes_to_exclude=None):

        id_col = 'id'

        st = SubtypeThesaurus()
        self.ALLIUM_SUBTYPES = st.allium_subtypes()

        # If subtypes_to_exclude is not None, remove them from self.ALLIUM_SUBTYPES
        if subtypes_to_exclude:
            print(f'Excluding subtypes: {subtypes_to_exclude}...')
            self.ALLIUM_SUBTYPES = [subtype for subtype in self.ALLIUM_SUBTYPES if subtype not in subtypes_to_exclude]

        def _process_unknown_subtypes(x):
            if x.startswith('UNRECOGNIZED') or x not in self.ALLIUM_SUBTYPES:
                return ""
            return x

        known_class_df = None
        if pheno_file_path is not None:
            known_class_df = pd.read_csv(pheno_file_path, sep=';')
            # Rename subtype column to known_class
            known_class_df = known_class_df.rename(
                columns={'subtype': PredictionDataset.KNOWN_CLASS_COL})

            # Loop through known_class_df and split known_class_col
            # into known_class and known_subtype
            known_class_df[PredictionDataset.KNOWN_CLASS_COL] = known_class_df[
                PredictionDataset.KNOWN_CLASS_COL].apply(
                    _process_unknown_subtypes)

        super().__init__('allsorts', predictions_csv,
                         dataset_name, id_col, 'Pred', known_class_df)

        # Process the probabilities
        # The probability columns start at col 1 and go until the 'Pred' column
        proba_columns = self.df_raw.columns[1:self.df_raw.columns.get_loc('Pred')]

        # Move these into a new df
        proba_df = self.df_raw[[id_col] + [
            col for col in self.df_raw.columns if col in proba_columns]]

        # For each column, if the name exists in the dict, rename it accordingly.
        # Otherwise, report it and drop it
        cols_to_rename = {id_col: PredictionDataset.ID_COL}
        cols_to_drop = []

        for col in proba_columns.tolist():
            print("Processing column:", col)
            translated_class_name = st.translate(col)

            if translated_class_name in self.ALLIUM_SUBTYPES:
                if translated_class_name != col:
                    cols_to_rename[col] = translated_class_name
                    print(f"Translated {col} to {translated_class_name}")
            else:
                print(f"Dropping unrecognized class: {col}")
                cols_to_drop.append(col)

        proba_df = proba_df.rename(columns=cols_to_rename)
        proba_df = proba_df.drop(columns=cols_to_drop)

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
                classes.append(st.translate(i))
            return ','.join(classes)

        # For each row, split the predicted class by ',' and map each value
        self.df[PredictionDataset.PREDICTED_CLASS_COL] = \
            self.df[PredictionDataset.PREDICTED_CLASS_COL].str.split(',').map(
                lambda x: map_classes(x))
