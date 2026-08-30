-- ============================================================
-- Sales Overview
-- ============================================================
--
-- Business source:
-- valid_sales view
--
-- valid_sales already excludes:
-- - cancelled transactions
-- - negative quantity
-- - zero quantity
-- - negative price
-- - zero price
-- ============================================================


-- Total revenue
SELECT
    ROUND(
        SUM(Revenue),
        2
    ) AS TotalRevenue
FROM valid_sales;


-- Total valid orders
SELECT
    COUNT(
        DISTINCT InvoiceNo
    ) AS TotalOrders
FROM valid_sales;


-- Average Order Value
WITH order_values AS (
    SELECT
        InvoiceNo,
        SUM(Revenue) AS OrderRevenue
    FROM valid_sales
    GROUP BY InvoiceNo
)

SELECT
    ROUND(
        AVG(OrderRevenue),
        2
    ) AS AverageOrderValue
FROM order_values;


-- Monthly revenue
SELECT
    YearMonth,
    ROUND(
        SUM(Revenue),
        2
    ) AS Revenue
FROM valid_sales
GROUP BY YearMonth
ORDER BY YearMonth;