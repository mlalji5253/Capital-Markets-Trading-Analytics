import pandas as pd
import numpy as np
from pathlib import Path

# -----------------------------
# Configuration
# -----------------------------
np.random.seed(42)
NUM_TRADES = 250000

clients_file = Path("data/raw/clients.csv")
prices_file = Path("data/raw/stock_prices.csv")
output_file = Path("data/raw/trades.csv")

# -----------------------------
# Load Parent Data
# -----------------------------
print("Loading clients and stock prices data...")
try:
    clients_df = pd.read_csv(clients_file)
    prices_df = pd.read_csv(prices_file)
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("Please ensure you have generated clients.csv and stock_prices.csv")
    exit()

client_ids = clients_df['client_id'].values

print(f"Generating {NUM_TRADES:,} realistic trades...")

# -----------------------------
# 1. Sample from Stock Prices
# -----------------------------
# We randomly pick days and companies that actually exist in our prices table
trades_df = prices_df[['company_id', 'trade_date', 'close_price']].sample(n=NUM_TRADES, replace=True).reset_index(drop=True)

# -----------------------------
# 2. Assign Clients and Trade Types
# -----------------------------
trades_df['trade_id'] = range(1, NUM_TRADES + 1)
trades_df['client_id'] = np.random.choice(client_ids, size=NUM_TRADES)
trades_df['trade_type'] = np.random.choice(['BUY', 'SELL'], size=NUM_TRADES, p=[0.6, 0.4]) # Slightly more buys than sells

# -----------------------------
# 3. Calculate Quantities and Prices
# -----------------------------
# Random quantity between 1 and 500 shares
trades_df['quantity'] = np.random.randint(1, 501, size=NUM_TRADES)

# Simulate intraday price (fluctuates slightly around the closing price)
price_fluctuation = np.random.uniform(0.99, 1.01, size=NUM_TRADES)
trades_df['price'] = np.round(trades_df['close_price'] * price_fluctuation, 2)

# Brokerage fee: typically 0.1% of the total trade value, minimum 20 rupees
trade_value = trades_df['quantity'] * trades_df['price']
brokerage = np.round(trade_value * 0.001, 2)
trades_df['brokerage_fee'] = np.clip(brokerage, a_min=20.0, a_max=None)

# -----------------------------
# 4. Generate Trade Datetime
# -----------------------------
# Indian stock market hours are roughly 09:15 to 15:30
# We will add random hours and minutes to the trade_date
random_hours = np.random.randint(9, 15, size=NUM_TRADES)
random_minutes = np.random.randint(15, 60, size=NUM_TRADES)
random_seconds = np.random.randint(0, 60, size=NUM_TRADES)

# Convert trade_date string to datetime, then add the random times
dates = pd.to_datetime(trades_df['trade_date'])
time_deltas = pd.to_timedelta(random_hours, unit='h') + \
              pd.to_timedelta(random_minutes, unit='m') + \
              pd.to_timedelta(random_seconds, unit='s')

trades_df['trade_datetime'] = dates + time_deltas

# -----------------------------
# 5. Clean up and Save
# -----------------------------
# Reorder columns to match our SQL schema
final_trades = trades_df[[
    'trade_id', 'client_id', 'company_id', 'trade_datetime', 
    'trade_type', 'quantity', 'price', 'brokerage_fee'
]]

final_trades.to_csv(output_file, index=False)

print("=" * 50)
print("Trades Dataset Generated Successfully!")
print(f"Total Rows : {len(final_trades):,}")
print(f"Saved to   : {output_file}")
print("=" * 50)