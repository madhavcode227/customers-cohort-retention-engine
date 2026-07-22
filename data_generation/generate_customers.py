import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()
random.seed(42)
np.random.seed(42)

NUM_CUSTOMERS = 3000
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 31)

CHANNELS = ["paid_search", "organic", "email", "social", "referral", "direct"]
CHANNEL_WEIGHTS = [0.30, 0.20, 0.10, 0.20, 0.10, 0.10]

def random_signup_date():
    days_range = (END_DATE - START_DATE).days
    return START_DATE + timedelta(days=random.randint(0, days_range))

customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    customers.append({
        "customer_id": i,
        "customer_name": fake.name(),
        "email": fake.email(),
        "signup_date": random_signup_date().date(),
        "acquisition_channel": np.random.choice(CHANNELS, p=CHANNEL_WEIGHTS),
        "country": fake.country()
    })

df = pd.DataFrame(customers)

missing_idx = df.sample(frac=0.02, random_state=42).index
df.loc[missing_idx, "acquisition_channel"] = None

dupes = df.sample(frac=0.03, random_state=1).copy()
df = pd.concat([df, dupes], ignore_index=True)

df.to_csv("raw_customers.csv", index=False)
print(f"Generated {len(df)} customer rows (including duplicates/nulls).")
print(df.head())
