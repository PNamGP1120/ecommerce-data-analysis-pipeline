-- ============================================================
-- Market / Country Analysis
-- ============================================================


-- Revenue by country
SELECT
    Country,
    ROUND(
        SUM(Revenue),
        2
    ) AS Revenue
FROM valid_sales
GROUP BY Country
ORDER BY Revenue DESC;


-- Top international markets
SELECT
    Country,
    ROUND(
        SUM(Revenue),
        2
    ) AS Revenue
FROM valid_sales
WHERE Country != 'United Kingdom'
GROUP BY Country
ORDER BY Revenue DESC
LIMIT 10;


-- UK revenue share
WITH total AS (
    SELECT
        SUM(Revenue) AS TotalRevenue
    FROM valid_sales
),

uk AS (
    SELECT
        SUM(Revenue) AS UKRevenue
    FROM valid_sales
    WHERE Country = 'United Kingdom'
)

SELECT
    ROUND(
        uk.UKRevenue,
        2
    ) AS UKRevenue,

    ROUND(
        total.TotalRevenue,
        2
    ) AS TotalRevenue,

    ROUND(
        uk.UKRevenue
        / total.TotalRevenue
        * 100,
        2
    ) AS UKRevenueSharePercent

FROM uk
CROSS JOIN total;

WITH country_revenue AS (
    SELECT
        Country,
        SUM(Revenue) AS Revenue
    FROM valid_sales
    GROUP BY Country
)

SELECT
    Country,

    ROUND(
        Revenue,
        2
    ) AS Revenue,

    RANK() OVER (
        ORDER BY Revenue DESC
    ) AS RevenueRank,

    ROUND(
        Revenue
        / SUM(Revenue) OVER ()
        * 100,
        2
    ) AS RevenueSharePercent

FROM country_revenue
ORDER BY RevenueRank;
