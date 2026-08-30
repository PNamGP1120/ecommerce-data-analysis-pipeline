from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

DATABASE_DIR = BASE_DIR / "database"

REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

RAW_DATA_PATH = RAW_DATA_DIR / "online_retail.csv"

PROCESSED_DATA_PATH = (
    PROCESSED_DATA_DIR
    / "transactions_processed.csv"
)

DATABASE_PATH = (
    DATABASE_DIR
    / "ecommerce.db"
)

INTERIM_DATA_PATH = (
    INTERIM_DATA_DIR
    / "transactions_cleaned.csv"
)

