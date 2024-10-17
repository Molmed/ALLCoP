import matplotlib.pyplot as plt
import seaborn as sns
from conformist import OutputDir, PredictionDataset


class DualSubtypeHeatmap(OutputDir):
    KNOWN_CLASS_COL = PredictionDataset.KNOWN_CLASS_COL
    KNOWN_PRIMARY_SUBTYPE_COL = f'{KNOWN_CLASS_COL}_1'
    KNOWN_SECONDARY_SUBTYPE_COL = f'{KNOWN_CLASS_COL}_2'

    def __init__(self,
                 prediction_dataset: PredictionDataset,
                 base_output_dir,
                 label_x,
                 label_y):
        self.prediction_dataset = prediction_dataset
        self.df = prediction_dataset.df
        self.label_x = label_x
        self.label_y = label_y
        self.create_output_dir(base_output_dir)

        # Split string in the known class column on comma
        new_cols = [f"{DualSubtypeHeatmap.KNOWN_CLASS_COL}_1",
                    f"{DualSubtypeHeatmap.KNOWN_CLASS_COL}_2"]
        self.df[new_cols] = \
            self.df[DualSubtypeHeatmap.KNOWN_CLASS_COL].str.split(
                ',', expand=True)

    def visualize(self):
        # Convert nans to empty strings
        self.df[DualSubtypeHeatmap.KNOWN_SECONDARY_SUBTYPE_COL] = \
            self.df[
                DualSubtypeHeatmap.KNOWN_SECONDARY_SUBTYPE_COL].fillna('')

        # Get all rows with non-empty secondary subtypes
        df_non_empty_secondary = self.df[
            self.df[
                DualSubtypeHeatmap.KNOWN_SECONDARY_SUBTYPE_COL] != '']

        # Create a new DataFrame with the specified columns
        new_df = df_non_empty_secondary[[
            DualSubtypeHeatmap.KNOWN_PRIMARY_SUBTYPE_COL,
            DualSubtypeHeatmap.KNOWN_SECONDARY_SUBTYPE_COL]].copy()

        # Rename the columns
        new_df.columns = [self.label_y, self.label_x]

        # Translate the values in the columns
        new_df[self.label_y] = new_df[self.label_y].map(
            self.prediction_dataset.translate_class_name)

        new_df[self.label_x] = new_df[self.label_x].map(
            self.prediction_dataset.translate_class_name)


        # Sort the values in each row
        new_df = new_df.apply(lambda row: sorted(row), axis=1, result_type='broadcast')

        # Sort the DataFrame by subtype1 and subtype2
        new_df.sort_values(by=[self.label_y, self.label_x], inplace=True)

        # Add a column for counts
        counts = new_df.groupby([self.label_y, self.label_x]).size()
        new_df['counts'] = new_df.set_index([self.label_y, self.label_x]).index.map(counts.get)

        # Get uniques
        unique_rows_df = new_df.drop_duplicates()

        # Create pivot table
        pivot_table = unique_rows_df.pivot(index=self.label_y, columns=self.label_x, values='counts')

        # Replace NaN values with zeros
        pivot_table.fillna(0, inplace=True)

        # Create a heatmap
        plt.figure()
        g = sns.clustermap(pivot_table, annot=True, cmap='flare',
                           row_cluster=False, col_cluster=True,
                           cbar_pos=None, dendrogram_ratio=(0, 0))

        # Make axis labels bold
        w = 'bold'
        lp = 10
        g.ax_heatmap.set_xlabel(g.ax_heatmap.get_xlabel(),
                                weight=w, labelpad=lp)
        g.ax_heatmap.set_ylabel(g.ax_heatmap.get_ylabel(),
                                weight=w, labelpad=lp)

        plt.savefig(f'{self.output_dir}/dual_subtype_samples.png',
                    bbox_inches='tight')

        print(f'Dual subtype heatmap saved to {self.output_dir}')
