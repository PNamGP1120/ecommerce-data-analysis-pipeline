import pandas as pd
import pytest

from ecommerce_analysis.data_validator import (
    EXPECTED_COLUMNS,
    validate_columns,
    validate_data,
    validate_not_empty,
    validate_unique_columns,
)


def make_valid_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "InvoiceNo": ["536365"],
            "StockCode": ["85123A"],
            "Description": ["WHITE HANGING HEART T-LIGHT HOLDER"],
            "Quantity": [6],
            "InvoiceDate": ["12/1/2010 8:26"],
            "UnitPrice": [2.55],
            "CustomerID": [17850.0],
            "Country": ["United Kingdom"],
        }
    )


def test_expected_columns_are_correct() -> None:
    assert EXPECTED_COLUMNS == {
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "CustomerID",
        "Country",
    }


def test_validate_not_empty_accepts_non_empty_dataframe() -> None:
    validate_not_empty(make_valid_dataframe())


def test_validate_not_empty_raises_for_empty_dataframe() -> None:
    with pytest.raises(ValueError, match="Dataset is empty"):
        validate_not_empty(pd.DataFrame())


def test_validate_columns_accepts_valid_schema() -> None:
    validate_columns(make_valid_dataframe())


def test_validate_columns_raises_for_missing_column() -> None:
    df = make_valid_dataframe().drop(columns=["Country"])

    with pytest.raises(ValueError, match="Country"):
        validate_columns(df)


def test_validate_columns_allows_extra_columns() -> None:
    df = make_valid_dataframe()
    df["ExtraColumn"] = "extra"

    validate_columns(df)


def test_validate_unique_columns_accepts_unique_columns() -> None:
    validate_unique_columns(make_valid_dataframe())


def test_validate_unique_columns_raises_for_duplicate_names() -> None:
    df = pd.DataFrame([[1, 2]], columns=["InvoiceNo", "InvoiceNo"])

    with pytest.raises(ValueError, match="Duplicate column names"):
        validate_unique_columns(df)


def test_validate_data_allows_business_quality_issues() -> None:
    df = make_valid_dataframe()
    df.loc[0, "CustomerID"] = None
    df.loc[0, "Quantity"] = -1
    df.loc[0, "UnitPrice"] = 0

    validate_data(df)


def test_validate_data_runs_schema_validation() -> None:
    df = make_valid_dataframe().drop(columns=["StockCode"])

    with pytest.raises(ValueError, match="StockCode"):
        validate_data(df)
