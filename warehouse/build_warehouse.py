import pandas as pd
import sqlite3

customers = pd.read_csv("../data_generation/raw_customers.csv", parse_dates=["signup_date"])
orders = pd.read_csv("../data_generation/raw_orders.csv", parse_dates=["order_date"])

print(f"Raw customers loaded: {len(customers)} rows")
print(f"Raw orders loaded: {len(orders)} rows")

customers_clean = customers.drop_duplicates(subset=["customer_id"], keep="first").copy()
print(f"After removing duplicate customers: {len(customers_clean)} rows")

customers_clean["acquisition_channel"] = customers_clean["acquisition_channel"].fillna("unknown")
print(f"Customers with 'unknown' channel: {(customers_clean['acquisition_channel'] == 'unknown').sum()}")

conn = sqlite3.connect("ecommerce_warehouse.db")

dim_customers = customers_clean[[
    "customer_id", "customer_name", "email", "signup_date",
    "acquisition_channel", "country"
]]
dim_customers.to_sql("dim_customers", conn, if_exists="replace", index=False)

fact_orders = orders[[
    "order_id", "customer_id", "order_date", "order_status",
    "payment_method", "order_amount"
]]
fact_orders.to_sql("fact_orders", conn, if_exists="replace", index=False)

conn.close()

print(f"\nWarehouse built: ecommerce_warehouse.db")
print(f"dim_customers: {len(dim_customers)} rows")
print(f"fact_orders: {len(fact_orders)} rows")
