import pandas as pd
import re
from .constants import ALLIUM_SUBTYPES, JUDE_TO_ALLIUM_SUBTYPE_DICT, \
    KNOWN_CLASSES_COL, KNOWN_PRIMARY_CLASS_COL, KNOWN_SECONDARY_CLASS_COL
from conformist import OutputDir, PredictionDataset


class JudePhenotypeParser(OutputDir):
    # Definitions
    SUBTYPE_PRIMARY = 1
    SUBTYPE_SECONDARY = 2
    SUBTYPE_LEVEL_DELIMITER = ','

    def __init__(self, jude_sample_info_tsv,
                 base_output_dir='output', include_unknowns=False):
        self.jude_sample_info_tsv = jude_sample_info_tsv
        self.create_output_dir(base_output_dir)
        self.output_file = 'output.tsv'
        self.output_path = f'{self.output_dir}/{self.output_file}'

        # Track unknown subtypes
        self.include_unknowns = include_unknowns
        self.unknown_primary_subtypes = {}
        self.unknown_secondary_subtypes = {}

        # Keep the underlying dataframe
        self.df = None

        # Parse
        self.parse()

    @staticmethod
    def split_attr_diagnosis(s):
        # Define the regular expression pattern
        pattern = r'Lineage:(.*?),Primary_subtype:(.*?)(?:,Secondary_subtype:(.*))?$'

        # Use re.match() to apply the pattern
        match = re.match(pattern, s)

        # Extract the groups from the match object
        lineage = match.group(1)
        primary_subtype = match.group(2)
        secondary_subtype = match.group(3) \
            if match.group(3) is not None else ''

        return lineage, primary_subtype, secondary_subtype

    def alliumify_subtype(self, s, level=SUBTYPE_PRIMARY):
        # Strip trailing ?s
        s = s.rstrip('?')
        if s in ALLIUM_SUBTYPES:
            return s
        if s == 'B-other' and self.include_unknowns:
            return s
        if s in JUDE_TO_ALLIUM_SUBTYPE_DICT:
            return JUDE_TO_ALLIUM_SUBTYPE_DICT[s]
        else:
            if level == JudePhenotypeParser.SUBTYPE_PRIMARY:
                self.unknown_primary_subtypes[s] = \
                    self.unknown_primary_subtypes.get(s, 0) + 1
            elif level == JudePhenotypeParser.SUBTYPE_SECONDARY and s != '':
                self.unknown_secondary_subtypes[s] = \
                    self.unknown_secondary_subtypes.get(s, 0) + 1
            return ""

    def parse(self):
        df = pd.read_csv(self.jude_sample_info_tsv, delimiter='\t')

        # Drop AML cases
        df = df[df['attr_diagnosis'] != 'AML']

        # Drop unnecessary columns
        df = df[['sample_name', 'attr_diagnosis']]

        # Rename sample_name to id
        df = df.rename(columns={'sample_name': 'id'})

        for index, row in df.iterrows():
            lineage, primary_subtype, secondary_subtype = \
                JudePhenotypeParser.split_attr_diagnosis(row['attr_diagnosis'])

            # ALLIUM only has one T-ALL subtype
            if lineage == 'T':
                primary_subtype = 'T-ALL'

            # Standardize to ALLIUM conventions
            primary_subtype = self.alliumify_subtype(
                primary_subtype, level=self.SUBTYPE_PRIMARY)
            secondary_subtype = self.alliumify_subtype(
                secondary_subtype, level=self.SUBTYPE_SECONDARY)

            # If the primary subtype is unknown, drop the entire row
            # But if only the secondary subtype is unknown, keep the row
            if primary_subtype == '':
                df = df.drop(index)
                continue

            final_subtype = primary_subtype
            if secondary_subtype != '':
                # Sort primary_subtype and secondary_subtype
                # alphabetically and join them
                final_subtype = self.SUBTYPE_LEVEL_DELIMITER.join(sorted([
                    primary_subtype, secondary_subtype]))

            df.at[index, KNOWN_PRIMARY_CLASS_COL] = primary_subtype
            df.at[index, KNOWN_SECONDARY_CLASS_COL] = secondary_subtype
            df.at[index, KNOWN_CLASSES_COL] = final_subtype

        # Rename column for better readability
        df = df.rename(columns={'attr_diagnosis': 'jude_diagnosis'})

        # Store the df
        self.df = df

        # Save summary
        self.save_summary()

        self.df.to_csv(self.output_path, sep='\t', index=False)

        # Save just id and known_class
        self.df = self.df[[PredictionDataset.ID_COL, KNOWN_CLASSES_COL]]

    def save_summary(self):
        with open(f'{self.output_dir}/summary.txt', 'w') as f:
            f.write("Unknown primary subtypes: %s\n" %
                    self.unknown_primary_subtypes)
            f.write("Total cases with unknown primary subtypes: %d\n" %
                    sum(self.unknown_primary_subtypes.values()))
            f.write("Unknown secondary subtypes: %s\n" %
                    self.unknown_secondary_subtypes)
            f.write("Total cases with unknown secondary subtypes: %d\n" %
                    sum(self.unknown_secondary_subtypes.values()))
            f.write("Number of cases remaining: %d\n" % self.df.shape[0])

            # List the members of allium_subtypes that
            # do not appear in the 'primary_subtype' column
            unmatched_subtypes = set(ALLIUM_SUBTYPES) - \
                set(self.df[KNOWN_PRIMARY_CLASS_COL].unique())
            f.write("ALLIUM subtypes that do not appear in the data: %s\n" %
                    list(unmatched_subtypes))

    def print_summary(self):
        with open(f'{self.output_dir}/summary.txt', 'r') as f:
            print(f.read())
