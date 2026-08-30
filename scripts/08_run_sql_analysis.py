from __future__ import annotations

import sqlite3
from pathlib import Path

from ecommerce_analysis.config import (
    BASE_DIR,
    DATABASE_PATH,
)
from ecommerce_analysis.sql_analysis import (
    execute_sql_script_queries,
    load_sql_file,
)


SQL_DIR = (
    BASE_DIR
    / "sql"
)


SQL_FILES = [
    "01_sales_overview.sql",
    "02_product_analysis.sql",
    "03_customer_analysis.sql",
    "04_market_analysis.sql",
    "05_time_analysis.sql",
    "06_cancellation_analysis.sql",
]


def print_result(
    result,
    number: int,
) -> None:
    print()
    print(
        f"Query {number}"
    )
    print("-" * 70)

    print(
        result.to_string(
            index=False
        )
    )


def run_sql_file(
    connection: sqlite3.Connection,
    path: Path,
) -> None:
    print()
    print("=" * 70)
    print(
        f"SQL Analysis: {path.name}"
    )
    print("=" * 70)

    sql = load_sql_file(
        path
    )

    results = (
        execute_sql_script_queries(
            connection,
            sql,
        )
    )

    for index, result in enumerate(
        results,
        start=1,
    ):
        print_result(
            result,
            index,
        )


def main() -> None:
    print(
        f"[sql] Opening database: "
        f"{DATABASE_PATH}"
    )

    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            "Database does not exist. "
            "Run scripts/07_build_database.py first."
        )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    try:
        for filename in SQL_FILES:
            run_sql_file(
                connection,
                SQL_DIR / filename,
            )

    finally:
        connection.close()

    print()
    print(
        "[sql] SQL analysis "
        "completed successfully."
    )


if __name__ == "__main__":
    main()