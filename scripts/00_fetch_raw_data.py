from __future__ import annotations

from ecommerce_analysis.config import RAW_DATA_PATH
from ecommerce_analysis.data_loader import (
    fetch_online_retail,
    save_csv,
)


def main() -> None:
    print(
        "[fetch] Fetching Online Retail "
        "dataset from UCI..."
    )

    df = fetch_online_retail()

    save_csv(
        df,
        RAW_DATA_PATH,
    )

    print(
        f"[fetch] Saved {len(df):,} rows "
        f"to {RAW_DATA_PATH}"
    )


if __name__ == "__main__":
    main()