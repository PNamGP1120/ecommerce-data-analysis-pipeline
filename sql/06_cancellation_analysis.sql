-- ============================================================
-- Cancellation Analysis
-- ============================================================


-- Cancellation documents
SELECT
    COUNT(
        DISTINCT InvoiceNo
    ) AS CancelledInvoices
FROM cancellations;


-- Invoice-document cancellation share
WITH all_invoices AS (
    SELECT
        COUNT(
            DISTINCT InvoiceNo
        ) AS TotalInvoices
    FROM transactions
),

cancelled_invoices AS (
    SELECT
        COUNT(
            DISTINCT InvoiceNo
        ) AS CancelledInvoices
    FROM cancellations
)

SELECT
    cancelled_invoices.CancelledInvoices,

    all_invoices.TotalInvoices,

    ROUND(
        100.0
        * cancelled_invoices.CancelledInvoices
        / all_invoices.TotalInvoices,
        2
    ) AS CancellationSharePercent

FROM all_invoices
CROSS JOIN cancelled_invoices;


-- Top cancelled products
SELECT
    StockCode,
    Description,

    SUM(
        ABS(Quantity)
    ) AS CancelledQuantity

FROM cancellations

GROUP BY
    StockCode,
    Description

ORDER BY CancelledQuantity DESC

LIMIT 10;


-- Cancellation value
SELECT
    ROUND(
        SUM(
            ABS(Revenue)
        ),
        2
    ) AS CancellationValue
FROM cancellations;