-- ============================================================
-- Time Analysis
-- ============================================================


-- Monthly revenue
SELECT
    YearMonth,

    ROUND(
        SUM(Revenue),
        2
    ) AS Revenue,

    COUNT(
        DISTINCT InvoiceNo
    ) AS Orders

FROM valid_sales

GROUP BY YearMonth

ORDER BY YearMonth;


-- Orders by weekday
SELECT
    DayOfWeek,

    COUNT(
        DISTINCT InvoiceNo
    ) AS Orders

FROM valid_sales

GROUP BY DayOfWeek

ORDER BY
    CASE DayOfWeek
        WHEN 'Monday' THEN 1
        WHEN 'Tuesday' THEN 2
        WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4
        WHEN 'Friday' THEN 5
        WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END;


-- Revenue by weekday
SELECT
    DayOfWeek,

    ROUND(
        SUM(Revenue),
        2
    ) AS Revenue

FROM valid_sales

GROUP BY DayOfWeek

ORDER BY
    CASE DayOfWeek
        WHEN 'Monday' THEN 1
        WHEN 'Tuesday' THEN 2
        WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4
        WHEN 'Friday' THEN 5
        WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END;


-- Orders by hour
SELECT
    Hour,

    COUNT(
        DISTINCT InvoiceNo
    ) AS Orders

FROM valid_sales

GROUP BY Hour

ORDER BY Hour;

WITH monthly_sales AS (
    SELECT
        YearMonth,
        SUM(Revenue) AS Revenue
    FROM valid_sales
    GROUP BY YearMonth
),

with_previous AS (
    SELECT
        YearMonth,
        Revenue,

        LAG(Revenue) OVER (
            ORDER BY YearMonth
        ) AS PreviousMonthRevenue

    FROM monthly_sales
)

SELECT
    YearMonth,

    ROUND(
        Revenue,
        2
    ) AS Revenue,

    ROUND(
        PreviousMonthRevenue,
        2
    ) AS PreviousMonthRevenue,

    ROUND(
        (
            Revenue
            - PreviousMonthRevenue
        )
        / PreviousMonthRevenue
        * 100,
        2
    ) AS GrowthPercent

FROM with_previous

ORDER BY YearMonth;