from __future__ import annotations

import sqlite3

import pandas as pd
import pytest

from ecommerce_analysis.sql_analysis import (
    execute_query,
    split_sql_statements,
)

import math

from ecommerce_analysis.analysis import (
    calculate_average_order_value,
    calculate_total_orders,
    calculate_total_revenue,
)
from ecommerce_analysis.analytical_views import (
    get_valid_sales,
)


@pytest.fixture
def connection() -> sqlite3.Connection:
    conn = sqlite3.connect(
        ":memory:"
    )

    conn.execute(
        """
        CREATE TABLE sales (
            InvoiceNo TEXT,
            CustomerID INTEGER,
            Revenue REAL
        );
        """
    )

    conn.executemany(
        """
        INSERT INTO sales (
            InvoiceNo,
            CustomerID,
            Revenue
        )
        VALUES (?, ?, ?);
        """,
        [
            ("A", 1, 10.0),
            ("A", 1, 20.0),
            ("B", 2, 30.0),
        ],
    )

    yield conn

    conn.close()


def test_execute_query_returns_dataframe(
    connection: sqlite3.Connection,
) -> None:
    result = execute_query(
        connection,
        """
        SELECT *
        FROM sales;
        """,
    )

    assert isinstance(
        result,
        pd.DataFrame,
    )

    assert len(result) == 3


def test_execute_query_total_revenue(
    connection: sqlite3.Connection,
) -> None:
    result = execute_query(
        connection,
        """
        SELECT
            SUM(Revenue)
            AS Revenue
        FROM sales;
        """,
    )

    assert (
        result.iloc[0]["Revenue"]
        == 60.0
    )


def test_sql_counts_unique_orders(
    connection: sqlite3.Connection,
) -> None:
    result = execute_query(
        connection,
        """
        SELECT
            COUNT(
                DISTINCT InvoiceNo
            ) AS Orders
        FROM sales;
        """,
    )

    assert (
        result.iloc[0]["Orders"]
        == 2
    )


def test_split_sql_statements() -> None:
    sql = """
    SELECT 1;

    SELECT 2;
    """

    statements = (
        split_sql_statements(
            sql
        )
    )

    assert len(statements) == 2


def test_execute_query_rejects_empty_query(
    connection: sqlite3.Connection,
) -> None:
    with pytest.raises(
        ValueError,
        match="cannot be empty",
    ):
        execute_query(
            connection,
            "",
        )