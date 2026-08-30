-- ============================================================
-- Customer Analysis
-- ============================================================


-- Top customers by spending
SELECT
    CustomerID,
    ROUND(
        SUM(Revenue),
        2
    ) AS Revenue
FROM customer_sales
GROUP BY CustomerID
ORDER BY Revenue DESC
LIMIT 10;


-- Top customers by unique orders
SELECT
    CustomerID,
    COUNT(
        DISTINCT InvoiceNo
    ) AS OrderCount
FROM customer_sales
GROUP BY CustomerID
ORDER BY OrderCount DESC
LIMIT 10;


-- Average revenue per customer
WITH customer_revenue AS (
    SELECT
        CustomerID,
        SUM(Revenue) AS Revenue
    FROM customer_sales
    GROUP BY CustomerID
)

SELECT
    ROUND(
        AVG(Revenue),
        2
    ) AS AverageRevenuePerCustomer
FROM customer_revenue;


-- Customer ranking by revenue
WITH customer_metrics AS (
    SELECT
        CustomerID,
        COUNT(
            DISTINCT InvoiceNo
        ) AS OrderCount,
        SUM(Revenue) AS Revenue
    FROM customer_sales
    GROUP BY CustomerID
)

SELECT
    CustomerID,
    OrderCount,
    ROUND(
        Revenue,
        2
    ) AS Revenue,

    RANK() OVER (
        ORDER BY Revenue DESC
    ) AS RevenueRank

FROM customer_metrics
ORDER BY RevenueRank
LIMIT 20;


WITH customer_revenue AS (
    SELECT
        CustomerID,
        SUM(Revenue) AS Revenue
    FROM customer_sales
    GROUP BY CustomerID
),

ranked AS (
    SELECT
        CustomerID,
        Revenue,

        SUM(Revenue) OVER () AS TotalRevenue,

        RANK() OVER (
            ORDER BY Revenue DESC
        ) AS RevenueRank

    FROM customer_revenue
)

SELECT
    CustomerID,

    ROUND(
        Revenue,
        2
    ) AS Revenue,

    ROUND(
        Revenue
        / TotalRevenue
        * 100,
        2
    ) AS RevenueSharePercent,

    RevenueRank

FROM ranked
ORDER BY RevenueRank
LIMIT 20;