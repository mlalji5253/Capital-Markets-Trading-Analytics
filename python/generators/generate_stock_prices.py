import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import numpy as np

# -----------------------------
# Configuration
# -----------------------------
np.random.seed(42)
random.seed(42)

input_file = Path("data/raw/companies.csv")
output_dir = Path("data/raw")
output_file = output_dir / "stock_prices.csv"

# -----------------------------
# Load Companies
# -----------------------------
print("Loading companies...")
try:
    companies_df = pd.read_csv(input_file)
except FileNotFoundError:
    print(f"Error: Could not find {input_file}. Did you run generate_companies.py?")
    exit()

# -----------------------------
# Date Range Setup
# -----------------------------
# 3 years of data ending today
end_date = datetime.today()
start_date = end_date - timedelta(days=3*365)
# Generate business days only (Monday-Friday)
business_days = pd.bdate_range(start=start_date, end=end_date)

records = []
price_id = 1

print(f"Generating 3 years of daily stock prices for {len(companies_df)} companies...")
print("This might take 10 to 20 seconds. Please wait...")

# -----------------------------
# Generate Prices
# -----------------------------
for _, row in companies_df.iterrows():
    company_id = row['company_id']
    
    # Set a random starting price based on typical Indian market stocks
    current_price = np.random.uniform(50.0, 3000.0)
    
    # Each stock gets a random daily volatility factor (how crazy the price swings)
    stock_volatility = np.random.uniform(0.01, 0.03)

    for date in business_days:
        # Simulate daily market movement (Random Walk)
        daily_change = np.random.normal(0, stock_volatility)
        
        open_price = current_price
        close_price = open_price * (1 + daily_change)
        
        # Calculate daily high and low
        daily_high = max(open_price, close_price) * (1 + np.random.uniform(0, 0.01))
        daily_low = min(open_price, close_price) * (1 - np.random.uniform(0, 0.01))
        
        # Ensure prices don't drop below 1
        close_price = max(1.0, close_price)
        daily_low = max(1.0, daily_low)
        
        # Generate random volume
        volume = int(np.random.uniform(10000, 5000000))
        
        records.append({
            "price_id": price_id,
            "company_id": company_id,
            "trade_date": date.date(),
            "open_price": round(open_price, 2),
            "high_price": round(daily_high, 2),
            "low_price": round(daily_low, 2),
            "close_price": round(close_price, 2),
            "volume": volume
        })
        
        price_id += 1
        current_price = close_price # Next day's open is based on today's close

# -----------------------------
# Save to CSV
# -----------------------------
df = pd.DataFrame(records)
df.to_csv(output_file, index=False)

print("=" * 50)
print("Stock Prices Dataset Generated Successfully!")
print(f"Total Rows : {len(df):,}")
print(f"Saved to   : {output_file}")
print("=" * 50)