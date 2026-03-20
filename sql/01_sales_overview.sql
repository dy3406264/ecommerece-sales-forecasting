-- ============================================================
-- 01_sales_overview.sql
-- Project : E-Commerce Sales & Revenue Forecasting
-- Desc    : High-level KPIs and revenue trends
-- ============================================================

-- ── 1. Overall KPIs ──────────────────────────────────────────
SELECT
    COUNT(DISTINCT order_id)    AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(DISTINCT product_id)  AS total_products,
    ROUND(SUM(sales), 2)        AS total_revenue,
    ROUND(SUM(profit), 2)       AS total_profit,
    ROUND(AVG(sales), 2)        AS avg_order_value,
    ROUND(AVG(profit / NULLIF(sales, 0)) * 100, 2) AS avg_profit_margin_pct
FROM superstore;

-- ── 2. Yearly Revenue & Profit ───────────────────────────────
SELECT
    strftime('%Y', order_date)    AS year,
    ROUND(SUM(sales), 2)          AS revenue,
    ROUND(SUM(profit), 2)         AS profit,
    ROUND(SUM(profit)/SUM(sales)*100, 2) AS profit_margin_pct,
    COUNT(DISTINCT order_id)      AS total_orders
FROM superstore
GROUP BY year
ORDER BY year;

-- ── 3. Monthly Revenue (for trend analysis) ──────────────────
SELECT
    strftime('%Y-%m', order_date) AS year_month,
    ROUND(SUM(sales), 2)          AS monthly_revenue,
    ROUND(SUM(profit), 2)         AS monthly_profit,
    COUNT(DISTINCT order_id)      AS orders
FROM superstore
GROUP BY year_month
ORDER BY year_month;

-- ── 4. Quarter-over-Quarter Growth ───────────────────────────
SELECT
    strftime('%Y', order_date) AS year,
    CAST(((strftime('%m', order_date) - 1) / 3) + 1 AS TEXT) AS quarter,
    ROUND(SUM(sales), 2)       AS quarterly_revenue,
    COUNT(DISTINCT order_id)   AS orders
FROM superstore
GROUP BY year, quarter
ORDER BY year, quarter;

-- ── 5. Revenue by Ship Mode ──────────────────────────────────
SELECT
    ship_mode,
    COUNT(DISTINCT order_id)   AS total_orders,
    ROUND(SUM(sales), 2)       AS total_revenue,
    ROUND(AVG(sales), 2)       AS avg_order_value,
    ROUND(SUM(profit), 2)      AS total_profit
FROM superstore
GROUP BY ship_mode
ORDER BY total_revenue DESC;
