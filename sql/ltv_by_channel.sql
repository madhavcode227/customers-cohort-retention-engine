-- LTV by Acquisition Channel
-- Calculates average customer lifetime value, order frequency, and average order value per channel

WITH customer_ltv AS (
    SELECT
        c.customer_id,
        c.acquisition_channel,
        COUNT(f.order_id) AS total_orders,
        SUM(f.order_amount) AS lifetime_value
    FROM dim_customers c
    LEFT JOIN fact_orders f
        ON c.customer_id = f.customer_id
        AND f.order_status = 'completed'
    GROUP BY c.customer_id, c.acquisition_channel
)

SELECT
    acquisition_channel,
    COUNT(customer_id) AS num_customers,
    ROUND(AVG(total_orders), 2) AS avg_orders_per_customer,
    ROUND(AVG(lifetime_value), 2) AS avg_ltv,
    ROUND(SUM(lifetime_value), 2) AS total_channel_revenue,
    ROUND(AVG(lifetime_value) / NULLIF(AVG(total_orders), 0), 2) AS avg_order_value
FROM customer_ltv
GROUP BY acquisition_channel
ORDER BY avg_ltv DESC;
