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
        self.output_dir = None
        self._base_output_dir = base_output_dir
        self._calibration_dataset = calibration_dataset
        self._prediction_dataset = prediction_dataset
        self._alphas = alphas

    def merge_prediction_sets(self, formatted_prediction_dict):
        if not self.output_dir:
            self.create_output_dir(self._base_output_dir)

        prediction_set_cols = []
        softmax_score_cols = []
        # For each dataset, rename 'prediction_sets' to 'prediction_sets a={alpha}'
        # And 'prediction_set_softmax_scores' to 'prediction_set_softmax_scores a={alpha}'
        # Then add the new dataset to a list

        # Sort formatted prediction dict by alpha decreasing
        formatted_prediction_dict = dict(
            sorted(formatted_prediction_dict.items(),
                   key=lambda item: item[0], reverse=True))

        datasets = []
        for alpha, formatted_predictions in formatted_prediction_dict.items():
            ps_col = f'prediction_sets a={alpha}'
            ss_col = f'prediction_set_softmax_scores a={alpha}'
            formatted_predictions = formatted_predictions.rename(columns={
                'prediction_sets': ps_col,
                'prediction_set_softmax_scores': ss_col
            })
            prediction_set_cols.append(ps_col)
            softmax_score_cols.append(ss_col)
            datasets.append(formatted_predictions)

        # Join all datasets on id
        merged = datasets[0]
        for i in range(1, len(datasets)):
            merged = merged.merge(datasets[i], on='id', how='left')

        # Columns to keep
        cols = (['dataset',
                'id',
                'known_class',
                'predicted_class']
                + prediction_set_cols
                + ['known_class_softmax_scores']
                + softmax_score_cols)

        # Keep only the columns in cols
        merged = merged[cols]

        # Rename predicted class to 'model_predicted_class'
        merged = merged.rename(columns={'predicted_class': 'model_predicted_class'})

        # Fill NaN with empty string
        merged = merged.fillna('')

        # Gather statistics
        stats = {}

        # How many rows in total?
        stats['total_num_samples'] = merged.shape[0]

        # Model contains correct class in how many cases?
        # Loop through rows, for each row, break up known_class into a list
        # and check if model_predicted_class is in that list
        stats['model_contains_correct_class'] = merged.apply(
            lambda row:
            row['model_predicted_class'] in row['known_class'].split(','),
            axis=1
        ).sum()

        # How many empty model predictions?
        stats['model_empty_predictions'] = merged.apply(
            lambda row: len(row['model_predicted_class'].strip()) < 1,
            axis=1
        ).sum()

        stats['model_incorrect_not_empty'] = int(
            stats['total_num_samples']-stats['model_contains_correct_class']-stats['model_empty_predictions'])

        # How many incorrect or empty?
        stats['model_incorrect_or_empty'] = int(
            stats['total_num_samples']-stats['model_contains_correct_class'])

        # For each alpha, how much was the error reduced?
        # 'prediction_sets a={alpha}' is a comma separate string, so it should be searched
        for alpha in self._alphas:
            stats[f'alpha={alpha}_correct'] = merged.apply(
                lambda row: any(pred_class in row['known_class'].split(',') for pred_class in row[f'prediction_sets a={alpha}'].split(',')),
                axis=1
            ).sum()

            stats[f'alpha={alpha}_empty'] = merged.apply(
                lambda row: len(row[f'prediction_sets a={alpha}'].strip()) < 1,
                axis=1
            ).sum()

            # Get empty in %
            stats[f'alpha={alpha}_empty_%'] = stats[f'alpha={alpha}_empty'] / stats['total_num_samples']

            # How many sets contain single subtype?
            stats[f'alpha={alpha}_single_subtype'] = merged.apply(
                lambda row: len(
                    row[f'prediction_sets a={alpha}'].strip()) > 0 and len(
                        row[f'prediction_sets a={alpha}'].split(',')) == 1,
                axis=1
            ).sum()

            # Get this in percent
            stats[f'alpha={alpha}_single_subtype_%'] = stats[f'alpha={alpha}_single_subtype'] / stats['total_num_samples']

            # How many contain two or more
            stats[f'alpha={alpha}_two_or_more'] = merged.apply(
                lambda row: len(row[f'prediction_sets a={alpha}'].split(',')) > 1,
                axis=1
            ).sum()

            # Get this in percent
            stats[f'alpha={alpha}_two_or_more_%'] = stats[f'alpha={alpha}_two_or_more'] / stats['total_num_samples']

            # How many incorrect?
            stats[f'alpha={alpha}_incorrect_or_empty'] = stats['total_num_samples'] - stats[f'alpha={alpha}_correct']

            # How many n cases fewer were incorrect?
            stats[f'alpha={alpha}_error_reduction_n'] = stats['model_incorrect_or_empty'] - stats[f'alpha={alpha}_incorrect_or_empty']

            # Mean set size
            stats[f'alpha={alpha}_mean_set_size'] = merged[f'prediction_sets a={alpha}'].apply(
                lambda x: len(x.split(',')) if x else 0).mean()

            # Go through each row. For each row, check f'prediction_sets a={alpha}'
            # Split it by string, if there is more than one class, count the classes in a dict
            # If the known class is in the dict, increment the count
            stats[f'alpha={alpha}_coocurring_classes'] = {}
            stats[f'alpha={alpha}_n_multiple_predictions'] = 0
            for index, row in merged.iterrows():
                pred_set = row[f'prediction_sets a={alpha}'].split(',')
                if len(pred_set) > 1:
                    stats[f'alpha={alpha}_n_multiple_predictions'] += 1
                    for class_ in pred_set:
                        if class_ != row['known_class']:
                            if stats[f'alpha={alpha}_coocurring_classes'].get(class_):
                                stats[f'alpha={alpha}_coocurring_classes'][class_] += 1
                            else:
                                stats[f'alpha={alpha}_coocurring_classes'][class_] = 1

        # Save the stats
        with open(f'{self.output_dir}/prediction_set_comparison_stats.txt', 'w') as f:
            for key, value in stats.items():
                f.write(f'{key}: {value}\n')

        # Save the merged dataset
        merged.to_csv(f'{self.output_dir}/prediction_set_comparison.csv', index=False)

    def merge_stats(self, stats_dict):
        if not self.output_dir:
            self.create_output_dir(self._base_output_dir)

        mean_model_fnrs = None
        allcop_fnrs = {}
        allcop_set_sizes = {}
        general_stats = {}

        for alpha, stats in stats_dict.items():
            mean_model_fnrs = pd.DataFrame.from_dict(
                stats['mean_model_fnrs'],
                orient='index',
                columns=['mean model FNR'])

            allcop_fnrs[alpha] = pd.DataFrame.from_dict(
                stats['mean_fnrs'],
                orient='index',
                columns=[f'mean ALLCoP FNR a={alpha}'])

            allcop_set_sizes[alpha] = pd.DataFrame.from_dict(
                stats['mean_set_sizes'],
                orient='index',
                columns=[f'mean set size a={alpha}'])

            general_stats[alpha] = pd.DataFrame.from_dict(
                stats['general_stats'],
                orient='index',
                columns=[f'a={alpha}'])

        # Sort by mean model FNR
        mean_model_fnrs = mean_model_fnrs.sort_values(by='mean model FNR')

        # Sort allcop_fnrs by alpha decreasing
        allcop_fnrs = dict(
            sorted(allcop_fnrs.items(),
                   key=lambda item: item[0], reverse=True))

        # Sort allcop_set_sizes by alpha decreasing
        allcop_set_sizes = dict(
            sorted(allcop_set_sizes.items(),
                   key=lambda item: item[0], reverse=True))

        all_dfs = [mean_model_fnrs] + list(
            allcop_fnrs.values()) + list(
                allcop_set_sizes.values())
        allcop_fnrs_combined = pd.concat(all_dfs, axis=1)

        # Sort the combined DataFrame by the desired column
        allcop_fnrs_combined = allcop_fnrs_combined.sort_values(by=[f'mean model FNR'])

        # Save the combined DataFrame to a CSV file
        allcop_fnrs_combined.to_csv(
            f'{self.output_dir}/stats_comparison_subtype.csv', mode="w")

        # Now general stats...
        # Sort general_stats by alpha decreasing
        general_stats = dict(
            sorted(general_stats.items(),
                   key=lambda item: item[0], reverse=True))
        # Combine them
        general_stats_combined = pd.concat(list(general_stats.values()), axis=1)

        # Save the combined DataFrame to a CSV file
        general_stats_combined.to_csv(
            f'{self.output_dir}/stats_comparison.csv', mode="w")

    def visualize(self):
        if not self.output_dir:
            self.create_output_dir(self._base_output_dir)

        self.prediction_dataset = self._prediction_dataset
        self.calibration_dataset = self._calibration_dataset
        self.pred_df = self._prediction_dataset.df

        # Get softmax scores columns
        softmax_columns = self.pred_df.columns[self.pred_df.columns.get_loc(
            PredictionDataset.KNOWN_CLASS_COL) + 1:]

        # For each row in vpd.df, get all column names where
        # the value is >= 1-alpha
        softmax_passing_threshold = self.pred_df.copy()
        softmax_passing_threshold['passing_threshold'] = None

        palettes = ["Blues", "YlOrBr", "Greens"]
        # Create plot with three columns and two rows
        fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(21, 21))

        i_plt_row = 0
        for alpha in self._alphas:
            for index, row in softmax_passing_threshold.iterrows():
                cols_pass = []
                for col in softmax_columns:
                    if row[col] >= 1 - alpha:
                        cols_pass.append(col)
                softmax_passing_threshold.at[index, 'passing_threshold'] = ','.join(cols_pass)

            # CALIBRATE CONFORMAL PREDICTOR #
            mcp = FNRCoP(self._calibration_dataset, alpha=alpha)
            mcp.calibrate()

            # Get formatted predictions
            formatted_predictions = mcp.predict(self._prediction_dataset)

            # print(formatted_predictions['known_class'].unique())


            fpd = PredictionDataset(df=formatted_predictions, dataset_name='preds')
            melted = fpd.melt()

            # Merge 'passing_threshold' column with vpd.df
            formatted_predictions = melted.merge(softmax_passing_threshold[['id', 'passing_threshold']],
                                on='id', how='left')


            # Replace NaN with empty string
            formatted_predictions['predicted_class'] = formatted_predictions['predicted_class'].fillna('')


            # Create new df where there is a column for every subtype in allium subtypes
            cols = ['melted_known_class'] + list(softmax_columns) + ['NO PREDICTION']
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

                    for col in list(softmax_columns):
                        new_row[col] = 1 if col in pclasses else 0
                    new_row['melted_known_class'] = row['melted_known_class']
                    return new_row

                df_predicted_class = df_predicted_class._append(get_new_row(predicted_classes), ignore_index=True)
                df_prediction_sets = df_prediction_sets._append(get_new_row(prediction_set), ignore_index=True)
                df_passing_threshold = df_passing_threshold._append(get_new_row(passing_thresh), ignore_index=True)

            def process_df(df):
                # Group by known_class and sum
                df = df.groupby('melted_known_class').sum()

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
            axs[i_plt_row][2].collections[0].colorbar.remove()

            i_plt_row += 1

        plt.tight_layout(h_pad=5)
        plt.savefig(f'{self.output_dir}/comparison.png')

