from __future__ import annotations

import pandas as pd


def calculate_total_revenue(
    sales: pd.DataFrame,
) -> float:
    """
    Calculate total revenue from valid sales.
    """
    return float(
        sales["Revenue"].sum()
    )


def calculate_total_orders(
    sales: pd.DataFrame,
) -> int:
    """
    Count unique invoices.

    One invoice represents one order.
    """
    return int(
        sales["InvoiceNo"].nunique()
    )


def calculate_average_order_value(
    sales: pd.DataFrame,
) -> float:
    """
    Calculate Average Order Value (AOV).

    Revenue is first aggregated at invoice level,
    then averaged across invoices.
    """
    if sales.empty:
        return 0.0

    order_values = (
        sales.groupby("InvoiceNo")["Revenue"]
        .sum()
    )

    if order_values.empty:
        return 0.0

    return float(
        order_values.mean()
    )


def calculate_monthly_revenue(
    sales: pd.DataFrame,
) -> pd.DataFrame:
    """
    Aggregate revenue by YearMonth.
    """
    return (
        sales.groupby(
            "YearMonth",
            as_index=False,
        )["Revenue"]
        .sum()
        .sort_values("YearMonth")
        .reset_index(drop=True)
    )


def top_products_by_revenue(
    sales: pd.DataFrame,
    n: int = 10,
) -> pd.DataFrame:
    """
    Return top products ranked by total revenue.
    """
    return (
        sales.groupby(
            [
                "StockCode",
                "Description",
            ],
            as_index=False,
        )["Revenue"]
        .sum()
        .sort_values(
            "Revenue",
            ascending=False,
        )
        .head(n)
        .reset_index(drop=True)
    )


def top_products_by_quantity(
    sales: pd.DataFrame,
    n: int = 10,
) -> pd.DataFrame:
    """
    Return top products ranked by total quantity sold.
    """
    return (
        sales.groupby(
            [
                "StockCode",
                "Description",
            ],
            as_index=False,
        )["Quantity"]
        .sum()
        .sort_values(
            "Quantity",
            ascending=False,
        )
        .head(n)
        .reset_index(drop=True)
    )


def revenue_by_country(
    sales: pd.DataFrame,
) -> pd.DataFrame:
    """
    Aggregate revenue by country.
    """
    return (
        sales.groupby(
            "Country",
            as_index=False,
        )["Revenue"]
        .sum()
        .sort_values(
            "Revenue",
            ascending=False,
        )
        .reset_index(drop=True)
    )


def top_customers_by_spending(
    customer_sales: pd.DataFrame,
    n: int = 10,
) -> pd.DataFrame:
    """
    Return customers ranked by total spending.
    """
    return (
        customer_sales.groupby(
            "CustomerID",
            as_index=False,
        )["Revenue"]
        .sum()
        .sort_values(
            "Revenue",
            ascending=False,
        )
        .head(n)
        .reset_index(drop=True)
    )


def top_customers_by_orders(
    customer_sales: pd.DataFrame,
    n: int = 10,
) -> pd.DataFrame:
    """
    Return customers ranked by number of unique orders.
    """
    return (
        customer_sales.groupby(
            "CustomerID",
            as_index=False,
        )
        .agg(
            OrderCount=(
                "InvoiceNo",
                "nunique",
            )
        )
        .sort_values(
            "OrderCount",
            ascending=False,
        )
        .head(n)
        .reset_index(drop=True)
    )


def average_revenue_per_customer(
    customer_sales: pd.DataFrame,
) -> float:
    """
    Calculate average total revenue generated per customer.
    """
    if customer_sales.empty:
        return 0.0

    customer_revenue = (
        customer_sales.groupby(
            "CustomerID"
        )["Revenue"]
        .sum()
    )

    if customer_revenue.empty:
        return 0.0

    return float(
        customer_revenue.mean()
    )


def revenue_by_weekday(
    sales: pd.DataFrame,
) -> pd.DataFrame:
    """
    Aggregate revenue by weekday.
    """
    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    result = (
        sales.groupby(
            "DayOfWeek",
            as_index=False,
        )["Revenue"]
        .sum()
    )

    result["DayOfWeek"] = pd.Categorical(
        result["DayOfWeek"],
        categories=weekday_order,
        ordered=True,
    )

    return (
        result.sort_values("DayOfWeek")
        .reset_index(drop=True)
    )


def orders_by_weekday(
    sales: pd.DataFrame,
) -> pd.DataFrame:
    """
    Count unique orders by weekday.
    """
    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    result = (
        sales.groupby(
            "DayOfWeek",
            as_index=False,
        )
        .agg(
            Orders=(
                "InvoiceNo",
                "nunique",
            )
        )
    )

    result["DayOfWeek"] = pd.Categorical(
        result["DayOfWeek"],
        categories=weekday_order,
        ordered=True,
    )

    return (
        result.sort_values("DayOfWeek")
        .reset_index(drop=True)
    )


def orders_by_hour(
    sales: pd.DataFrame,
) -> pd.DataFrame:
    """
    Count unique orders by hour.
    """
    return (
        sales.groupby(
            "Hour",
            as_index=False,
        )
        .agg(
            Orders=(
                "InvoiceNo",
                "nunique",
            )
        )
        .sort_values("Hour")
        .reset_index(drop=True)
    )


def calculate_cancellation_rate(
    all_transactions: pd.DataFrame,
    cancellations: pd.DataFrame,
) -> float:
    """
    Calculate invoice-level cancellation share.

    This metric represents:
        unique cancellation documents
        /
        unique invoice documents

    It is not equivalent to the percentage of original
    customer orders that were fully cancelled.
    """
    total_invoices = int(
        all_transactions[
            "InvoiceNo"
        ].nunique()
    )

    if total_invoices == 0:
        return 0.0

    cancelled_invoices = int(
        cancellations[
            "InvoiceNo"
        ].nunique()
    )

    return float(
        cancelled_invoices
        / total_invoices
    )


def top_cancelled_products(
    cancellations: pd.DataFrame,
    n: int = 10,
) -> pd.DataFrame:
    """
    Return products most frequently appearing in cancellations.
    """
    if cancellations.empty:
        return pd.DataFrame(
            columns=[
                "StockCode",
                "Description",
                "CancelledQuantity",
            ]
        )

    result = cancellations.copy()

    result["CancelledQuantity"] = (
        result["Quantity"].abs()
    )

    return (
        result.groupby(
            [
                "StockCode",
                "Description",
            ],
            as_index=False,
        )["CancelledQuantity"]
        .sum()
        .sort_values(
            "CancelledQuantity",
            ascending=False,
        )
        .head(n)
        .reset_index(drop=True)
    )


# ============================================================
# Business Investigation
# ============================================================


def investigate_special_stock_codes(
    sales: pd.DataFrame,
) -> pd.DataFrame:
    """
    Find StockCodes that do not match the common merchandise
    pattern: five digits optionally followed by one letter.

    Examples may include postage, manual adjustments,
    administrative records, etc.
    """
    mask = ~sales["StockCode"].str.match(
        r"^\d{5}[A-Z]?$",
        na=False,
    )

    special = sales.loc[
        mask,
        [
            "StockCode",
            "Description",
            "Quantity",
            "Revenue",
        ],
    ]

    if special.empty:
        return pd.DataFrame(
            columns=[
                "StockCode",
                "Description",
                "Quantity",
                "Revenue",
            ]
        )

    return (
        special.groupby(
            [
                "StockCode",
                "Description",
            ],
            as_index=False,
        )
        .agg(
            Quantity=(
                "Quantity",
                "sum",
            ),
            Revenue=(
                "Revenue",
                "sum",
            ),
        )
        .sort_values(
            "Revenue",
            ascending=False,
        )
        .reset_index(drop=True)
    )


def investigate_quantity_outliers(
    sales: pd.DataFrame,
    n: int = 20,
) -> pd.DataFrame:
    """
    Return transaction lines with the largest quantities.
    """
    columns = [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "UnitPrice",
        "Revenue",
        "CustomerID",
        "Country",
        "InvoiceDate",
    ]

    return (
        sales.nlargest(
            n,
            "Quantity",
        )[columns]
        .reset_index(drop=True)
        .copy()
    )


def investigate_revenue_outliers(
    sales: pd.DataFrame,
    n: int = 20,
) -> pd.DataFrame:
    """
    Return transaction lines with the largest line-level revenue.
    """
    columns = [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "UnitPrice",
        "Revenue",
        "CustomerID",
        "Country",
        "InvoiceDate",
    ]

    return (
        sales.nlargest(
            n,
            "Revenue",
        )[columns]
        .reset_index(drop=True)
        .copy()
    )


def calculate_country_revenue_share(
    sales: pd.DataFrame,
    country: str,
) -> float:
    """
    Calculate the proportion of total revenue generated
    by a specific country.
    """
    total_revenue = float(
        sales["Revenue"].sum()
    )

    if total_revenue == 0:
        return 0.0

    country_revenue = float(
        sales.loc[
            sales["Country"] == country,
            "Revenue",
        ].sum()
    )

    return float(
        country_revenue
        / total_revenue
    )


def top_international_markets(
    sales: pd.DataFrame,
    exclude_country: str = "United Kingdom",
    n: int = 10,
) -> pd.DataFrame:
    """
    Rank markets by revenue after excluding
    the domestic market.
    """
    international = sales.loc[
        sales["Country"] != exclude_country
    ]

    return (
        international.groupby(
            "Country",
            as_index=False,
        )["Revenue"]
        .sum()
        .sort_values(
            "Revenue",
            ascending=False,
        )
        .head(n)
        .reset_index(drop=True)
    )


def calculate_duplicate_sensitivity(
    sales: pd.DataFrame,
) -> pd.DataFrame:
    """
    Compare total revenue with and without rows belonging
    to duplicate groups.

    Important:
    This is a sensitivity analysis only.

    IsDuplicate uses keep=False, therefore removing these rows
    removes every row belonging to a duplicate group, including
    the first occurrence.
    """
    revenue_with_duplicates = float(
        sales["Revenue"].sum()
    )

    if "IsDuplicate" not in sales.columns:
        raise ValueError(
            "IsDuplicate column is required "
            "for duplicate sensitivity analysis."
        )

    without_duplicate_groups = sales.loc[
        ~sales["IsDuplicate"]
    ]

    revenue_without_duplicates = float(
        without_duplicate_groups[
            "Revenue"
        ].sum()
    )

    revenue_difference = (
        revenue_with_duplicates
        - revenue_without_duplicates
    )

    difference_percent = (
        revenue_difference
        / revenue_with_duplicates
        if revenue_with_duplicates != 0
        else 0.0
    )

    return pd.DataFrame(
        {
            "metric": [
                "revenue_with_duplicate_groups",
                "revenue_without_duplicate_groups",
                "revenue_difference",
                "difference_percent",
            ],
            "value": [
                revenue_with_duplicates,
                revenue_without_duplicates,
                revenue_difference,
                difference_percent,
            ],
        }
    )


def investigate_business_data(
    sales: pd.DataFrame,
) -> dict[str, object]:
    """
    Run business-focused investigations before finalizing
    product and KPI definitions.
    """
    return {
        "special_stock_codes": (
            investigate_special_stock_codes(
                sales
            )
        ),
        "quantity_outliers": (
            investigate_quantity_outliers(
                sales
            )
        ),
        "revenue_outliers": (
            investigate_revenue_outliers(
                sales
            )
        ),
        "uk_revenue_share": (
            calculate_country_revenue_share(
                sales,
                "United Kingdom",
            )
        ),
        "international_markets": (
            top_international_markets(
                sales
            )
        ),
        "duplicate_sensitivity": (
            calculate_duplicate_sensitivity(
                sales
            )
        ),
    }

def calculate_monthly_growth(
    sales: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate monthly revenue and month-over-month growth.
    """
    result = calculate_monthly_revenue(
        sales
    ).copy()

    result["PreviousMonthRevenue"] = (
        result["Revenue"].shift(1)
    )

    result["GrowthPercent"] = (
        result["Revenue"]
        .pct_change(fill_method=None)
        * 100
    )

    return result