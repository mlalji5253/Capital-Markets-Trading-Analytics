from pathlib import Path
import pandas as pd


class DataCleaner:
    def __init__(self, input_file, output_file):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.df = None
        self.report = {}

    def load(self):
        self.df = pd.read_csv(self.input_file)
        self.report["rows_before"] = len(self.df)
        return self

    def remove_duplicates(self):
        before = len(self.df)
        self.df = self.df.drop_duplicates()
        self.report["duplicates_removed"] = before - len(self.df)
        return self

    def trim_whitespace(self):
        object_cols = self.df.select_dtypes(include="object").columns

        for col in object_cols:
            self.df[col] = self.df[col].astype(str).str.strip()

        return self

    def standardize_text(self):
        object_cols = self.df.select_dtypes(include="object").columns

        for col in object_cols:
            self.df[col] = self.df[col].str.title()

        return self

    def fill_missing_numeric(self):
        numeric_cols = self.df.select_dtypes(include="number").columns

        for col in numeric_cols:
            self.df[col] = self.df[col].fillna(self.df[col].median())

        return self

    def fill_missing_text(self):
        object_cols = self.df.select_dtypes(include="object").columns

        for col in object_cols:
            self.df[col] = self.df[col].fillna("Unknown")

        return self

    def remove_negative(self, columns):

        for col in columns:
            if col in self.df.columns:
                self.df = self.df[self.df[col] >= 0]

        return self

    def save(self):
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        self.report["rows_after"] = len(self.df)

        self.df.to_csv(self.output_file, index=False)

        return self

    def generate_report(self):

        Path("reports").mkdir(exist_ok=True)

        report_file = Path("reports") / f"{self.input_file.stem}_quality_report.txt"

        with open(report_file, "w") as f:

            f.write("=" * 50 + "\n")
            f.write(f"{self.input_file.stem.upper()} DATA QUALITY REPORT\n")
            f.write("=" * 50 + "\n\n")

            for key, value in self.report.items():
                f.write(f"{key}: {value}\n")

        print(f"Report Saved -> {report_file}")

    def validate_dates(self, columns):

    for col in columns:
        if col in self.df.columns:
            self.df[col] = pd.to_datetime(
                self.df[col],
                errors="coerce"
            )

            self.df = self.df.dropna(subset=[col])

    return self

    def validate_allowed_values(self, column, allowed):

    if column in self.df.columns:
        self.df = self.df[
            self.df[column].isin(allowed)
        ]

    return self  

    def validate_range(self, column, minimum=None, maximum=None):

    if column not in self.df.columns:
        return self

    if minimum is not None:
        self.df = self.df[
            self.df[column] >= minimum
        ]

    if maximum is not None:
        self.df = self.df[
            self.df[column] <= maximum
        ]

    return self


    def remove_duplicate_keys(self, column):

    if column in self.df.columns:
        self.df = self.df.drop_duplicates(
            subset=[column]
        )

    return self