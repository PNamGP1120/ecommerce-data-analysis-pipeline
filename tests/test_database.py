from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import pytest

from ecommerce_analysis.database import (
    build_database,
    get_connection,
    get_database_summary,
)


@pytest.fixture
def sample_processed_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "InvoiceNo": [
                "100001",
                "100001",
                "C100002",
                "100003",
                "100004",
            ],
            "StockCode": [
                "11111",
                "22222",
                "33333",
                "44444",
                "55555",
            ],
            "Description": [
                "Product A",
                "Product B",
                "Product C",
                None,
                "Adjustment",
            ],
            "Quantity": [
                2,
                4,
                -1,
                1,
                -2,
            ],
            "InvoiceDate": pd.to_datetime(
                [
                    "2011-01-01 10:00:00",
                    "2011-01-01 10:00:00",
                    "2011-01-02 11:00:00",
                    "2011-01-03 12:00:00",
                    "2011-01-04 13:00:00",
                ]
            ),
            "UnitPrice": [
                5.0,
                5.0,
                5.0,
                0.0,
                2.0,
            ],
            "CustomerID": pd.Series(
                [
                    1001,
                    1001,
                    1002,
                    None,
                    None,
                ],
                dtype="Int64",
            ),
            "Country": [
                "UK",
                "UK",
                "UK",
                "UK",
                "UK",
            ],
            "IsCancelled": [
                False,
                False,
                True,
                False,
                False,
            ],
            "IsNegativeQuantity": [
                False,
                False,
                True,
                False,
                True,
            ],
            "IsZeroQuantity": [
                False,
                False,
                False,
                False,
                False,
            ],
            "IsNegativePrice": [
                False,
                False,
                False,
                False,
                False,
            ],
            "IsZeroPrice": [
                False,
                False,
                False,
                True,
                False,
            ],
            "HasCustomerID": [
                True,
                True,
                True,
                False,
                False,
            ],
            "HasDescription": [
                True,
                True,
                True,
                False,
                True,
            ],
            "IsDuplicate": [
                False,
                False,
                False,
                False,
                False,
            ],
            "IsNegativeNonCancelled": [
                False,
                False,
                False,
                False,
                True,
            ],
            "Revenue": [
                10.0,
                20.0,
                -5.0,
                0.0,
                -4.0,
            ],
            "Year": [
                2011,
                2011,
                2011,
                2011,
                2011,
            ],
            "Month": [
                1,
                1,
                1,
                1,
                1,
            ],
            "Day": [
                1,
                1,
                2,
                3,
                4,
            ],
            "DayOfWeek": [
                "Saturday",
                "Saturday",
                "Sunday",
                "Monday",
                "Tuesday",
            ],
            "Hour": [
                10,
                10,
                11,
                12,
                13,
            ],
            "YearMonth": [
                "2011-01",
                "2011-01",
                "2011-01",
                "2011-01",
                "2011-01",
            ],
            "Date": [
                "2011-01-01",
                "2011-01-01",
                "2011-01-02",
                "2011-01-03",
                "2011-01-04",
            ],
        }
    )


@pytest.fixture
def database_path(
    tmp_path: Path,
    sample_processed_data: pd.DataFrame,
) -> Path:
    path = (
        tmp_path
        / "test_ecommerce.db"
    )

    build_database(
        sample_processed_data,
        path,
    )

    return path


def test_database_file_is_created(
    database_path: Path,
) -> None:
    assert database_path.exists()


def test_foreign_keys_are_enabled(
    database_path: Path,
) -> None:
    connection = get_connection(
        database_path
    )

    try:
        result = connection.execute(
            "PRAGMA foreign_keys;"
        ).fetchone()[0]

        assert result == 1

    finally:
        connection.close()


def test_required_tables_exist(
    database_path: Path,
) -> None:
    connection = sqlite3.connect(
        database_path
    )

    try:
        rows = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table';
            """
        ).fetchall()

        names = {
            row[0]
            for row in rows
        }

        assert "transactions" in names
        assert "customers" in names
        assert "products" in names

    finally:
        connection.close()


def test_required_views_exist(
    database_path: Path,
) -> None:
    connection = sqlite3.connect(
        database_path
    )

    try:
        rows = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'view';
            """
        ).fetchall()

        names = {
            row[0]
            for row in rows
        }

        assert "valid_sales" in names
        assert "customer_sales" in names
        assert "cancellations" in names
        assert "anomalies" in names

    finally:
        connection.close()


def test_database_summary_counts(
    database_path: Path,
) -> None:
    connection = get_connection(
        database_path
    )

    try:
        summary = get_database_summary(
            connection
        )

        assert summary[
            "transactions"
        ] == 5

        assert summary[
            "customers"
        ] == 2

        assert summary[
            "products"
        ] == 4

        assert summary[
            "valid_sales"
        ] == 2

        assert summary[
            "customer_sales"
        ] == 2

        assert summary[
            "cancellations"
        ] == 1

        assert summary[
            "anomalies"
        ] == 2

    finally:
        connection.close()


def test_valid_sales_revenue_matches_expected(
    database_path: Path,
) -> None:
    connection = get_connection(
        database_path
    )

    try:
        revenue = connection.execute(
            """
            SELECT SUM(Revenue)
            FROM valid_sales;
            """
        ).fetchone()[0]

        assert revenue == 30.0

    finally:
        connection.close()


def test_null_customer_ids_are_preserved(
    database_path: Path,
) -> None:
    connection = get_connection(
        database_path
    )

    try:
        count = connection.execute(
            """
            SELECT COUNT(*)
            FROM transactions
            WHERE CustomerID IS NULL;
            """
        ).fetchone()[0]

        assert count == 2

    finally:
        connection.close()


def test_indexes_are_created(
    database_path: Path,
) -> None:
    connection = get_connection(
        database_path
    )

    try:
        rows = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'index';
            """
        ).fetchall()

        names = {
            row[0]
            for row in rows
        }

        assert (
            "idx_transactions_invoice_no"
            in names
        )

        assert (
            "idx_transactions_customer_id"
            in names
        )

        assert (
            "idx_transactions_stock_code"
            in names
        )

        assert (
            "idx_transactions_year_month"
            in names
        )

    finally:
        connection.close()