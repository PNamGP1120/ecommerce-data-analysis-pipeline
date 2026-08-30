import pandas as pd

from ecommerce_analysis.feature_engineering import (
    add_revenue_feature,
    add_time_features,
    build_features,
)


def test_revenue_calculation() -> None:
    df = pd.DataFrame(
        {
            "Quantity": [
                2,
                -3,
            ],
            "UnitPrice": [
                5.0,
                4.0,
            ],
        }
    )

    result = add_revenue_feature(df)

    assert result["Revenue"].tolist() == [
        10.0,
        -12.0,
    ]

def test_time_features() -> None:
    df = pd.DataFrame(
        {
            "InvoiceDate": pd.to_datetime(
                [
                    "2011-11-16 10:39:00",
                ]
            )
        }
    )

    result = add_time_features(df)

    assert result.loc[0, "Year"] == 2011
    assert result.loc[0, "Month"] == 11
    assert result.loc[0, "Day"] == 16
    assert result.loc[0, "DayOfWeek"] == "Wednesday"
    assert result.loc[0, "Hour"] == 10
    assert result.loc[0, "YearMonth"] == "2011-11"

def test_feature_engineering_does_not_mutate_input() -> None:
    df = pd.DataFrame(
        {
            "Quantity": [2],
            "UnitPrice": [5.0],
        }
    )

    original_columns = df.columns.tolist()

    add_revenue_feature(df)

    assert df.columns.tolist() == original_columns

def test_build_features() -> None:
    df = pd.DataFrame(
        {
            "InvoiceDate": pd.to_datetime(
                ["2011-12-09 12:50:00"]
            ),
            "Quantity": [3],
            "UnitPrice": [2.5],
        }
    )

    result = build_features(df)

    expected_columns = {
        "Revenue",
        "Year",
        "Month",
        "YearMonth",
        "Day",
        "DayOfWeek",
        "Hour",
    }

    assert expected_columns.issubset(
        result.columns
    )

    assert result.loc[0, "Revenue"] == 7.5