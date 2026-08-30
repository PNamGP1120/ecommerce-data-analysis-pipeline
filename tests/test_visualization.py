from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

from ecommerce_analysis.visualization import (
    plot_monthly_revenue,
    plot_orders_by_hour,
    plot_orders_by_weekday,
    plot_top_customers,
    save_figure,
)


def test_plot_monthly_revenue_returns_figure() -> None:
    df = pd.DataFrame(
        {
            "YearMonth": [
                "2011-01",
                "2011-02",
            ],
            "Revenue": [
                100.0,
                150.0,
            ],
        }
    )

    fig = plot_monthly_revenue(
        df
    )

    assert isinstance(
        fig,
        Figure,
    )

    plt.close(fig)


def test_plot_orders_by_hour_returns_figure() -> None:
    df = pd.DataFrame(
        {
            "Hour": [
                10,
                11,
                12,
            ],
            "Orders": [
                5,
                10,
                15,
            ],
        }
    )

    fig = plot_orders_by_hour(
        df
    )

    assert isinstance(
        fig,
        Figure,
    )

    plt.close(fig)


def test_plot_orders_by_weekday_handles_missing_days() -> None:
    df = pd.DataFrame(
        {
            "DayOfWeek": [
                "Monday",
                "Sunday",
            ],
            "Orders": [
                10,
                5,
            ],
        }
    )

    fig = plot_orders_by_weekday(
        df
    )

    assert isinstance(
        fig,
        Figure,
    )

    plt.close(fig)


def test_plot_top_customers_returns_figure() -> None:
    df = pd.DataFrame(
        {
            "CustomerID": pd.Series(
                [
                    1001,
                    1002,
                ],
                dtype="Int64",
            ),
            "Revenue": [
                100.0,
                200.0,
            ],
        }
    )

    fig = plot_top_customers(
        df
    )

    assert isinstance(
        fig,
        Figure,
    )

    plt.close(fig)


def test_save_figure_creates_file(
    tmp_path: Path,
) -> None:
    df = pd.DataFrame(
        {
            "YearMonth": [
                "2011-01",
                "2011-02",
            ],
            "Revenue": [
                100.0,
                200.0,
            ],
        }
    )

    fig = plot_monthly_revenue(
        df
    )

    output_path = (
        tmp_path
        / "figure.png"
    )

    save_figure(
        fig,
        output_path,
    )

    assert output_path.exists()
    assert output_path.stat().st_size > 0

    plt.close(fig)