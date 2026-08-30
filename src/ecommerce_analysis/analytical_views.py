from __future__ import annotations

import pandas as pd


def get_valid_sales(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Return transactions considered valid for sales analysis."""
    mask = (
        ~df["IsCancelled"]
        & ~df["IsNegativeQuantity"]
        & ~df["IsZeroQuantity"]
        & ~df["IsNegativePrice"]
        & ~df["IsZeroPrice"]
    )

    return df.loc[mask].copy()


def get_customer_sales(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Return valid sales that have an identified customer."""
    sales = get_valid_sales(df)

    return sales.loc[
        sales["HasCustomerID"]
    ].copy()


def get_cancellations(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Return cancelled transaction lines."""
    return df.loc[
        df["IsCancelled"]
    ].copy()


def get_anomalies(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Return records requiring separate quality/business investigation."""
    mask = (
        df["IsNegativeNonCancelled"]
        | df["IsNegativePrice"]
        | df["IsZeroPrice"]
        | ~df["HasDescription"]
    )

    return df.loc[mask].copy()