from pathlib import Path

import pandas as pd
from ucimlrepo import fetch_ucirepo


UCI_DATASET_ID = 352


def fetch_online_retail() -> pd.DataFrame:
    """
    Fetch the Online Retail dataset from UCI Machine Learning Repository.

    Returns
    -------
    pd.DataFrame
        Raw Online Retail dataset.

    Raises
    ------
    ValueError
        If the fetched dataset is empty.
    """
    dataset = fetch_ucirepo(id=UCI_DATASET_ID)

    df = dataset.data.original.copy()

    if df.empty:
        raise ValueError("Fetched dataset is empty.")

    return df


def save_csv(
    df: pd.DataFrame,
    path: Path,
) -> None:
    """
    Save a DataFrame to a CSV file.

    Parameters
    ----------
    df:
        DataFrame to save.
    path:
        Destination CSV path.
    """
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        path,
        index=False,
    )


def load_csv(
    path: Path,
) -> pd.DataFrame:
    """
    Load a DataFrame from a CSV file.

    Parameters
    ----------
    path:
        Path to the CSV file.

    Returns
    -------
    pd.DataFrame
        Loaded DataFrame.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the loaded dataset is empty.
    """
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {path}"
        )

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError(
            f"Dataset is empty: {path}"
        )

    return df


def load_raw_data(
    path: Path,
) -> pd.DataFrame:
    """
    Load the raw Online Retail dataset.

    This wrapper keeps the intent explicit while reusing load_csv().
    """
    return load_csv(path)


def load_interim_data(
    path: Path,
) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Interim dataset not found: {path}"
        )

    df = pd.read_csv(
        path,
        parse_dates=["InvoiceDate"],
        dtype={
            "InvoiceNo": "string",
            "StockCode": "string",
            "Description": "string",
            "Country": "string",
        },
    )

    if df.empty:
        raise ValueError(
            f"Interim dataset is empty: {path}"
        )

    df["CustomerID"] = (
        pd.to_numeric(
            df["CustomerID"],
            errors="coerce",
        )
        .astype("Int64")
    )

    return df


def load_processed_data(
    path: Path,
) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {path}"
        )

    df = pd.read_csv(
        path,
        parse_dates=[
            "InvoiceDate",
            "Date",
        ],
        dtype={
            "InvoiceNo": "string",
            "StockCode": "string",
            "Description": "string",
            "Country": "string",
        },
    )

    if df.empty:
        raise ValueError(
            f"Processed dataset is empty: {path}"
        )

    df["CustomerID"] = (
        pd.to_numeric(
            df["CustomerID"],
            errors="coerce",
        )
        .astype("Int64")
    )

    return df