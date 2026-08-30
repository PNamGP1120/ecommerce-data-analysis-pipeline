from __future__ import annotations

import math

from ecommerce_analysis.analysis import (
    calculate_total_revenue,
)
from ecommerce_analysis.analytical_views import (
    get_anomalies,
    get_cancellations,
    get_customer_sales,
    get_valid_sales,
)
from ecommerce_analysis.config import (
    DATABASE_PATH,
    PROCESSED_DATA_PATH,
)
from ecommerce_analysis.data_loader import (
    load_processed_data,
)
from ecommerce_analysis.database import (
    build_database,
)


def validate_database_against_pandas(
    df,
    summary: dict[str, int | float],
) -> None:
    """
    Cross-check SQLite results against the Pandas
    analytical definitions.
    """
    valid_sales = get_valid_sales(
        df
    )

    customer_sales = get_customer_sales(
        df
    )

    cancellations = get_cancellations(
        df
    )

    anomalies = get_anomalies(
        df
    )

    expected_counts = {
        "transactions": len(df),
        "valid_sales": len(
            valid_sales
        ),
        "customer_sales": len(
            customer_sales
        ),
        "cancellations": len(
            cancellations
        ),
        "anomalies": len(
            anomalies
        ),
    }

    for name, expected in (
        expected_counts.items()
    ):
        actual = int(
            summary[name]
        )

        if actual != expected:
            raise ValueError(
                f"SQLite/Pandas mismatch "
                f"for {name}: "
                f"SQLite={actual:,}, "
                f"Pandas={expected:,}"
            )

    pandas_revenue = (
        calculate_total_revenue(
            valid_sales
        )
    )

    sqlite_revenue = float(
        summary["total_revenue"]
    )

    if not math.isclose(
        pandas_revenue,
        sqlite_revenue,
        rel_tol=1e-9,
        abs_tol=1e-6,
    ):
        raise ValueError(
            "SQLite/Pandas revenue mismatch: "
            f"SQLite={sqlite_revenue}, "
            f"Pandas={pandas_revenue}"
        )


def main() -> None:
    print(
        f"[database] Loading processed data: "
        f"{PROCESSED_DATA_PATH}"
    )

    df = load_processed_data(
        PROCESSED_DATA_PATH
    )

    print(
        f"[database] Input shape: "
        f"{df.shape}"
    )

    print(
        f"[database] Building SQLite database: "
        f"{DATABASE_PATH}"
    )

    summary = build_database(
        df,
        DATABASE_PATH,
    )

    # ---------------------------------------
    # Pandas vs SQL validation
    # ---------------------------------------
    validate_database_against_pandas(
        df,
        summary,
    )

    print(
        "[database] SQLite/Pandas "
        "validation passed."
    )

    # ---------------------------------------
    # Summary
    # ---------------------------------------
    print()
    print("Database Summary")
    print("=" * 60)

    print(
        f"Transactions   : "
        f"{int(summary['transactions']):,}"
    )

    print(
        f"Customers      : "
        f"{int(summary['customers']):,}"
    )

    print(
        f"Products       : "
        f"{int(summary['products']):,}"
    )

    print(
        f"Valid sales    : "
        f"{int(summary['valid_sales']):,}"
    )

    print(
        f"Customer sales : "
        f"{int(summary['customer_sales']):,}"
    )

    print(
        f"Cancellations  : "
        f"{int(summary['cancellations']):,}"
    )

    print(
        f"Anomalies      : "
        f"{int(summary['anomalies']):,}"
    )

    print(
        f"Total revenue  : "
        f"£{float(summary['total_revenue']):,.2f}"
    )

    print("=" * 60)

    print()
    print(
        f"[database] Saved database: "
        f"{DATABASE_PATH}"
    )

    print(
        "[database] Database stage "
        "completed successfully."
    )


if __name__ == "__main__":
    main()