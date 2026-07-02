import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

np.random.seed(42)
output_file = Path("data/raw/market_indices.csv")

end_date = datetime.today()
start_date = end_date - timedelta(days=3*365)
business_days = pd.bdate_range(start=start_date, end=end_date)

indices = [
    {"name": "NIFTY_50", "start_value": 15000, "volatility": 0.012},
    {"name": "SENSEX", "start_value": 50000, "volatility": 0.011},
    {"name": "BANK_NIFTY", "start_value": 35000, "volatility": 0.015}
]

records = []
index_id = 1

print("Generating 3 years of Market Indices...")

for idx in indices:
    current_value = idx["start_value"]
    
    for date in business_days:
        daily_change_pct = np.random.normal(0.0005, idx["volatility"]) # Slight upward bias
        
        open_val = current_value
        close_val = open_val * (1 + daily_change_pct)
        daily_change_pts = close_val - open_val
        
        records.append({
            "index_id": index_id,
            "index_name": idx["name"],
            "trade_date": date.date(),
            "open_value": round(open_val, 2),
            "close_value": round(close_val, 2),
            "daily_change": round(daily_change_pts, 2)
        })
        
        index_id += 1
        current_value = close_val

df = pd.DataFrame(records)
df.to_csv(output_file, index=False)

print("=" * 50)
print("Market Indices Generated Successfully!")
print(f"Total Rows : {len(df):,}")
print("=" * 50)