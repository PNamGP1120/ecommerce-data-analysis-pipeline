from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


def load_sql_file(
    path: Path,
) -> str:
    """
    Load SQL source text from a file.
    """
    if not path.exists():
        raise FileNotFoundError(
            f"SQL file not found: {path}"
        )

    sql = path.read_text(
        encoding="utf-8"
    )

    if not sql.strip():
        raise ValueError(
            f"SQL file is empty: {path}"
        )

    return sql


def execute_query(
    connection: sqlite3.Connection,
    query: str,
) -> pd.DataFrame:
    """
    Execute a SELECT query and return a DataFrame.
    """
    if not query.strip():
        raise ValueError(
            "SQL query cannot be empty."
        )

    return pd.read_sql_query(
        query,
        connection,
    )


def split_sql_statements(
    sql: str,
) -> list[str]:
    """
    Split a SQL script into executable statements.

    Suitable for the analysis SQL files in this project,
    where individual SELECT/CTE statements are separated
    by semicolons.
    """
    statements = [
        statement.strip()
        for statement
        in sql.split(";")
        if statement.strip()
    ]

    return statements


def execute_sql_script_queries(
    connection: sqlite3.Connection,
    sql: str,
) -> list[pd.DataFrame]:
    """
    Execute all SELECT/CTE statements contained in
    an analysis SQL file.
    """
    statements = split_sql_statements(
        sql
    )

    results: list[pd.DataFrame] = []

    for statement in statements:
        result = execute_query(
            connection,
            statement,
        )

        results.append(result)

    return results