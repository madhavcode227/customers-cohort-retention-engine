# Customer Cohort Retention & LTV Engine

**A growth-analytics project answering one question: which acquisition channels bring loyal, high-value customers — and which bring one-time buyers?**

🔗 **[Live Interactive Dashboard →](https://madhavcode227.github.io/customers-cohort-retention-engine/dashboard/dashboard.html)**

## The Business Problem

The Head of Growth wants to reallocate marketing budget toward acquisition channels that drive long-term customer value, not just signup volume. This project builds the full analytics pipeline — from raw data to an executive dashboard — to answer that question with data.

## Key Finding

**Organic customers have a lifetime value of $333 — 3.8x higher than paid_search customers ($87).** Critically, average order value is nearly identical across every channel (~$62–67). The entire LTV gap comes from **purchase frequency**, not spend per transaction: organic customers order 5.3x on average, while paid_search customers order 1.3x. Paid search still drives the highest total channel revenue due to volume, so the recommendation isn't to cut it — it's to pair paid acquisition with retention campaigns while shifting incremental budget toward organic/referral growth.

## Tech Stack

- **Python** (`pandas`, `numpy`, `faker`) — synthetic data generation with realistic, engineered retention patterns
- **SQL** (SQLite) — CTEs, window functions (`NTILE`, aggregate windows), date arithmetic for cohort analysis
- **SQLite** — data warehouse using a star schema (dimension + fact tables)
- **HTML/CSS/JS (Chart.js)** — interactive dashboard, hosted via GitHub Pages

## Project Structure
## Pipeline Overview

**1. Data Generation** — Synthetic e-commerce data (3,000 customers, ~8,900 orders across 24 months) with deliberately engineered realism: organic/referral customers repeat-purchase far more than paid_search/social customers, order amounts follow a realistic (non-uniform) distribution, and ~3% duplicate records / ~2% missing channel data simulate real CRM export messiness.

**2. ETL & Warehouse** — `build_warehouse.py` deduplicates customers, explicitly labels missing channel data as `unknown` (rather than dropping rows), and loads clean data into a SQLite star schema: `dim_customers` and `fact_orders`. Rerunning this script rebuilds the warehouse from raw data — the foundation for an automated refresh.

**3. RFM Segmentation** — Every customer scored on Recency, Frequency, and Monetary value using `NTILE(5)` window functions, then grouped into six segments (Champions, Loyal Customers, At Risk, Lost, etc.) for the growth team to act on directly.

**4. Cohort Retention Analysis** — Customers grouped into monthly cohorts by first purchase date; tracks what % of each cohort returns in each subsequent month, using manual month-difference date math (SQLite has no built-in month-diff function).

**5. LTV by Channel** — Combines order frequency and average order value per channel to isolate *why* LTV differs between channels, not just *that* it differs.

**6. Dashboard** — Interactive HTML dashboard (Chart.js) presenting all three analyses for a non-technical stakeholder, hosted live via GitHub Pages.

## Running This Project

```bash
# 1. Set up environment
python3 -m venv venv
source venv/bin/activate
pip install faker pandas numpy

# 2. Generate raw data
cd data_generation
python3 generate_customers.py
python3 generate_orders.py

# 3. Build the warehouse
cd ../warehouse
python3 build_warehouse.py

# 4. Run analyses
cd ../sql
sqlite3 ../warehouse/ecommerce_warehouse.db < rfm_segmentation.sql
sqlite3 ../warehouse/ecommerce_warehouse.db < cohort_retention.sql
sqlite3 ../warehouse/ecommerce_warehouse.db < ltv_by_channel.sql
```

## Design Decisions Worth Noting

- **Synthetic data over a public dataset:** chosen deliberately so retention behavior could be engineered to reflect a real, known pattern (paid acquisition → lower loyalty), giving the analysis a genuine finding to surface rather than arbitrary numbers.
- **Kept messiness in raw data, cleaned it explicitly downstream:** duplicates and missing values are injected at generation time and handled visibly in the ETL step — mirroring how real pipelines work, rather than starting from artificially perfect data.
- **`unknown` label instead of dropping missing data:** dropping rows with missing acquisition_channel would silently bias channel-level metrics; explicit labeling preserves the record and makes the gap visible.
- **SQLite instead of Postgres/Snowflake:** all SQL here (CTEs, window functions, `NTILE`) is standard and portable — the same queries would run unchanged against Postgres or Snowflake in a production setting.

## Author

Madhav Kapoor
