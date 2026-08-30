import pandas as pd

from ecommerce_analysis.analytical_views import (
    get_anomalies,
    get_cancellations,
    get_customer_sales,
    get_valid_sales,
)


def test_customer_sales_requires_customer_id() -> None:
    df = pd.DataFrame(
        {
            "IsCancelled": [False, False],
            "IsNegativeQuantity": [False, False],
            "IsZeroQuantity": [False, False],
            "IsNegativePrice": [False, False],
            "IsZeroPrice": [False, False],
            "HasCustomerID": [True, False],
        }
    )

    result = get_customer_sales(df)

    assert len(result) == 1
    assert result["HasCustomerID"].all()


def test_cancellations_only_returns_cancelled_rows() -> None:
    df = pd.DataFrame(
        {
            "IsCancelled": [
                True,
                False,
                True,
            ]
        }
    )

    result = get_cancellations(df)

    assert len(result) == 2
    assert result["IsCancelled"].all()


def test_anomalies_returns_quality_issue_rows() -> None:
    df = pd.DataFrame(
        {
            "IsNegativeNonCancelled": [
                True,
                False,
                False,
                False,
            ],
            "IsNegativePrice": [
                False,
                True,
                False,
                False,
            ],
            "IsZeroPrice": [
                False,
                False,
                True,
                False,
            ],
            "HasDescription": [
                True,
                True,
                True,
                True,
            ],
        }
    )

    result = get_anomalies(df)

    assert len(result) == 3