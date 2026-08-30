from __future__ import annotations

import pandas as pd


def convert_data_types(
    df: pd.DataFrame,
) -> pd.DataFrame:
    result = df.copy()

    result["InvoiceNo"] = result["InvoiceNo"].astype("string")
    result["StockCode"] = result["StockCode"].astype("string")
    result["Description"] = result["Description"].astype("string")
    result["Country"] = result["Country"].astype("string")

    result["InvoiceDate"] = pd.to_datetime(
        result["InvoiceDate"],
        errors="coerce",
    )

    result["CustomerID"] = (
        pd.to_numeric(
            result["CustomerID"],
            errors="coerce",
        )
        .astype("Int64")
    )

    return result


def normalize_strings(
    df: pd.DataFrame,
) -> pd.DataFrame:
    result = df.copy()

    for column in [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Country",
    ]:
        result[column] = (
            result[column]
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

    return result


def add_cancellation_flag(
    df: pd.DataFrame,
) -> pd.DataFrame:
    result = df.copy()

    result["IsCancelled"] = (
        result["InvoiceNo"]
        .str.startswith("C", na=False)
    )

    return result


def add_quantity_flags(
    df: pd.DataFrame,
) -> pd.DataFrame:
    result = df.copy()

    result["IsNegativeQuantity"] = (
        result["Quantity"] < 0
    )

    result["IsZeroQuantity"] = (
        result["Quantity"] == 0
    )

    return result


def add_price_flags(
    df: pd.DataFrame,
) -> pd.DataFrame:
    result = df.copy()

    result["IsNegativePrice"] = (
        result["UnitPrice"] < 0
    )

    result["IsZeroPrice"] = (
        result["UnitPrice"] == 0
    )

    return result


def add_missing_value_flags(
    df: pd.DataFrame,
) -> pd.DataFrame:
    result = df.copy()

    result["HasCustomerID"] = (
        result["CustomerID"].notna()
    )

    result["HasDescription"] = (
        result["Description"].notna()
    )

    return result


def add_duplicate_flag(
    df: pd.DataFrame,
) -> pd.DataFrame:
    result = df.copy()

    source_columns = [
        "InvoiceNo",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "UnitPrice",
        "CustomerID",
        "Country",
    ]

    result["IsDuplicate"] = result.duplicated(
        subset=source_columns,
        keep=False,
    )

    return result


def add_anomaly_flags(
    df: pd.DataFrame,
) -> pd.DataFrame:
    result = df.copy()

    result["IsNegativeNonCancelled"] = (
        result["IsNegativeQuantity"]
        & ~result["IsCancelled"]
    )

    return result


def clean_data(
    df: pd.DataFrame,
) -> pd.DataFrame:
    result = df.copy()

    result = convert_data_types(result)
    result = normalize_strings(result)

    result = add_cancellation_flag(result)
    result = add_quantity_flags(result)
    result = add_price_flags(result)
    result = add_missing_value_flags(result)
    result = add_duplicate_flag(result)
    result = add_anomaly_flags(result)

    return result

def build_cleaning_summary(
    df: pd.DataFrame,
) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "metric": [
                "rows",
                "cancelled_rows",
                "negative_quantity_rows",
                "negative_non_cancelled_rows",
                "zero_quantity_rows",
                "negative_price_rows",
                "zero_price_rows",
                "missing_customer_rows",
                "missing_description_rows",
                "duplicate_rows",
                "invalid_invoice_dates",
            ],
            "value": [
                len(df),
                int(df["IsCancelled"].sum()),
                int(df["IsNegativeQuantity"].sum()),
                int(df["IsNegativeNonCancelled"].sum()),
                int(df["IsZeroQuantity"].sum()),
                int(df["IsNegativePrice"].sum()),
                int(df["IsZeroPrice"].sum()),
                int((~df["HasCustomerID"]).sum()),
                int((~df["HasDescription"]).sum()),
                int(df["IsDuplicate"].sum()),
                int(df["InvoiceDate"].isna().sum()),
            ],
        }
    )