import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

random.seed(42)
np.random.seed(42)

customers = pd.read_csv("raw_customers.csv", parse_dates=["signup_date"])
customers_unique = customers.drop_duplicates(subset=["customer_id"])

END_DATE = datetime(2025, 12, 31)

CHANNEL_ORDER_RANGE = {
    "organic": (2, 10),
    "referral": (2, 9),
    "email": (1, 5),
    "direct": (1, 4),
    "paid_search": (1, 2),
    "social": (1, 2),
}

orders = []
order_id_counter = 1

for _, row in customers_unique.iterrows():
    customer_id = row["customer_id"]
    signup_date = row["signup_date"]
    channel = row["acquisition_channel"]

    if pd.isna(channel) or channel not in CHANNEL_ORDER_RANGE:
        min_o, max_o = (1, 2)
    else:
        min_o, max_o = CHANNEL_ORDER_RANGE[channel]

    num_orders = random.randint(min_o, max_o)

    days_available = (END_DATE - signup_date).days
    if days_available < 1:
        continue

    order_gaps_days = sorted(random.sample(range(1, days_available + 1), min(num_orders, days_available)))

    for gap in order_gaps_days:
        order_date = signup_date + timedelta(days=gap)
        orders.append({
            "order_id": order_id_counter,
            "customer_id": customer_id,
            "order_date": order_date.date(),
            "order_status": np.random.choice(
                ["completed", "refunded", "cancelled"],
                p=[0.90, 0.06, 0.04]
            ),
            "payment_method": np.random.choice(
                ["credit_card", "paypal", "debit_card", "upi"],
                p=[0.45, 0.25, 0.20, 0.10]
            ),
            "order_amount": round(np.random.gamma(shape=2.5, scale=25), 2)
        })
        order_id_counter += 1

orders_df = pd.DataFrame(orders)
orders_df.to_csv("raw_orders.csv", index=False)

print(f"\nGenerated {len(orders_df)} total orders for {orders_df['customer_id'].nunique()} customers")
print(f"Average order amount: ${orders_df['order_amount'].mean():.2f}")
print(orders_df.head(10))
