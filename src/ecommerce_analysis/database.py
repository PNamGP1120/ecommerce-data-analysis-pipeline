from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


TRANSACTION_COLUMNS = [
    "InvoiceNo",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "UnitPrice",
    "CustomerID",
    "Country",
    "IsCancelled",
    "IsNegativeQuantity",
    "IsZeroQuantity",
    "IsNegativePrice",
    "IsZeroPrice",
    "HasCustomerID",
    "HasDescription",
    "IsDuplicate",
    "IsNegativeNonCancelled",
    "Revenue",
    "Year",
    "Month",
    "Day",
    "DayOfWeek",
    "Hour",
    "YearMonth",
    "Date",
]


BOOLEAN_COLUMNS = [
    "IsCancelled",
    "IsNegativeQuantity",
    "IsZeroQuantity",
    "IsNegativePrice",
    "IsZeroPrice",
    "HasCustomerID",
    "HasDescription",
    "IsDuplicate",
    "IsNegativeNonCancelled",
]


SCHEMA_SQL = """
CREATE TABLE customers (
    CustomerID INTEGER PRIMARY KEY
);


CREATE TABLE products (
    StockCode TEXT NOT NULL,
    Description TEXT NOT NULL,

    PRIMARY KEY (
        StockCode,
        Description
    )
);


CREATE TABLE transactions (
    TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,

    InvoiceNo TEXT NOT NULL,
    StockCode TEXT NOT NULL,
    Description TEXT,

    Quantity INTEGER NOT NULL,
    InvoiceDate TEXT NOT NULL,
    UnitPrice REAL NOT NULL,

    CustomerID INTEGER,
    Country TEXT NOT NULL,

    IsCancelled INTEGER NOT NULL
        CHECK (IsCancelled IN (0, 1)),

    IsNegativeQuantity INTEGER NOT NULL
        CHECK (IsNegativeQuantity IN (0, 1)),

    IsZeroQuantity INTEGER NOT NULL
        CHECK (IsZeroQuantity IN (0, 1)),

    IsNegativePrice INTEGER NOT NULL
        CHECK (IsNegativePrice IN (0, 1)),

    IsZeroPrice INTEGER NOT NULL
        CHECK (IsZeroPrice IN (0, 1)),

    HasCustomerID INTEGER NOT NULL
        CHECK (HasCustomerID IN (0, 1)),

    HasDescription INTEGER NOT NULL
        CHECK (HasDescription IN (0, 1)),

    IsDuplicate INTEGER NOT NULL
        CHECK (IsDuplicate IN (0, 1)),

    IsNegativeNonCancelled INTEGER NOT NULL
        CHECK (
            IsNegativeNonCancelled
            IN (0, 1)
        ),

    Revenue REAL NOT NULL,

    Year INTEGER NOT NULL,
    Month INTEGER NOT NULL,
    Day INTEGER NOT NULL,

    DayOfWeek TEXT NOT NULL,
    Hour INTEGER NOT NULL,
    YearMonth TEXT NOT NULL,
    Date TEXT NOT NULL,

    FOREIGN KEY (CustomerID)
        REFERENCES customers(CustomerID),

    FOREIGN KEY (
        StockCode,
        Description
    )
        REFERENCES products(
            StockCode,
            Description
        )
);


CREATE INDEX idx_transactions_invoice_no
    ON transactions(InvoiceNo);


CREATE INDEX idx_transactions_customer_id
    ON transactions(CustomerID);


CREATE INDEX idx_transactions_stock_code
    ON transactions(StockCode);


CREATE INDEX idx_transactions_invoice_date
    ON transactions(InvoiceDate);


CREATE INDEX idx_transactions_country
    ON transactions(Country);


CREATE INDEX idx_transactions_year_month
    ON transactions(YearMonth);


CREATE VIEW valid_sales AS

SELECT *
FROM transactions

WHERE IsCancelled = 0
  AND IsNegativeQuantity = 0
  AND IsZeroQuantity = 0
  AND IsNegativePrice = 0
  AND IsZeroPrice = 0;


CREATE VIEW customer_sales AS

SELECT *
FROM valid_sales

WHERE HasCustomerID = 1;


CREATE VIEW cancellations AS

SELECT *
FROM transactions

WHERE IsCancelled = 1;


CREATE VIEW anomalies AS

SELECT *
FROM transactions

WHERE IsNegativeNonCancelled = 1
   OR IsNegativePrice = 1
   OR IsZeroPrice = 1
   OR HasDescription = 0;
"""


def get_connection(
    path: Path,
) -> sqlite3.Connection:
    """
    Open a SQLite connection with foreign-key enforcement enabled.
    """
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    connection = sqlite3.connect(
        path
    )

    connection.execute(
        "PRAGMA foreign_keys = ON;"
    )

    return connection


def reset_database(
    path: Path,
) -> None:
    """
    Remove an existing database so the build is reproducible.
    """
    if path.exists():
        path.unlink()


def _convert_boolean_column(
    series: pd.Series,
) -> pd.Series:
    """
    Convert a boolean-like Pandas Series to SQLite 0/1 values.
    """
    if pd.api.types.is_bool_dtype(
        series.dtype
    ):
        return series.astype("int64")

    mapping = {
        True: 1,
        False: 0,
        1: 1,
        0: 0,
        "True": 1,
        "False": 0,
        "true": 1,
        "false": 0,
    }

    result = series.map(mapping)

    if result.isna().any():
        raise ValueError(
            "Boolean column contains "
            "unsupported values."
        )

    return result.astype("int64")


def prepare_transactions_for_sqlite(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Prepare the processed transaction dataset for SQLite.

    Converts:
    - datetime -> ISO strings
    - booleans -> 0/1
    - CustomerID -> nullable integer
    - pandas missing values -> Python None
    """
    missing_columns = (
        set(TRANSACTION_COLUMNS)
        - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Processed dataset is missing "
            f"columns: {sorted(missing_columns)}"
        )

    result = df[
        TRANSACTION_COLUMNS
    ].copy()

    # ---------------------------------------
    # Datetime
    # ---------------------------------------
    invoice_dates = pd.to_datetime(
        result["InvoiceDate"],
        errors="raise",
    )

    result["InvoiceDate"] = (
        invoice_dates.dt.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    dates = pd.to_datetime(
        result["Date"],
        errors="raise",
    )

    result["Date"] = (
        dates.dt.strftime(
            "%Y-%m-%d"
        )
    )

    # ---------------------------------------
    # CustomerID
    # ---------------------------------------
    customer_ids = pd.to_numeric(
        result["CustomerID"],
        errors="coerce",
    )

    non_null_ids = customer_ids.dropna()

    if (
        non_null_ids
        % 1
        != 0
    ).any():
        raise ValueError(
            "CustomerID contains "
            "non-integer values."
        )

    result["CustomerID"] = (
        customer_ids.astype("Int64")
    )

    # ---------------------------------------
    # Boolean flags
    # ---------------------------------------
    for column in BOOLEAN_COLUMNS:
        result[column] = (
            _convert_boolean_column(
                result[column]
            )
        )

    # ---------------------------------------
    # Replace Pandas NA with Python None
    # for sqlite3 compatibility.
    # ---------------------------------------
    result = result.astype(object)

    result = result.where(
        pd.notna(result),
        None,
    )

    return result


def prepare_customers(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create the customer dimension.
    """
    customer_ids = pd.to_numeric(
        df["CustomerID"],
        errors="coerce",
    )

    customers = (
        customer_ids
        .dropna()
        .astype("int64")
        .drop_duplicates()
        .sort_values()
        .to_frame(
            name="CustomerID"
        )
        .reset_index(drop=True)
    )

    return customers


def prepare_products(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create the product dimension.

    StockCode alone is not treated as unique because
    the EDA showed multiple descriptions for some codes.
    """
    products = (
        df.loc[
            df["Description"].notna(),
            [
                "StockCode",
                "Description",
            ],
        ]
        .drop_duplicates()
        .sort_values(
            [
                "StockCode",
                "Description",
            ]
        )
        .reset_index(drop=True)
    )

    return products


def create_schema(
    connection: sqlite3.Connection,
) -> None:
    """
    Create tables, indexes and analytical views.
    """
    connection.executescript(
        SCHEMA_SQL
    )


def insert_dataframe(
    connection: sqlite3.Connection,
    df: pd.DataFrame,
    table_name: str,
    chunksize: int = 5000,
) -> None:
    """
    Append a Pandas DataFrame to an existing SQLite table.
    """
    df.to_sql(
        table_name,
        connection,
        if_exists="append",
        index=False,
        chunksize=chunksize,
    )


def get_row_count(
    connection: sqlite3.Connection,
    object_name: str,
) -> int:
    """
    Return row count from a table or view.
    """
    allowed_names = {
        "transactions",
        "customers",
        "products",
        "valid_sales",
        "customer_sales",
        "cancellations",
        "anomalies",
    }

    if object_name not in allowed_names:
        raise ValueError(
            f"Unsupported database object: "
            f"{object_name}"
        )

    cursor = connection.execute(
        f"SELECT COUNT(*) "
        f"FROM {object_name};"
    )

    return int(
        cursor.fetchone()[0]
    )


def get_total_revenue(
    connection: sqlite3.Connection,
) -> float:
    """
    Calculate total revenue from the SQL valid_sales view.
    """
    cursor = connection.execute(
        """
        SELECT COALESCE(
            SUM(Revenue),
            0
        )
        FROM valid_sales;
        """
    )

    return float(
        cursor.fetchone()[0]
    )


def get_database_summary(
    connection: sqlite3.Connection,
) -> dict[str, int | float]:
    """
    Return important database statistics.
    """
    return {
        "transactions": get_row_count(
            connection,
            "transactions",
        ),
        "customers": get_row_count(
            connection,
            "customers",
        ),
        "products": get_row_count(
            connection,
            "products",
        ),
        "valid_sales": get_row_count(
            connection,
            "valid_sales",
        ),
        "customer_sales": get_row_count(
            connection,
            "customer_sales",
        ),
        "cancellations": get_row_count(
            connection,
            "cancellations",
        ),
        "anomalies": get_row_count(
            connection,
            "anomalies",
        ),
        "total_revenue": (
            get_total_revenue(
                connection
            )
        ),
    }


def build_database(
    df: pd.DataFrame,
    path: Path,
) -> dict[str, int | float]:
    """
    Rebuild the complete SQLite database from processed data.
    """
    reset_database(path)

    transactions = (
        prepare_transactions_for_sqlite(
            df
        )
    )

    customers = prepare_customers(
        df
    )

    products = prepare_products(
        df
    )

    connection = get_connection(
        path
    )

    try:
        create_schema(
            connection
        )

        with connection:
            # Dimension tables must be inserted first
            # because transactions contain foreign keys.
            insert_dataframe(
                connection,
                customers,
                "customers",
            )

            insert_dataframe(
                connection,
                products,
                "products",
            )

            insert_dataframe(
                connection,
                transactions,
                "transactions",
            )

        summary = get_database_summary(
            connection
        )

        return summary

    finally:
        connection.close()