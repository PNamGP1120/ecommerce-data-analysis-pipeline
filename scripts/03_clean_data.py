from __future__ import annotations

from ecommerce_analysis.config import (
    INTERIM_DATA_PATH,
    RAW_DATA_PATH,
)
from ecommerce_analysis.data_cleaner import (
    build_cleaning_summary,
    clean_data,
)
from ecommerce_analysis.data_loader import (
    load_raw_data,
    save_csv,
)
from ecommerce_analysis.data_validator import (
    validate_data,
)


def validate_cleaning_result(
    raw_rows: int,
    raw_columns: set[str],
    cleaned_df,
) -> None:
    """
    Validate important invariants after cleaning.

    The current cleaning policy is:
    normalize + flag + preserve.

    Therefore:
    - row count must not change;
    - original columns must still exist;
    - InvoiceDate must be valid after conversion.
    """
    if len(cleaned_df) != raw_rows:
        raise ValueError(
            "Cleaning unexpectedly changed row count. "
            f"Before: {raw_rows:,}, "
            f"After: {len(cleaned_df):,}"
        )

    missing_source_columns = (
        raw_columns
        - set(cleaned_df.columns)
    )

    if missing_source_columns:
        raise ValueError(
            "Cleaning removed source columns: "
            f"{sorted(missing_source_columns)}"
        )

    if cleaned_df["InvoiceDate"].isna().any():
        invalid_count = (
            cleaned_df["InvoiceDate"]
            .isna()
            .sum()
        )

        raise ValueError(
            "Invalid InvoiceDate values found "
            f"after cleaning: {invalid_count}"
        )


def main() -> None:
    print(
        f"[clean] Loading raw data: "
        f"{RAW_DATA_PATH}"
    )

    # -------------------------------------------------
    # 1. Load raw dataset
    # -------------------------------------------------
    raw_df = load_raw_data(
        RAW_DATA_PATH
    )

    print(
        f"[clean] Raw shape: "
        f"{raw_df.shape}"
    )

    # -------------------------------------------------
    # 2. Structural validation
    # -------------------------------------------------
    validate_data(raw_df)

    print(
        "[clean] Structural validation passed."
    )

    # Save invariants before cleaning
    raw_rows = len(raw_df)
    raw_columns = set(raw_df.columns)

    # -------------------------------------------------
    # 3. Cleaning
    # -------------------------------------------------
    cleaned_df = clean_data(
        raw_df
    )

    # -------------------------------------------------
    # 4. Validate cleaning result
    # -------------------------------------------------
    validate_cleaning_result(
        raw_rows=raw_rows,
        raw_columns=raw_columns,
        cleaned_df=cleaned_df,
    )

    print(
        "[clean] Cleaning result validation passed."
    )

    # -------------------------------------------------
    # 5. Build cleaning summary
    # -------------------------------------------------
    summary = build_cleaning_summary(
        cleaned_df
    )

    print()
    print("Cleaning Summary")
    print("=" * 55)
    print(
        summary.to_string(
            index=False
        )
    )
    print("=" * 55)

    # -------------------------------------------------
    # 6. Save interim dataset
    # -------------------------------------------------
    save_csv(
        cleaned_df,
        INTERIM_DATA_PATH,
    )

    print()
    print(
        f"[clean] Cleaned shape: "
        f"{cleaned_df.shape}"
    )

    print(
        f"[clean] Saved cleaned data: "
        f"{INTERIM_DATA_PATH}"
    )

    print(
        "[clean] Cleaning stage completed successfully."
    )


if __name__ == "__main__":
    main()