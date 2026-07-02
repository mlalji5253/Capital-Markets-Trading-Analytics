from pathlib import Path
import pandas as pd

# -----------------------------
# Paths
# -----------------------------

INPUT_PATH = Path("data/cleaned")
OUTPUT_PATH = Path("data/processed")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

# =====================================================
# CLIENTS
# =====================================================

clients = pd.read_csv(INPUT_PATH / "clients.csv")

clients["date_of_birth"] = pd.to_datetime(clients["date_of_birth"])

today = pd.Timestamp.today()

clients["age"] = ((today - clients["date_of_birth"]).dt.days // 365)

clients["income_bracket"] = pd.cut(
    clients["annual_income"],
    bins=[0, 500000, 1000000, 5000000, float("inf")],
    labels=[
        "Low",
        "Middle",
        "Upper Middle",
        "High"
    ]
)

clients.to_csv(
    OUTPUT_PATH / "clients.csv",
    index=False
)

print("✓ Clients Feature Engineering Completed")

# =====================================================
# COMPANIES
# =====================================================

companies = pd.read_csv(INPUT_PATH / "companies.csv")

companies["market_cap_category"] = pd.cut(
    companies["market_cap_billion"],
    bins=[0, 10, 50, float("inf")],
    labels=[
        "Small Cap",
        "Mid Cap",
        "Large Cap"
    ]
)

companies.to_csv(
    OUTPUT_PATH / "companies.csv",
    index=False
)

print("✓ Companies Feature Engineering Completed")

# =====================================================
# STOCK PRICES
# =====================================================

prices = pd.read_csv(INPUT_PATH / "stock_prices.csv")

prices["price_change"] = (
    prices["close_price"] -
    prices["open_price"]
)

prices["daily_return_pct"] = (
    prices["price_change"] /
    prices["open_price"]
) * 100

prices.to_csv(
    OUTPUT_PATH / "stock_prices.csv",
    index=False
)

print("✓ Stock Prices Feature Engineering Completed")

# =====================================================
# TRADES
# =====================================================

trades = pd.read_csv(INPUT_PATH / "trades.csv")

trades["trade_datetime"] = pd.to_datetime(
    trades["trade_datetime"]
)

trades["trade_value"] = (
    trades["quantity"] *
    trades["price"]
)

trades["net_amount"] = (
    trades["trade_value"] +
    trades["brokerage_fee"]
)

trades["trade_year"] = (
    trades["trade_datetime"].dt.year
)

trades["trade_month"] = (
    trades["trade_datetime"].dt.month_name()
)

trades["trade_day"] = (
    trades["trade_datetime"].dt.day_name()
)

trades.to_csv(
    OUTPUT_PATH / "trades.csv",
    index=False
)

print("✓ Trades Feature Engineering Completed")

# =====================================================
# MARKET INDICES
# =====================================================

indices = pd.read_csv(INPUT_PATH / "market_indices.csv")

indices["daily_return_pct"] = (
    (
        indices["close_value"] -
        indices["open_value"]
    ) /
    indices["open_value"]
) * 100

indices.to_csv(
    OUTPUT_PATH / "market_indices.csv",
    index=False
)

print("✓ Market Indices Feature Engineering Completed")

print("\n========================================")
print("Feature Engineering Completed Successfully")
print("========================================")