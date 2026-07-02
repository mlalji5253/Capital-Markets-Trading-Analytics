from cleaner import DataCleaner

cleaner = (
    DataCleaner(
        "data/raw/trades.csv",
        "data/cleaned/trades.csv"
    )
    .load()
    .remove_duplicates()

    .validate_dates([
        "trade_date"
    ])

    .validate_allowed_values(
        "trade_type",
        ["BUY", "SELL"]
    )

    .validate_range(
        "quantity",
        minimum=1
    )

    .validate_range(
        "price",
        minimum=1
    )

    .validate_range(
        "brokerage_fee",
        minimum=0
    )

    .save()
)

cleaner.generate_report()

print("Trades cleaned successfully.")