import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from pathlib import Path

# -----------------------------
# Database Configuration
# -----------------------------
DB_USER = "root"
DB_PASS = "Password"  # <--- UPDATE THIS
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "capital_markets"

encoded_pass = quote_plus(DB_PASS)
engine_url = f"mysql+pymysql://{DB_USER}:{encoded_pass}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print("Connecting to MySQL Database...")
try:
    engine = create_engine(engine_url)
    print("✅ Connection Successful!\n")
except Exception as e:
    print("❌ Connection Failed.")
    print(e)
    exit()

# -----------------------------
# Setup Output Folder
# -----------------------------
output_dir = Path("images/eda_charts")
output_dir.mkdir(parents=True, exist_ok=True)

print("Running SQL Queries and Generating Charts...\n")

# ============================================================================
# Chart 1: Sector Performance (Trading Volume)
# ============================================================================
print("Generating Sector Performance Chart...")
query_sector = """
    SELECT c.sector, SUM(t.quantity) AS total_volume
    FROM trades t
    JOIN companies c ON t.company_id = c.company_id
    GROUP BY c.sector
    ORDER BY total_volume DESC;
"""
df_sector = pd.read_sql(query_sector, engine)

plt.figure(figsize=(10, 6))
plt.bar(df_sector['sector'], df_sector['total_volume'], color='teal')
plt.title('Total Trading Volume by Sector', fontsize=14, fontweight='bold')
plt.xlabel('Sector', fontsize=12)
plt.ylabel('Total Volume Traded', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / 'sector_performance.png')
plt.close()

# ============================================================================
# Chart 2: Monthly Brokerage Revenue (Time Series)
# ============================================================================
print("Generating Monthly Revenue Trend Chart...")
query_revenue = """
    SELECT DATE_FORMAT(trade_datetime, '%%Y-%%m') AS trade_month, SUM(brokerage_fee) AS revenue
    FROM trades
    GROUP BY trade_month
    ORDER BY trade_month;
"""
df_revenue = pd.read_sql(query_revenue, engine)

plt.figure(figsize=(12, 6))
plt.plot(df_revenue['trade_month'], df_revenue['revenue'], marker='o', linestyle='-', color='darkorange', linewidth=2)
plt.title('Monthly Brokerage Revenue Trend', fontsize=14, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Revenue (INR)', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig(output_dir / 'monthly_revenue.png')
plt.close()

# ============================================================================
# Chart 3: Client Risk Profile Distribution
# ============================================================================
print("Generating Client Risk Profile Chart...")
query_risk = """
    SELECT risk_profile, COUNT(client_id) as client_count
    FROM clients
    GROUP BY risk_profile;
"""
df_risk = pd.read_sql(query_risk, engine)

plt.figure(figsize=(8, 8))
plt.pie(df_risk['client_count'], labels=df_risk['risk_profile'], autopct='%1.1f%%', 
        startangle=140, colors=['#4CAF50', '#FFC107', '#F44336'])
plt.title('Client Portfolio Risk Distribution', fontsize=14, fontweight='bold')
plt.savefig(output_dir / 'risk_distribution.png')
plt.close()

print("=" * 50)
print(f"🎉 EDA Complete! 3 Charts successfully saved in: {output_dir}")
print("=" * 50)