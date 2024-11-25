import pandas as pd
from conformist import PredictionDataset, \
    PredictionDataPreprocessor
from allium_prepro.subtype_thesaurus import SubtypeThesaurus


class AllcatchrDataPreprocessor(PredictionDataPreprocessor):
    def __init__(self,
                 predictions_tsv,
                 dataset_name,
                 pheno_file_path=None,
                 subtypes_to_exclude=None):

        id_col = 'sample'

        st = SubtypeThesaurus()
        self.ALLIUM_SUBTYPES = st.allium_subtypes()

        # If subtypes_to_exclude is not None, remove them from self.ALLIUM_SUBTYPES
        if subtypes_to_exclude:
            print(f'Excluding subtypes: {subtypes_to_exclude}...')
            self.ALLIUM_SUBTYPES = [subtype for subtype in self.ALLIUM_SUBTYPES if subtype not in subtypes_to_exclude]

        if pheno_file_path is not None:
            known_class_df = pd.read_csv(pheno_file_path, sep=';')
            # Rename subtype column to known_class
            known_class_df = known_class_df.rename(columns={'subtype': 'known_class'})

        super().__init__('allcatchr', predictions_tsv,
                         dataset_name, id_col, 'Prediction',
                         known_class_df, '\t')

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
                # Translate class name
                translated_class_name = st.translate(class_name)
                proba_df[translated_class_name] = \
                    (self.df_raw[col] + self.df_raw[nn_col]) / 2

        # Translate all values in predicted class column
        self.df[PredictionDataset.PREDICTED_CLASS_COL] = \
            self.df[PredictionDataset.PREDICTED_CLASS_COL].apply(st.translate)

        # Get all columns beginnign with "UNRECOGNIZED"
        unrecognized_cols = [col for col in proba_df.columns if col.startswith('UNRECOGNIZED')]
        # Print them
        print("Dropping unrecognized columns: ", unrecognized_cols)
        # Drop them
        proba_df = proba_df.drop(columns=unrecognized_cols)

        # Rename id column
        proba_df = proba_df.rename(columns={id_col: PredictionDataset.ID_COL})

        # Merge proba_df into self.df
        self.df = pd.merge(self.df,
                           proba_df,
                           on=PredictionDataset.ID_COL)

