from __future__ import annotations

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

from ecommerce_analysis.analysis import (
    calculate_monthly_growth,
    calculate_monthly_revenue,
    orders_by_hour,
    orders_by_weekday,
    top_cancelled_products,
    top_customers_by_spending,
    top_international_markets,
    top_products_by_revenue,
)
from ecommerce_analysis.analytical_views import (
    get_cancellations,
    get_customer_sales,
    get_valid_sales,
)
from ecommerce_analysis.config import (
    FIGURES_DIR,
    PROCESSED_DATA_PATH,
)
from ecommerce_analysis.data_loader import (
    load_processed_data,
)
from ecommerce_analysis.visualization import (
    plot_monthly_growth,
    plot_monthly_revenue,
    plot_orders_by_hour,
    plot_orders_by_weekday,
    plot_top_cancelled_products,
    plot_top_customers,
    plot_top_international_markets,
    plot_top_products_by_revenue,
    save_figure,
)


def save_and_close(
    fig,
    filename: str,
) -> None:
    path = (
        FIGURES_DIR
        / filename
    )

    save_figure(
        fig,
        path,
    )

    plt.close(fig)

    print(
        f"[figures] Saved: {path}"
    )


def main() -> None:
    print(
        f"[figures] Loading processed data: "
        f"{PROCESSED_DATA_PATH}"
    )

    df = load_processed_data(
        PROCESSED_DATA_PATH
    )

    sales = get_valid_sales(
        df
    )

    customer_sales = get_customer_sales(
        df
    )

    cancellations = get_cancellations(
        df
    )

    FIGURES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------
    # 01 Monthly revenue
    # --------------------------------------------------
    monthly_revenue = (
        calculate_monthly_revenue(
            sales
        )
    )

    fig = plot_monthly_revenue(
        monthly_revenue
    )

    save_and_close(
        fig,
        "01_monthly_revenue.png",
    )

    # --------------------------------------------------
    # 02 Monthly growth
    # --------------------------------------------------
    monthly_growth = (
        calculate_monthly_growth(
            sales
        )
    )

    fig = plot_monthly_growth(
        monthly_growth
    )

    save_and_close(
        fig,
        "02_monthly_growth.png",
    )

    # --------------------------------------------------
    # 03 Products / StockCode-Description pairs
    # --------------------------------------------------
    top_products = (
        top_products_by_revenue(
            sales,
            n=10,
        )
    )

    fig = (
        plot_top_products_by_revenue(
            top_products
        )
    )

    save_and_close(
        fig,
        "03_top_products_revenue.png",
    )

    # --------------------------------------------------
    # 04 International markets
    # --------------------------------------------------
    international_markets = (
        top_international_markets(
            sales,
            exclude_country=(
                "United Kingdom"
            ),
            n=10,
        )
    )

    fig = (
        plot_top_international_markets(
            international_markets
        )
    )

    save_and_close(
        fig,
        "04_top_international_markets.png",
    )

    # --------------------------------------------------
    # 05 Customers
    # --------------------------------------------------
    top_customers = (
        top_customers_by_spending(
            customer_sales,
            n=10,
        )
    )

    fig = plot_top_customers(
        top_customers
    )

    save_and_close(
        fig,
        "05_top_customers.png",
    )

    # --------------------------------------------------
    # 06 Weekday
    # --------------------------------------------------
    weekday_orders = (
        orders_by_weekday(
            sales
        )
    )

    fig = plot_orders_by_weekday(
        weekday_orders
    )

    save_and_close(
        fig,
        "06_orders_by_weekday.png",
    )

    # --------------------------------------------------
    # 07 Hour
    # --------------------------------------------------
    hourly_orders = (
        orders_by_hour(
            sales
        )
    )

    fig = plot_orders_by_hour(
        hourly_orders
    )

    save_and_close(
        fig,
        "07_orders_by_hour.png",
    )

    # --------------------------------------------------
    # 08 Cancellations
    # --------------------------------------------------
    cancelled_products = (
        top_cancelled_products(
            cancellations,
            n=10,
        )
    )

    fig = (
        plot_top_cancelled_products(
            cancelled_products
        )
    )

    save_and_close(
        fig,
        "08_top_cancelled_products.png",
    )

    print()
    print(
        "[figures] Visualization stage "
        "completed successfully."
    )


if __name__ == "__main__":
    main()