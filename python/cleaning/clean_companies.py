from cleaner import DataCleaner

cleaner = (
    DataCleaner(
        "data/raw/companies.csv",
        "data/cleaned/companies.csv"
    )
    .load()
    .remove_duplicates()
    .remove_duplicate_keys("company_id")
    .trim_whitespace()
    .standardize_text()

    .validate_range(
        "market_cap",
        minimum=1
    )

    .fill_missing_numeric()
    .fill_missing_text()

    .save()
)

cleaner.generate_report()

print("Companies cleaned successfully.")