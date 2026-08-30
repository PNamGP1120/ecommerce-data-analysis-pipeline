from __future__ import annotations

import pandas as pd

from ecommerce_analysis.config import RAW_DATA_PATH
from ecommerce_analysis.data_loader import load_raw_data
from ecommerce_analysis.data_validator import validate_data


def build_data_quality_summary(df: pd.DataFrame) -> pd.DataFrame:
    invoice_dates = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    cancel_mask = df["InvoiceNo"].astype(str).str.startswith("C")

    rows = [
        ("rows", len(df)),
        ("columns", df.shape[1]),
        ("unique_invoices", df["InvoiceNo"].nunique()),
        ("unique_customers", df["CustomerID"].nunique(dropna=True)),
        ("unique_stock_codes", df["StockCode"].nunique()),
        ("countries", df["Country"].nunique(dropna=True)),
        ("missing_customer_id", df["CustomerID"].isna().sum()),
        ("missing_description", df["Description"].isna().sum()),
        ("duplicate_rows", df.duplicated().sum()),
        ("quantity_negative", (df["Quantity"] < 0).sum()),
        ("quantity_zero", (df["Quantity"] == 0).sum()),
        ("unit_price_negative", (df["UnitPrice"] < 0).sum()),
        ("unit_price_zero", (df["UnitPrice"] == 0).sum()),
        ("cancelled_rows", cancel_mask.sum()),
        ("cancelled_invoices", df.loc[cancel_mask, "InvoiceNo"].nunique()),
        ("start_date", invoice_dates.min()),
        ("end_date", invoice_dates.max()),
        ("unparseable_invoice_dates", invoice_dates.isna().sum()),
    ]

    return pd.DataFrame(rows, columns=["metric", "value"])


def main() -> None:
    print(f"[quality] Loading raw data: {RAW_DATA_PATH}")

    df = load_raw_data(RAW_DATA_PATH)
    validate_data(df)

    summary = build_data_quality_summary(df)

    print()
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
