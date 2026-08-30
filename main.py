from ecommerce_analysis.config import RAW_DATA_PATH
from ecommerce_analysis.data_loader import (
    fetch_online_retail,
    load_raw_data,
    save_raw_data,
)


def main() -> None:
    if RAW_DATA_PATH.exists():
        print("Loading dataset from local file...")

        df = load_raw_data(
            RAW_DATA_PATH
        )

    else:
        print("Fetching dataset from UCI...")

        df = fetch_online_retail()

        save_raw_data(
            df,
            RAW_DATA_PATH,
        )

    print(df.head())
    print()
    print(f"Shape: {df.shape}")


if __name__ == "__main__":
    main()