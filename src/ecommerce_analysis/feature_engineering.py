import pandas as pd


def add_revenue_feature(
    df: pd.DataFrame,
) -> pd.DataFrame:
    result = df.copy()

    result["Revenue"] = (
        result["Quantity"]
        * result["UnitPrice"]
    )

    return result


def add_time_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    result = df.copy()

    result["Year"] = (
        result["InvoiceDate"].dt.year
    )

    result["Month"] = (
        result["InvoiceDate"].dt.month
    )

    result["Day"] = (
        result["InvoiceDate"].dt.day
    )

    result["DayOfWeek"] = (
        result["InvoiceDate"]
        .dt.day_name()
    )

    result["Hour"] = (
        result["InvoiceDate"].dt.hour
    )

    result["YearMonth"] = (
        result["InvoiceDate"]
        .dt.strftime("%Y-%m")
    )

    result["Date"] = (
        result["InvoiceDate"].dt.date
    )

    return result


def build_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    result = df.copy()

    result = add_revenue_feature(
        result
    )

    result = add_time_features(
        result
    )

    return result