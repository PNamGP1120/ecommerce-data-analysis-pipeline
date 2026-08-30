from __future__ import annotations

from ecommerce_analysis.config import (
    INTERIM_DATA_PATH,
    PROCESSED_DATA_PATH,
)
from ecommerce_analysis.data_loader import (
    load_interim_data,
    save_csv,
)
from ecommerce_analysis.feature_engineering import (
    build_features,
)


def main() -> None:
    print(
        f"[features] Loading interim data: "
        f"{INTERIM_DATA_PATH}"
    )

    cleaned_df = load_interim_data(
        INTERIM_DATA_PATH
    )

    print(
        f"[features] Input shape: "
        f"{cleaned_df.shape}"
    )

    processed_df = build_features(
        cleaned_df
    )

    if len(processed_df) != len(cleaned_df):
        raise ValueError(
            "Feature engineering changed row count."
        )

    save_csv(
        processed_df,
        PROCESSED_DATA_PATH,
    )

    print(
        f"[features] Output shape: "
        f"{processed_df.shape}"
    )

    print(
        f"[features] Saved processed data: "
        f"{PROCESSED_DATA_PATH}"
    )

    print(
        "[features] Feature engineering "
        "completed successfully."
    )


if __name__ == "__main__":
    main()