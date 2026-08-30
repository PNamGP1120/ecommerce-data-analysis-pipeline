from __future__ import annotations

import pandas as pd


EXPECTED_COLUMNS = {
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
}


def validate_not_empty(df: pd.DataFrame) -> None:
    """Raise ValueError when the dataset contains no rows."""
    if df.empty:
        raise ValueError("Dataset is empty.")


def validate_columns(df: pd.DataFrame) -> None:
    """Validate that all required columns exist."""
    missing_columns = EXPECTED_COLUMNS - set(df.columns)

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing required columns: {missing}")


def validate_unique_columns(df: pd.DataFrame) -> None:
    """Validate that column names are unique."""
    if not df.columns.is_unique:
        duplicated = df.columns[df.columns.duplicated()].tolist()
        raise ValueError(f"Duplicate column names found: {duplicated}")


def validate_data(df: pd.DataFrame) -> None:
    """
    Run structural validation for the raw Online Retail dataset.

    This deliberately does NOT reject missing CustomerID/Description,
    negative Quantity, zero/negative UnitPrice, duplicated rows, or
    cancelled invoices. Those are data-quality/business issues that
    must be investigated before a cleaning policy is applied.
    """
    validate_not_empty(df)
    validate_columns(df)
    validate_unique_columns(df)
