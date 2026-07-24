-- RFM Segmentation
-- Calculates Recency, Frequency, Monetary scores per customer and assigns business-friendly segments

WITH customer_orders AS (
    -- Only count completed orders — refunded/cancelled shouldn't count toward customer value
    SELECT
        customer_id,
        MAX(order_date) AS last_order_date,
        COUNT(*) AS frequency,
        SUM(order_amount) AS monetary
    FROM fact_orders
    WHERE order_status = 'completed'
    GROUP BY customer_id
),

rfm_base AS (
    SELECT
        customer_id,
        last_order_date,
        CAST(julianday('2025-12-31') - julianday(last_order_date) AS INTEGER) AS recency_days,
        frequency,
        monetary
    FROM customer_orders
),

rfm_scored AS (
    SELECT
        customer_id,
        recency_days,
        frequency,
        monetary,
        -- Recency: LOWER days = BETTER, so we reverse the NTILE order (5 = most recent)
        NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
        -- Frequency: HIGHER = BETTER, so 5 = most frequent
        NTILE(5) OVER (ORDER BY frequency ASC) AS f_score,
        -- Monetary: HIGHER = BETTER, so 5 = highest spend
        NTILE(5) OVER (ORDER BY monetary ASC) AS m_score
    FROM rfm_base
)

SELECT
    customer_id,
    recency_days,
    frequency,
    ROUND(monetary, 2) AS monetary,
    r_score,
    f_score,
    m_score,
    (r_score + f_score + m_score) AS rfm_total,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
        WHEN r_score >= 3 AND f_score >= 3 THEN 'Loyal Customers'
        WHEN r_score >= 4 AND f_score <= 2 THEN 'New/Promising'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At Risk'
        WHEN r_score <= 2 AND f_score <= 2 AND m_score <= 2 THEN 'Lost'
        ELSE 'Needs Attention'
    END AS customer_segment
FROM rfm_scored
ORDER BY rfm_total DESC;
