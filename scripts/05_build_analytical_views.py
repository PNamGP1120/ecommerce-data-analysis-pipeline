from ecommerce_analysis.analytical_views import (
    get_anomalies,
    get_cancellations,
    get_customer_sales,
    get_valid_sales,
)
from ecommerce_analysis.config import (
    PROCESSED_DATA_PATH,
)
from ecommerce_analysis.data_loader import (
    load_processed_data,
)


def main() -> None:
    print(
        f"[views] Loading processed data: "
        f"{PROCESSED_DATA_PATH}"
    )

    df = load_processed_data(
        PROCESSED_DATA_PATH
    )

    valid_sales = get_valid_sales(df)
    customer_sales = get_customer_sales(df)
    cancellations = get_cancellations(df)
    anomalies = get_anomalies(df)

    print()
    print("Analytical Views Summary")
    print("=" * 50)

    print(
        f"All transactions : {len(df):,}"
    )

    print(
        f"Valid sales      : {len(valid_sales):,}"
    )

    print(
        f"Customer sales   : {len(customer_sales):,}"
    )

    print(
        f"Cancellations    : {len(cancellations):,}"
    )

    print(
        f"Anomalies        : {len(anomalies):,}"
    )

    print("=" * 50)


if __name__ == "__main__":
    main()