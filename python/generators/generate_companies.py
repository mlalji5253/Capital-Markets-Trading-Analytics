import random
from pathlib import Path
import pandas as pd

random.seed(42)

sectors = {
    "Banking": [
        ("HDFCBANK", "HDFC Bank"),
        ("ICICIBANK", "ICICI Bank"),
        ("SBIN", "State Bank of India"),
        ("AXISBANK", "Axis Bank"),
        ("KOTAKBANK", "Kotak Mahindra Bank"),
    ],
    "Information Technology": [
        ("TCS", "Tata Consultancy Services"),
        ("INFY", "Infosys"),
        ("WIPRO", "Wipro"),
        ("HCLTECH", "HCL Technologies"),
        ("TECHM", "Tech Mahindra"),
    ],
    "Automobile": [
        ("MARUTI", "Maruti Suzuki"),
        ("TATAMOTORS", "Tata Motors"),
        ("M&M", "Mahindra & Mahindra"),
        ("BAJAJAUTO", "Bajaj Auto"),
        ("HEROMOTOCO", "Hero MotoCorp"),
    ],
    "Pharmaceuticals": [
        ("SUNPHARMA", "Sun Pharma"),
        ("DRREDDY", "Dr. Reddy's"),
        ("CIPLA", "Cipla"),
        ("LUPIN", "Lupin"),
        ("AUROPHARMA", "Aurobindo Pharma"),
    ],
    "Energy": [
        ("RELIANCE", "Reliance Industries"),
        ("ONGC", "ONGC"),
        ("IOC", "Indian Oil"),
        ("BPCL", "BPCL"),
        ("NTPC", "NTPC"),
    ],
    "FMCG": [
        ("HINDUNILVR", "Hindustan Unilever"),
        ("ITC", "ITC"),
        ("NESTLEIND", "Nestle India"),
        ("DABUR", "Dabur"),
        ("BRITANNIA", "Britannia"),
    ]
}

companies = []

company_id = 1

for sector, values in sectors.items():

    for symbol, company in values:

        companies.append({
            "company_id": company_id,
            "stock_symbol": symbol,
            "company_name": company,
            "sector": sector,
            "market_cap_billion": random.randint(50000, 2500000)
        })

        company_id += 1

df = pd.DataFrame(companies)

output = Path("data/raw")
output.mkdir(parents=True, exist_ok=True)

df.to_csv(output / "companies.csv", index=False)

print(df.head())
print()
print(f"Total Companies : {len(df)}")