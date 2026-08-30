from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure


def save_figure(
    fig: Figure,
    path: Path,
) -> None:
    """
    Save a Matplotlib figure to disk.
    """
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fig.savefig(
        path,
        dpi=150,
        bbox_inches="tight",
    )


def plot_monthly_revenue(
    data: pd.DataFrame,
) -> Figure:
    """
    Plot monthly sales revenue.
    """
    fig, ax = plt.subplots(
        figsize=(11, 6)
    )

    ax.plot(
        data["YearMonth"],
        data["Revenue"],
        marker="o",
    )

    ax.set_title(
        "Monthly Sales Revenue"
    )

    ax.set_xlabel(
        "Month"
    )

    ax.set_ylabel(
        "Revenue (£)"
    )

    ax.tick_params(
        axis="x",
        rotation=45,
    )

    ax.grid(
        axis="y",
        alpha=0.3,
    )

    fig.tight_layout()

    return fig


def plot_monthly_growth(
    data: pd.DataFrame,
) -> Figure:
    """
    Plot month-over-month revenue growth.
    """
    fig, ax = plt.subplots(
        figsize=(11, 6)
    )

    ax.bar(
        data["YearMonth"],
        data["GrowthPercent"],
    )

    ax.axhline(
        0,
        linewidth=1,
    )

    ax.set_title(
        "Month-over-Month Revenue Growth"
    )

    ax.set_xlabel(
        "Month"
    )

    ax.set_ylabel(
        "Growth (%)"
    )

    ax.tick_params(
        axis="x",
        rotation=45,
    )

    ax.grid(
        axis="y",
        alpha=0.3,
    )

    fig.tight_layout()

    return fig


def plot_top_products_by_revenue(
    data: pd.DataFrame,
) -> Figure:
    """
    Plot top StockCode-Description pairs by revenue.

    The dataset may contain non-merchandise codes such as
    postage and manual adjustments, so the chart deliberately
    avoids claiming that every row represents merchandise.
    """
    plot_data = (
        data.sort_values(
            "Revenue",
            ascending=True,
        )
        .copy()
    )

    labels = (
        plot_data["Description"]
        .fillna(
            plot_data["StockCode"]
        )
    )

    fig, ax = plt.subplots(
        figsize=(11, 7)
    )

    ax.barh(
        labels,
        plot_data["Revenue"],
    )

    ax.set_title(
        "Top StockCode–Description Pairs by Revenue"
    )

    ax.set_xlabel(
        "Revenue (£)"
    )

    ax.set_ylabel(
        ""
    )

    ax.grid(
        axis="x",
        alpha=0.3,
    )

    fig.tight_layout()

    return fig


def plot_top_international_markets(
    data: pd.DataFrame,
) -> Figure:
    """
    Plot top international markets excluding the UK.
    """
    plot_data = (
        data.sort_values(
            "Revenue",
            ascending=True,
        )
        .copy()
    )

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    ax.barh(
        plot_data["Country"],
        plot_data["Revenue"],
    )

    ax.set_title(
        "Top International Markets by Revenue"
    )

    ax.set_xlabel(
        "Revenue (£)"
    )

    ax.set_ylabel(
        ""
    )

    ax.grid(
        axis="x",
        alpha=0.3,
    )

    fig.tight_layout()

    return fig


def plot_top_customers(
    data: pd.DataFrame,
) -> Figure:
    """
    Plot highest-value customers by total revenue.
    """
    plot_data = (
        data.sort_values(
            "Revenue",
            ascending=True,
        )
        .copy()
    )

    labels = (
        plot_data["CustomerID"]
        .astype("Int64")
        .astype("string")
    )

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    ax.barh(
        labels,
        plot_data["Revenue"],
    )

    ax.set_title(
        "Top Customers by Spending"
    )

    ax.set_xlabel(
        "Revenue (£)"
    )

    ax.set_ylabel(
        "Customer ID"
    )

    ax.grid(
        axis="x",
        alpha=0.3,
    )

    fig.tight_layout()

    return fig


def plot_orders_by_weekday(
    data: pd.DataFrame,
) -> Figure:
    """
    Plot unique orders by weekday.
    """
    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    plot_data = (
        data.set_index(
            "DayOfWeek"
        )
        .reindex(
            weekday_order,
            fill_value=0,
        )
        .reset_index()
    )

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    ax.bar(
        plot_data["DayOfWeek"],
        plot_data["Orders"],
    )

    ax.set_title(
        "Orders by Day of Week"
    )

    ax.set_xlabel(
        "Day"
    )

    ax.set_ylabel(
        "Unique Orders"
    )

    ax.tick_params(
        axis="x",
        rotation=30,
    )

    ax.grid(
        axis="y",
        alpha=0.3,
    )

    fig.tight_layout()

    return fig


def plot_orders_by_hour(
    data: pd.DataFrame,
) -> Figure:
    """
    Plot unique orders by hour of day.
    """
    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    ax.plot(
        data["Hour"],
        data["Orders"],
        marker="o",
    )

    ax.set_title(
        "Orders by Hour of Day"
    )

    ax.set_xlabel(
        "Hour"
    )

    ax.set_ylabel(
        "Unique Orders"
    )

    ax.set_xticks(
        data["Hour"]
    )

    ax.grid(
        alpha=0.3,
    )

    fig.tight_layout()

    return fig


def plot_top_cancelled_products(
    data: pd.DataFrame,
) -> Figure:
    """
    Plot StockCode-Description pairs with the highest
    cancelled quantities.
    """
    plot_data = (
        data.sort_values(
            "CancelledQuantity",
            ascending=True,
        )
        .copy()
    )

    labels = (
        plot_data["Description"]
        .fillna(
            plot_data["StockCode"]
        )
    )

    fig, ax = plt.subplots(
        figsize=(11, 7)
    )

    ax.barh(
        labels,
        plot_data[
            "CancelledQuantity"
        ],
    )

    ax.set_title(
        "Top Cancelled StockCode–Description Pairs"
    )

    ax.set_xlabel(
        "Cancelled Quantity"
    )

    ax.set_ylabel(
        ""
    )

    ax.grid(
        axis="x",
        alpha=0.3,
    )

    fig.tight_layout()

    return fig