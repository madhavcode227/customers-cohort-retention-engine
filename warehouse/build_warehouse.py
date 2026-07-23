import pandas as pd
import sqlite3

# Load raw data generated in Day 1 & Day 2
customers = pd.read_csv("../data_generation/raw_customers.csv", parse_dates=["signup_date"])
orders = pd.read_csv("../data_generation/raw_orders.csv", parse_dates=["order_date"])

print(f"Raw customers loaded: {len(customers)} rows")
print(f"Raw orders loaded: {len(orders)} rows")

# --- CLEANING STEP 1: Remove duplicate customers ---
# We intentionally injected ~3% duplicates in Day 1 to simulate a messy CRM export.
# Keep the FIRST occurrence of each customer_id (arbitrary but consistent rule).
# .copy() ensures we get a truly independent DataFrame, not a view into the original
# (avoids the SettingWithCopyWarning when we modify it below).
customers_clean = customers.drop_duplicates(subset=["customer_id"], keep="first").copy()
print(f"After removing duplicate customers: {len(customers_clean)} rows")

# --- CLEANING STEP 2: Handle missing acquisition_channel ---
# Rather than silently dropping these customers (losing data) or guessing,
# we explicitly label them — this preserves the record and makes the gap visible in analysis.
customers_clean["acquisition_channel"] = customers_clean["acquisition_channel"].fillna("unknown")
print(f"Customers with 'unknown' channel: {(customers_clean['acquisition_channel'] == 'unknown').sum()}")

# --- LOAD STEP: Create SQLite warehouse and write dimension + fact tables ---
conn = sqlite3.connect("ecommerce_warehouse.db")

# dim_customers: one row per real customer, cleaned and deduplicated
dim_customers = customers_clean[[
    "customer_id", "customer_name", "email", "signup_date",
    "acquisition_channel", "country"
]]
dim_customers.to_sql("dim_customers", conn, if_exists="replace", index=False)

# fact_orders: one row per order, linked to dim_customers via customer_id
fact_orders = orders[[
    "order_id", "customer_id", "order_date", "order_status", "payment_method"
]]
fact_orders.to_sql("fact_orders", conn, if_exists="replace", index=False)

conn.close()

print(f"\nWarehouse built: ecommerce_warehouse.db")
print(f"dim_customers: {len(dim_customers)} rows")
print(f"fact_orders: {len(fact_orders)} rows")
