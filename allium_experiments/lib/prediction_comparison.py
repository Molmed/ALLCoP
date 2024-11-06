import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.patches as mpatches
from conformist import OutputDir, PredictionDataset, FNRCoP


class PredictionComparison(OutputDir):
    def __init__(self,
                 base_output_dir,
                 calibration_dataset: PredictionDataset,
                 prediction_dataset: PredictionDataset,
                 alphas: list = [0.1, 0.15, 0.2]):
        self.create_output_dir(base_output_dir)

        self.prediction_dataset = prediction_dataset
        self.calibration_dataset = calibration_dataset
        self.pred_df = prediction_dataset.df

        # Get softmax scores columns
        softmax_columns = self.pred_df.columns[self.pred_df.columns.get_loc(
            PredictionDataset.KNOWN_CLASS_COL) + 1:]

        # For each row in vpd.df, get all column names where
        # the value is >= 1-alpha
        softmax_passing_threshold = self.pred_df.copy()
        softmax_passing_threshold['passing_threshold'] = None

        palettes = ["Blues", "YlOrBr", "icefire"]
        # Create plot with three columns and two rows
        fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(21, 21))

        i_plt_row = 0
        for alpha in alphas:
            for index, row in softmax_passing_threshold.iterrows():
                cols_pass = []
                for col in softmax_columns:
                    if row[col] >= 1 - alpha:
                        cols_pass.append(col)
                softmax_passing_threshold.at[index, 'passing_threshold'] = ','.join(cols_pass)

            # CALIBRATE CONFORMAL PREDICTOR #
            mcp = FNRCoP(calibration_dataset, alpha=alpha)
            mcp.calibrate()

            # Get formatted predictions
            formatted_predictions = mcp.predict(prediction_dataset)

            # Merge 'passing_threshold' column with vpd.df
            formatted_predictions = formatted_predictions.merge(softmax_passing_threshold[['id', 'passing_threshold']],
                                on='id', how='left')

            # Replace NaN with empty string
            formatted_predictions['predicted_class'] = formatted_predictions['predicted_class'].fillna('')


            # Create new df where there is a column for every subtype in allium subtypes
            cols = ['known_class'] + softmax_columns + ['NO PREDICTION']
            df_predicted_class = pd.DataFrame(columns=cols)
            df_prediction_sets = pd.DataFrame(columns=cols)
            df_passing_threshold = pd.DataFrame(columns=cols)

            # Loop through formatted predictions and append to df_predicted_class
            for index, row in formatted_predictions.iterrows():
                predicted_classes = row['predicted_class'].split(',')
                prediction_set = row['prediction_sets'].split(',')
                passing_thresh = row['passing_threshold'].split(',')

                def get_new_row(pclasses):
                    new_row = {}

                    if not pclasses or pclasses[0] == '':
                        new_row['NO PREDICTION'] = 1

                    for col in softmax_columns:
                        new_row[col] = 1 if col in pclasses else 0
                    new_row['known_class'] = row['known_class']
                    return new_row

                df_predicted_class = df_predicted_class._append(get_new_row(predicted_classes), ignore_index=True)
                df_prediction_sets = df_prediction_sets._append(get_new_row(prediction_set), ignore_index=True)
                df_passing_threshold = df_passing_threshold._append(get_new_row(passing_thresh), ignore_index=True)

            def process_df(df):
                # Group by known_class and sum
                df = df.groupby('known_class').sum()

                # Sort the rows and columns
                df.sort_index(axis=0, inplace=True)  # Sort rows
                df.sort_index(axis=1, inplace=True)  # Sort columns
                # Put "NO PREDICTION" at the end
                df = df.drop(columns='NO PREDICTION').assign(**{'NO PREDICTION': df['NO PREDICTION']})

                df = df.apply(pd.to_numeric)
                return df

            # Create the first heatmap
            sns.heatmap(process_df(df_predicted_class), annot=True, fmt='g', cmap=palettes[i_plt_row], ax=axs[i_plt_row][0])
            axs[i_plt_row][0].set_title('ALLIUM predicted subtypes', weight='bold')
            # Set y axis
            axs[i_plt_row][0].set_ylabel('TRUE CLASS', weight='bold')
            # Remove color bar
            axs[i_plt_row][0].collections[0].colorbar.remove()


            sns.heatmap(process_df(df_prediction_sets), annot=True, fmt='g', cmap=palettes[i_plt_row], ax=axs[i_plt_row][1])
            axs[i_plt_row][1].set_title(f'ALLCoP prediction sets for ALLIUM, α={alpha}', weight='bold')
            axs[i_plt_row][1].set_ylabel('')
            axs[i_plt_row][1].collections[0].colorbar.remove()

            sns.heatmap(process_df(df_passing_threshold), annot=True, fmt='g', cmap=palettes[i_plt_row], ax=axs[i_plt_row][2])
            axs[i_plt_row][2].set_title(f'ALLIUM softmax >= {1 - alpha}', weight='bold')
            axs[i_plt_row][2].set_ylabel('')

            i_plt_row += 1

        plt.tight_layout(h_pad=5)
        plt.savefig(f'{self.output_dir}/comparison.png')

    def visualize(self):
        pass
