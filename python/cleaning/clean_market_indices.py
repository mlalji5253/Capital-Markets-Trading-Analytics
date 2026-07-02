from cleaner import DataCleaner

cleaner = (
    DataCleaner(
        input_file="data/raw/market_indices.csv",
        output_file="data/cleaned/market_indices.csv"
    )
    .load()
    .remove_duplicates()
    .trim_whitespace()
    .standardize_text()
    .fill_missing_numeric()
    .remove_negative([
        "open_value",
        "high_value",
        "low_value",
        "close_value",
        "volume"
    ])
    .save()
)

cleaner.generate_report()

print("Market indices cleaned successfully.")