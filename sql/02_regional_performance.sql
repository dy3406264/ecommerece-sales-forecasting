-- ============================================================
-- 02_regional_performance.sql
-- Project : E-Commerce Sales & Revenue Forecasting
-- Desc    : Sales breakdown by region, state, city
-- ============================================================

-- ── 1. Revenue by Region ─────────────────────────────────────
SELECT
    region,
    ROUND(SUM(sales), 2)          AS total_revenue,
    ROUND(SUM(profit), 2)         AS total_profit,
    ROUND(SUM(profit)/SUM(sales)*100, 2) AS profit_margin_pct,
    COUNT(DISTINCT order_id)      AS total_orders,
    COUNT(DISTINCT customer_id)   AS unique_customers
FROM superstore
GROUP BY region
ORDER BY total_revenue DESC;

-- ── 2. Top 10 States by Revenue ──────────────────────────────
SELECT
    state,
    region,
    ROUND(SUM(sales), 2)   AS total_revenue,
    ROUND(SUM(profit), 2)  AS total_profit,
    COUNT(DISTINCT order_id) AS orders
FROM superstore
GROUP BY state, region
ORDER BY total_revenue DESC
LIMIT 10;

-- ── 3. Bottom 10 States by Profit ────────────────────────────
SELECT
    state,
    region,
    ROUND(SUM(sales), 2)   AS total_revenue,
    ROUND(SUM(profit), 2)  AS total_profit
FROM superstore
GROUP BY state, region
ORDER BY total_profit ASC
LIMIT 10;

-- ── 4. Top 10 Cities by Revenue ──────────────────────────────
SELECT
    city,
    state,
    ROUND(SUM(sales), 2)   AS total_revenue,
    ROUND(SUM(profit), 2)  AS total_profit,
    COUNT(DISTINCT order_id) AS orders
FROM superstore
GROUP BY city, state
ORDER BY total_revenue DESC
LIMIT 10;

-- ── 5. Region × Category Revenue Matrix ──────────────────────
SELECT
    region,
    category,
    ROUND(SUM(sales), 2)          AS revenue,
    ROUND(SUM(profit), 2)         AS profit,
    ROUND(SUM(profit)/SUM(sales)*100, 2) AS margin_pct
FROM superstore
GROUP BY region, category
ORDER BY region, revenue DESC;

-- ── 6. Customer Segment by Region ────────────────────────────
SELECT
    region,
    segment,
    ROUND(SUM(sales), 2)        AS revenue,
    COUNT(DISTINCT customer_id) AS customers
FROM superstore
GROUP BY region, segment
ORDER BY region, revenue DESC;
