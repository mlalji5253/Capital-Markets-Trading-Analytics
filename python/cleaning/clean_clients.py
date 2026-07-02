from cleaner import DataCleaner

cleaner = (
    DataCleaner(
        "data/raw/clients.csv",
        "data/cleaned/clients.csv"
    )
    .load()
    .remove_duplicates()
    .remove_duplicate_keys("client_id")
    .trim_whitespace()
    .standardize_text()

    .validate_dates([
        "date_of_birth",
        "account_open_date"
    ])

    .validate_allowed_values(
        "gender",
        ["Male", "Female"]
    )

    .validate_allowed_values(
        "risk_profile",
        ["Low", "Medium", "High"]
    )

    .validate_range(
        "annual_income",
        minimum=0
    )

    .fill_missing_numeric()
    .fill_missing_text()

    .save()
)

cleaner.generate_report()

print("Clients cleaned successfully.")