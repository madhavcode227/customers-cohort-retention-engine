WITH customer_first_order AS (
    SELECT
        customer_id,
        MIN(order_date) AS first_order_date,
        strftime('%Y-%m', MIN(order_date)) AS cohort_month
    FROM fact_orders
    WHERE order_status = 'completed'
    GROUP BY customer_id
),
cohort_size AS (
    SELECT cohort_month, COUNT(*) AS num_customers
    FROM customer_first_order
    GROUP BY cohort_month
),
orders_with_cohort AS (
    SELECT
        f.customer_id,
        c.cohort_month,
        f.order_date,
        (CAST(strftime('%Y', f.order_date) AS INTEGER) - CAST(substr(c.cohort_month, 1, 4) AS INTEGER)) * 12
        + (CAST(strftime('%m', f.order_date) AS INTEGER) - CAST(substr(c.cohort_month, 6, 2) AS INTEGER))
        AS months_since_first_order
    FROM fact_orders f
    JOIN customer_first_order c ON f.customer_id = c.customer_id
    WHERE f.order_status = 'completed'
),
retention_counts AS (
    SELECT
        cohort_month,
        months_since_first_order,
        COUNT(DISTINCT customer_id) AS active_customers
    FROM orders_with_cohort
    GROUP BY cohort_month, months_since_first_order
)
SELECT
    r.cohort_month,
    r.months_since_first_order,
    r.active_customers,
    s.num_customers AS cohort_size,
    ROUND(100.0 * r.active_customers / s.num_customers, 1) AS retention_pct
FROM retention_counts r
JOIN cohort_size s ON r.cohort_month = s.cohort_month
ORDER BY r.cohort_month, r.months_since_first_order;
