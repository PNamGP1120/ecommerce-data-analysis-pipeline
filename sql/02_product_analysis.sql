-- ============================================================
-- Product Analysis
-- ============================================================


-- Top products by revenue
SELECT
    StockCode,
    Description,
    ROUND(
        SUM(Revenue),
        2
    ) AS Revenue
FROM valid_sales
GROUP BY
    StockCode,
    Description
ORDER BY Revenue DESC
LIMIT 10;


-- Top products by quantity
SELECT
    StockCode,
    Description,
    SUM(Quantity) AS Quantity
FROM valid_sales
GROUP BY
    StockCode,
    Description
ORDER BY Quantity DESC
LIMIT 10;


-- Product performance with both revenue and quantity
SELECT
    StockCode,
    Description,
    SUM(Quantity) AS Quantity,
    ROUND(
        SUM(Revenue),
        2
    ) AS Revenue,
    COUNT(
        DISTINCT InvoiceNo
    ) AS OrderCount
FROM valid_sales
GROUP BY
    StockCode,
    Description
HAVING SUM(Quantity) > 0
ORDER BY Revenue DESC
LIMIT 20;