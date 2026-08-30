import pandas as pd

from ecommerce_analysis.data_cleaner import (
    add_cancellation_flag,
    add_duplicate_flag,
    add_missing_value_flags,
    add_price_flags,
    add_quantity_flags,
    clean_data,
    convert_data_types,
)

def test_cancellation_flag() -> None:
    df = pd.DataFrame(
        {
            "InvoiceNo": [
                "536365",
                "C536379",
            ]
        }
    )

    result = add_cancellation_flag(df)

    assert result[
        "IsCancelled"
    ].tolist() == [
        False,
        True,
    ]

def test_quantity_flags() -> None:
    df = pd.DataFrame(
        {
            "Quantity": [
                5,
                0,
                -2,
            ]
        }
    )

    result = add_quantity_flags(df)

    assert result[
        "IsNegativeQuantity"
    ].tolist() == [
        False,
        False,
        True,
    ]

    assert result[
        "IsZeroQuantity"
    ].tolist() == [
        False,
        True,
        False,
    ]

def test_price_flags() -> None:
    df = pd.DataFrame(
        {
            "UnitPrice": [
                2.5,
                0,
                -3,
            ]
        }
    )

    result = add_price_flags(df)

    assert result[
        "IsZeroPrice"
    ].tolist() == [
        False,
        True,
        False,
    ]

    assert result[
        "IsNegativePrice"
    ].tolist() == [
        False,
        False,
        True,
    ]

def test_missing_value_flags() -> None:
    df = pd.DataFrame(
        {
            "CustomerID": [
                17850,
                None,
            ],
            "Description": [
                "PRODUCT",
                None,
            ],
        }
    )

    result = add_missing_value_flags(df)

    assert result[
        "HasCustomerID"
    ].tolist() == [
        True,
        False,
    ]

    assert result[
        "HasDescription"
    ].tolist() == [
        True,
        False,
    ]

def test_duplicate_flag() -> None:
    df = pd.DataFrame(
        {
            "InvoiceNo": [
                "1",
                "1",
                "2",
            ],
            "StockCode": [
                "A",
                "A",
                "B",
            ],
            "Description": [
                "Item A",
                "Item A",
                "Item B",
            ],
            "Quantity": [
                1,
                1,
                2,
            ],
            "InvoiceDate": pd.to_datetime(
                [
                    "2020-01-01",
                    "2020-01-01",
                    "2020-01-02",
                ]
            ),
            "UnitPrice": [
                2.0,
                2.0,
                3.0,
            ],
            "CustomerID": pd.Series(
                [1, 1, 2],
                dtype="Int64",
            ),
            "Country": [
                "UK",
                "UK",
                "France",
            ],
        }
    )

    result = add_duplicate_flag(df)

    assert result[
        "IsDuplicate"
    ].tolist() == [
        True,
        True,
        False,
    ]

def test_negative_non_cancelled() -> None:
    df = pd.DataFrame(
        {
            "InvoiceNo": [
                "C123",
                "123",
            ],
            "Quantity": [
                -1,
                -1,
            ],
        }
    )

    df = add_cancellation_flag(df)
    df = add_quantity_flags(df)

    from ecommerce_analysis.data_cleaner import (
        add_anomaly_flags,
    )

    result = add_anomaly_flags(df)

    assert result[
        "IsNegativeNonCancelled"
    ].tolist() == [
        False,
        True,
    ]

def test_convert_customer_id_to_nullable_integer() -> None:
    df = pd.DataFrame(
        {
            "InvoiceNo": ["1", "2"],
            "StockCode": ["A", "B"],
            "Description": ["A", "B"],
            "Quantity": [1, 1],
            "InvoiceDate": [
                "12/1/2010 8:26",
                "12/2/2010 9:30",
            ],
            "UnitPrice": [1.0, 2.0],
            "CustomerID": [
                17850.0,
                None,
            ],
            "Country": [
                "UK",
                "UK",
            ],
        }
    )

    result = convert_data_types(df)

    assert str(
        result["CustomerID"].dtype
    ) == "Int64"

    assert pd.api.types.is_datetime64_any_dtype(
        result["InvoiceDate"]
    )

