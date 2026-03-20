-- ============================================================
-- 03_product_analysis.sql
-- Project : E-Commerce Sales & Revenue Forecasting
-- Desc    : Product, category, sub-category & discount analysis
-- ============================================================

-- ── 1. Revenue by Category ───────────────────────────────────
SELECT
    category,
    ROUND(SUM(sales), 2)   AS total_revenue,
    ROUND(SUM(profit), 2)  AS total_profit,
    ROUND(SUM(profit)/SUM(sales)*100, 2) AS profit_margin_pct,
    COUNT(DISTINCT product_id) AS products_sold,
    SUM(quantity)          AS units_sold
FROM superstore
GROUP BY category
ORDER BY total_revenue DESC;

-- ── 2. Revenue & Profit by Sub-Category ──────────────────────
SELECT
    sub_category,
    category,
    ROUND(SUM(sales), 2)   AS total_revenue,
    ROUND(SUM(profit), 2)  AS total_profit,
    ROUND(SUM(profit)/SUM(sales)*100, 2) AS profit_margin_pct,
    SUM(quantity)          AS units_sold
FROM superstore
GROUP BY sub_category, category
ORDER BY total_revenue DESC;

-- ── 3. Top 15 Products by Revenue ────────────────────────────
SELECT
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales), 2)   AS total_revenue,
    ROUND(SUM(profit), 2)  AS total_profit,
    SUM(quantity)          AS units_sold
FROM superstore
GROUP BY product_name, category, sub_category
ORDER BY total_revenue DESC
LIMIT 15;

-- ── 4. Top 15 Products by Profit ─────────────────────────────
SELECT
    product_name,
    category,
    sub_category,
    ROUND(SUM(profit), 2)  AS total_profit,
    ROUND(SUM(sales), 2)   AS total_revenue
FROM superstore
GROUP BY product_name, category, sub_category
ORDER BY total_profit DESC
LIMIT 15;

-- ── 5. Loss-Making Products (Negative Profit) ────────────────
SELECT
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales), 2)   AS total_revenue,
    ROUND(SUM(profit), 2)  AS total_profit
FROM superstore
GROUP BY product_name, category, sub_category
HAVING total_profit < 0
ORDER BY total_profit ASC
LIMIT 20;

-- ── 6. Impact of Discount on Profit ──────────────────────────
SELECT
    CASE
        WHEN discount = 0          THEN '0% (No Discount)'
        WHEN discount <= 0.10      THEN '1-10%'
        WHEN discount <= 0.20      THEN '11-20%'
        WHEN discount <= 0.30      THEN '21-30%'
        WHEN discount <= 0.50      THEN '31-50%'
        ELSE 'Above 50%'
    END AS discount_band,
    COUNT(*)                        AS order_count,
    ROUND(SUM(sales), 2)            AS total_revenue,
    ROUND(SUM(profit), 2)           AS total_profit,
    ROUND(AVG(profit), 2)           AS avg_profit_per_order
FROM superstore
GROUP BY discount_band
ORDER BY discount_band;

-- ── 7. Most Returned / Highest Discount Items ────────────────
SELECT
    product_name,
    ROUND(AVG(discount) * 100, 1)  AS avg_discount_pct,
    ROUND(SUM(profit), 2)          AS total_profit,
    COUNT(*)                        AS order_lines
FROM superstore
GROUP BY product_name
HAVING avg_discount_pct > 30
ORDER BY total_profit ASC
LIMIT 15;
