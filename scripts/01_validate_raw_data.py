from __future__ import annotations

from ecommerce_analysis.config import RAW_DATA_PATH
from ecommerce_analysis.data_loader import load_raw_data
from ecommerce_analysis.data_validator import validate_data


def main() -> None:
    print(f"[validate] Loading raw data: {RAW_DATA_PATH}")

    df = load_raw_data(RAW_DATA_PATH)
    validate_data(df)

    print("[validate] Structural validation passed.")
    print(f"[validate] Shape: {df.shape}")


if __name__ == "__main__":
    main()
