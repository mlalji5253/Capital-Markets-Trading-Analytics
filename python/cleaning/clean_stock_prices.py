from cleaner import DataCleaner

cleaner = (
    DataCleaner(
        "data/raw/stock_prices.csv",
        "data/cleaned/stock_prices.csv"
    )
    .load()
    .remove_duplicates()

    .validate_dates([
        "trade_date"
    ])

    .validate_range(
        "open_price",
        minimum=1
    )

    .validate_range(
        "high_price",
        minimum=1
    )

    .validate_range(
        "low_price",
        minimum=1
    )

    .validate_range(
        "close_price",
        minimum=1
    )

    .validate_range(
        "volume",
        minimum=0
    )

    .save()
)

cleaner.generate_report()

print("Stock prices cleaned successfully.")