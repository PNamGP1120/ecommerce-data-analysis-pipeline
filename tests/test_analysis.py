import pandas as pd
import pytest

from ecommerce_analysis.analysis import (
    average_revenue_per_customer,
    calculate_average_order_value,
    calculate_cancellation_rate,
    calculate_country_revenue_share,
    calculate_duplicate_sensitivity,
    calculate_monthly_revenue,
    calculate_total_orders,
    calculate_total_revenue,
    investigate_quantity_outliers,
    investigate_special_stock_codes,
    orders_by_hour,
    orders_by_weekday,
    revenue_by_country,
    top_customers_by_orders,
    top_customers_by_spending,
    top_international_markets,
    top_products_by_quantity,
    top_products_by_revenue, calculate_monthly_growth,
)


def test_total_revenue() -> None:
    df = pd.DataFrame(
        {
            "Revenue": [
                10.0,
                20.0,
                30.0,
            ]
        }
    )

    assert (
        calculate_total_revenue(df)
        == 60.0
    )


def test_total_orders_counts_unique_invoices() -> None:
    df = pd.DataFrame(
        {
            "InvoiceNo": [
                "A",
                "A",
                "B",
            ]
        }
    )

    assert (
        calculate_total_orders(df)
        == 2
    )


def test_average_order_value() -> None:
    df = pd.DataFrame(
        {
            "InvoiceNo": [
                "A",
                "A",
                "B",
            ],
            "Revenue": [
                10.0,
                20.0,
                30.0,
            ],
        }
    )

    result = (
        calculate_average_order_value(
            df
        )
    )

    # Invoice A = 30
    # Invoice B = 30
    # AOV = 30
    assert result == 30.0


def test_average_order_value_empty_dataframe() -> None:
    df = pd.DataFrame(
        columns=[
            "InvoiceNo",
            "Revenue",
        ]
    )

    assert (
        calculate_average_order_value(df)
        == 0.0
    )


def test_monthly_revenue() -> None:
    df = pd.DataFrame(
        {
            "YearMonth": [
                "2011-01",
                "2011-01",
                "2011-02",
            ],
            "Revenue": [
                10.0,
                20.0,
                50.0,
            ],
        }
    )

    result = (
        calculate_monthly_revenue(df)
    )

    assert (
        result.loc[
            result["YearMonth"]
            == "2011-01",
            "Revenue",
        ].iloc[0]
        == 30.0
    )

    assert (
        result.loc[
            result["YearMonth"]
            == "2011-02",
            "Revenue",
        ].iloc[0]
        == 50.0
    )


def test_top_products_by_revenue() -> None:
    df = pd.DataFrame(
        {
            "StockCode": [
                "A",
                "A",
                "B",
            ],
            "Description": [
                "Product A",
                "Product A",
                "Product B",
            ],
            "Revenue": [
                10.0,
                20.0,
                50.0,
            ],
        }
    )

    result = top_products_by_revenue(
        df,
        n=1,
    )

    assert (
        result.iloc[0]["StockCode"]
        == "B"
    )

    assert (
        result.iloc[0]["Revenue"]
        == 50.0
    )


def test_top_products_by_quantity() -> None:
    df = pd.DataFrame(
        {
            "StockCode": [
                "A",
                "A",
                "B",
            ],
            "Description": [
                "Product A",
                "Product A",
                "Product B",
            ],
            "Quantity": [
                10,
                20,
                15,
            ],
        }
    )

    result = top_products_by_quantity(
        df,
        n=1,
    )

    assert (
        result.iloc[0]["StockCode"]
        == "A"
    )

    assert (
        result.iloc[0]["Quantity"]
        == 30
    )


def test_revenue_by_country() -> None:
    df = pd.DataFrame(
        {
            "Country": [
                "UK",
                "UK",
                "France",
            ],
            "Revenue": [
                20.0,
                30.0,
                40.0,
            ],
        }
    )

    result = revenue_by_country(df)

    uk_revenue = (
        result.loc[
            result["Country"] == "UK",
            "Revenue",
        ].iloc[0]
    )

    assert uk_revenue == 50.0


def test_top_customers_by_spending() -> None:
    df = pd.DataFrame(
        {
            "CustomerID": [
                1,
                1,
                2,
            ],
            "Revenue": [
                20.0,
                30.0,
                100.0,
            ],
        }
    )

    result = top_customers_by_spending(
        df,
        n=1,
    )

    assert (
        result.iloc[0]["CustomerID"]
        == 2
    )

    assert (
        result.iloc[0]["Revenue"]
        == 100.0
    )


def test_top_customers_by_orders_counts_unique_invoices() -> None:
    df = pd.DataFrame(
        {
            "CustomerID": [
                1,
                1,
                1,
                2,
            ],
            "InvoiceNo": [
                "A",
                "A",
                "B",
                "C",
            ],
        }
    )

    result = top_customers_by_orders(
        df,
        n=2,
    )

    assert (
        result.iloc[0]["CustomerID"]
        == 1
    )

    assert (
        result.iloc[0]["OrderCount"]
        == 2
    )


def test_average_revenue_per_customer() -> None:
    df = pd.DataFrame(
        {
            "CustomerID": [
                1,
                1,
                2,
            ],
            "Revenue": [
                10.0,
                20.0,
                50.0,
            ],
        }
    )

    result = (
        average_revenue_per_customer(
            df
        )
    )

    # Customer 1 = 30
    # Customer 2 = 50
    # Average = 40
    assert result == 40.0


def test_orders_by_weekday_counts_unique_invoices() -> None:
    df = pd.DataFrame(
        {
            "InvoiceNo": [
                "A",
                "A",
                "B",
            ],
            "DayOfWeek": [
                "Monday",
                "Monday",
                "Tuesday",
            ],
        }
    )

    result = orders_by_weekday(df)

    monday = result.loc[
        result["DayOfWeek"]
        == "Monday"
    ]

    assert (
        monday["Orders"].iloc[0]
        == 1
    )


def test_orders_by_hour_counts_unique_invoices() -> None:
    df = pd.DataFrame(
        {
            "InvoiceNo": [
                "A",
                "A",
                "B",
            ],
            "Hour": [
                10,
                10,
                11,
            ],
        }
    )

    result = orders_by_hour(df)

    hour_10 = result.loc[
        result["Hour"] == 10
    ]

    assert (
        hour_10["Orders"].iloc[0]
        == 1
    )


def test_cancellation_rate() -> None:
    all_transactions = pd.DataFrame(
        {
            "InvoiceNo": [
                "A",
                "B",
                "C1",
                "C2",
            ]
        }
    )

    cancellations = pd.DataFrame(
        {
            "InvoiceNo": [
                "C1",
                "C2",
            ]
        }
    )

    result = (
        calculate_cancellation_rate(
            all_transactions,
            cancellations,
        )
    )

    assert result == 0.5


def test_country_revenue_share() -> None:
    df = pd.DataFrame(
        {
            "Country": [
                "UK",
                "UK",
                "France",
            ],
            "Revenue": [
                50.0,
                30.0,
                20.0,
            ],
        }
    )

    result = (
        calculate_country_revenue_share(
            df,
            "UK",
        )
    )

    assert result == 0.8


def test_country_revenue_share_zero_revenue() -> None:
    df = pd.DataFrame(
        {
            "Country": [
                "UK",
                "France",
            ],
            "Revenue": [
                0.0,
                0.0,
            ],
        }
    )

    assert (
        calculate_country_revenue_share(
            df,
            "UK",
        )
        == 0.0
    )


def test_top_international_markets_excludes_domestic_market() -> None:
    df = pd.DataFrame(
        {
            "Country": [
                "UK",
                "France",
                "Germany",
            ],
            "Revenue": [
                1000.0,
                200.0,
                300.0,
            ],
        }
    )

    result = top_international_markets(
        df,
        exclude_country="UK",
    )

    assert (
        "UK"
        not in result[
            "Country"
        ].tolist()
    )

    assert (
        result.iloc[0]["Country"]
        == "Germany"
    )


def test_quantity_outliers_returns_largest_quantity() -> None:
    df = pd.DataFrame(
        {
            "InvoiceNo": [
                "A",
                "B",
            ],
            "StockCode": [
                "11111",
                "22222",
            ],
            "Description": [
                "Product A",
                "Product B",
            ],
            "Quantity": [
                10,
                100,
            ],
            "UnitPrice": [
                1.0,
                1.0,
            ],
            "Revenue": [
                10.0,
                100.0,
            ],
            "CustomerID": [
                1,
                2,
            ],
            "Country": [
                "UK",
                "UK",
            ],
            "InvoiceDate": pd.to_datetime(
                [
                    "2011-01-01",
                    "2011-01-02",
                ]
            ),
        }
    )

    result = investigate_quantity_outliers(
        df,
        n=1,
    )

    assert (
        result.iloc[0]["Quantity"]
        == 100
    )


def test_special_stock_codes_detects_non_standard_codes() -> None:
    df = pd.DataFrame(
        {
            "StockCode": [
                "22423",
                "85123A",
                "DOT",
                "POST",
            ],
            "Description": [
                "Normal Product",
                "Normal Product 2",
                "DOTCOM POSTAGE",
                "POSTAGE",
            ],
            "Quantity": [
                1,
                1,
                1,
                1,
            ],
            "Revenue": [
                10.0,
                20.0,
                30.0,
                40.0,
            ],
        }
    )

    result = (
        investigate_special_stock_codes(
            df
        )
    )

    codes = set(
        result["StockCode"]
    )

    assert "DOT" in codes
    assert "POST" in codes
    assert "22423" not in codes
    assert "85123A" not in codes


def test_duplicate_sensitivity() -> None:
    df = pd.DataFrame(
        {
            "Revenue": [
                100.0,
                50.0,
                25.0,
            ],
            "IsDuplicate": [
                False,
                True,
                True,
            ],
        }
    )

    result = (
        calculate_duplicate_sensitivity(
            df
        )
    )

    with_duplicates = float(
        result.loc[
            result["metric"]
            == "revenue_with_duplicate_groups",
            "value",
        ].iloc[0]
    )

    without_duplicates = float(
        result.loc[
            result["metric"]
            == "revenue_without_duplicate_groups",
            "value",
        ].iloc[0]
    )

    difference = float(
        result.loc[
            result["metric"]
            == "revenue_difference",
            "value",
        ].iloc[0]
    )

    assert with_duplicates == 175.0
    assert without_duplicates == 100.0
    assert difference == 75.0


def test_duplicate_sensitivity_requires_duplicate_flag() -> None:
    df = pd.DataFrame(
        {
            "Revenue": [
                100.0,
            ]
        }
    )

    with pytest.raises(
        ValueError,
        match="IsDuplicate",
    ):
        calculate_duplicate_sensitivity(
            df
        )

def test_monthly_growth() -> None:
    df = pd.DataFrame(
        {
            "YearMonth": [
                "2011-01",
                "2011-02",
                "2011-03",
            ],
            "Revenue": [
                100.0,
                120.0,
                90.0,
            ],
        }
    )

    result = calculate_monthly_growth(
        df
    )

    assert pd.isna(
        result.loc[
            0,
            "GrowthPercent",
        ]
    )

    assert result.loc[
               1,
               "GrowthPercent",
           ] == pytest.approx(20.0)

    assert result.loc[
               2,
               "GrowthPercent",
           ] == pytest.approx(-25.0)