import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from faker import Faker

# -----------------------------
# Configuration
# -----------------------------
fake = Faker("en_IN")
random.seed(42)
Faker.seed(42)

NUM_CLIENTS = 10000

# -----------------------------
# Indian States & Cities
# -----------------------------
locations = {
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
    "Karnataka": ["Bengaluru", "Mysuru", "Hubli"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai"],
    "Delhi": ["New Delhi"],
    "West Bengal": ["Kolkata"],
    "Rajasthan": ["Jaipur", "Udaipur"],
    "Uttar Pradesh": ["Lucknow", "Noida", "Kanpur"],
    "Telangana": ["Hyderabad"],
    "Madhya Pradesh": ["Indore", "Bhopal"]
}

risk_profiles = ["Low", "Medium", "High"]

records = []

for client_id in range(1, NUM_CLIENTS + 1):

    state = random.choice(list(locations.keys()))
    city = random.choice(locations[state])

    age = random.randint(21, 70)

    dob = datetime.today() - timedelta(days=age * 365 + random.randint(0, 365))

    account_open = fake.date_between(
        start_date="-10y",
        end_date="today"
    )

    annual_income = random.randint(300000, 5000000)

    risk = random.choices(
        risk_profiles,
        weights=[40, 40, 20],
        k=1
    )[0]

    gender = random.choice(["Male", "Female"])

    records.append({
        "client_id": client_id,
        "first_name": fake.first_name_male() if gender == "Male" else fake.first_name_female(),
        "last_name": fake.last_name(),
        "gender": gender,
        "date_of_birth": dob.date(),
        "city": city,
        "state": state,
        "country": "India",
        "annual_income": annual_income,
        "risk_profile": risk,
        "account_open_date": account_open
    })

df = pd.DataFrame(records)

# Create folder if not exists
output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "clients.csv"

df.to_csv(output_file, index=False)

print("=" * 50)
print("Clients Dataset Generated Successfully!")
print(f"Rows : {len(df)}")
print(f"Saved : {output_file}")
print("=" * 50)