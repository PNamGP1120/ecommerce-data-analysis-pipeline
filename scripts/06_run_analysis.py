from __future__ import annotations

from ecommerce_analysis.analysis import (
    average_revenue_per_customer,
    calculate_average_order_value,
    calculate_cancellation_rate,
    calculate_monthly_revenue,
    calculate_total_orders,
    calculate_total_revenue,
    investigate_business_data,
    orders_by_hour,
    orders_by_weekday,
    revenue_by_country,
    revenue_by_weekday,
    top_cancelled_products,
    top_customers_by_orders,
    top_customers_by_spending,
    top_products_by_quantity,
    top_products_by_revenue,
)
from ecommerce_analysis.analytical_views import (
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


def print_section(
    title: str,
    width: int = 70,
) -> None:
    print()
    print(title)
    print("=" * width)


def main() -> None:
    print(
        f"[analysis] Loading processed data: "
        f"{PROCESSED_DATA_PATH}"
    )

    # --------------------------------------------------
    # Load processed dataset
    # --------------------------------------------------
    df = load_processed_data(
        PROCESSED_DATA_PATH
    )

    # --------------------------------------------------
    # Build analytical views
    # --------------------------------------------------
    sales = get_valid_sales(df)

    customer_sales = get_customer_sales(
        df
    )

    cancellations = get_cancellations(
        df
    )

    # --------------------------------------------------
    # Sales overview
    # --------------------------------------------------
    total_revenue = calculate_total_revenue(
        sales
    )

    total_orders = calculate_total_orders(
        sales
    )

    average_order_value = (
        calculate_average_order_value(
            sales
        )
    )

    avg_revenue_customer = (
        average_revenue_per_customer(
            customer_sales
        )
    )

    cancellation_rate = (
        calculate_cancellation_rate(
            df,
            cancellations,
        )
    )

    print_section(
        "Sales Overview"
    )

    print(
        f"All transaction rows       : "
        f"{len(df):,}"
    )

    print(
        f"Valid sales rows           : "
        f"{len(sales):,}"
    )

    print(
        f"Customer sales rows        : "
        f"{len(customer_sales):,}"
    )

    print(
        f"Cancellation rows          : "
        f"{len(cancellations):,}"
    )

    print(
        f"Total revenue              : "
        f"£{total_revenue:,.2f}"
    )

    print(
        f"Valid orders               : "
        f"{total_orders:,}"
    )

    print(
        f"Average Order Value        : "
        f"£{average_order_value:,.2f}"
    )

    print(
        f"Average revenue/customer   : "
        f"£{avg_revenue_customer:,.2f}"
    )

    print(
        f"Invoice cancellation share : "
        f"{cancellation_rate:.2%}"
    )

    # --------------------------------------------------
    # Monthly revenue
    # --------------------------------------------------
    print_section(
        "Monthly Revenue"
    )

    monthly_revenue = (
        calculate_monthly_revenue(
            sales
        )
    )

    print(
        monthly_revenue.to_string(
            index=False
        )
    )

    # --------------------------------------------------
    # Product analysis
    # --------------------------------------------------
    print_section(
        "Top 10 Products by Revenue"
    )

    print(
        top_products_by_revenue(
            sales,
            n=10,
        ).to_string(
            index=False
        )
    )

    print_section(
        "Top 10 Products by Quantity"
    )

    print(
        top_products_by_quantity(
            sales,
            n=10,
        ).to_string(
            index=False
        )
    )

    # --------------------------------------------------
    # Country analysis
    # --------------------------------------------------
    print_section(
        "Top Countries by Revenue"
    )

    print(
        revenue_by_country(
            sales
        )
        .head(10)
        .to_string(
            index=False
        )
    )

    # --------------------------------------------------
    # Customer analysis
    # --------------------------------------------------
    print_section(
        "Top Customers by Spending"
    )

    print(
        top_customers_by_spending(
            customer_sales,
            n=10,
        ).to_string(
            index=False
        )
    )

    print_section(
        "Top Customers by Orders"
    )

    print(
        top_customers_by_orders(
            customer_sales,
            n=10,
        ).to_string(
            index=False
        )
    )

    # --------------------------------------------------
    # Time analysis
    # --------------------------------------------------
    print_section(
        "Orders by Weekday"
    )

    print(
        orders_by_weekday(
            sales
        ).to_string(
            index=False
        )
    )

    print_section(
        "Revenue by Weekday"
    )

    print(
        revenue_by_weekday(
            sales
        ).to_string(
            index=False
        )
    )

    print_section(
        "Orders by Hour"
    )

    print(
        orders_by_hour(
            sales
        ).to_string(
            index=False
        )
    )

    # --------------------------------------------------
    # Cancellation analysis
    # --------------------------------------------------
    print_section(
        "Top Cancelled Products"
    )

    print(
        top_cancelled_products(
            cancellations,
            n=10,
        ).to_string(
            index=False
        )
    )

    # --------------------------------------------------
    # Business investigation
    # --------------------------------------------------
    investigation = (
        investigate_business_data(
            sales
        )
    )

    print_section(
        "Special StockCodes"
    )

    print(
        investigation[
            "special_stock_codes"
        ]
        .head(20)
        .to_string(
            index=False
        )
    )

    print_section(
        "Top Quantity Outliers"
    )

    print(
        investigation[
            "quantity_outliers"
        ].to_string(
            index=False
        )
    )

    print_section(
        "Top Revenue Outliers"
    )

    print(
        investigation[
            "revenue_outliers"
        ].to_string(
            index=False
        )
    )

    print_section(
        "Revenue Concentration"
    )

    uk_share = investigation[
        "uk_revenue_share"
    ]

    print(
        "United Kingdom revenue share: "
        f"{uk_share:.2%}"
    )

    print_section(
        "Top International Markets"
    )

    print(
        investigation[
            "international_markets"
        ].to_string(
            index=False
        )
    )

    # --------------------------------------------------
    # Duplicate sensitivity
    # --------------------------------------------------
    print_section(
        "Duplicate Sensitivity"
    )

    duplicate_summary = (
        investigation[
            "duplicate_sensitivity"
        ]
    )

    print(
        duplicate_summary.to_string(
            index=False
        )
    )

    difference_row = (
        duplicate_summary.loc[
            duplicate_summary["metric"]
            == "difference_percent",
            "value",
        ]
    )

    if not difference_row.empty:
        difference_percent = float(
            difference_row.iloc[0]
        )

        print()
        print(
            "Potential revenue affected by "
            "duplicate groups: "
            f"{difference_percent:.2%}"
        )

    print()
    print(
        "[analysis] Business analysis "
        "completed successfully."
    )


if __name__ == "__main__":
    main()