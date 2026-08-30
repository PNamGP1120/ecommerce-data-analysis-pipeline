from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parents[1]
)

RAW_DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "online_retail.csv"
)


PIPELINE_STAGES = [
    "scripts/01_validate_raw_data.py",
    "scripts/02_data_quality_report.py",
    "scripts/03_clean_data.py",
    "scripts/04_build_features.py",
    "scripts/05_build_analytical_views.py",
    "scripts/06_run_analysis.py",
    "scripts/07_build_database.py",
    "scripts/08_run_sql_analysis.py",
    "scripts/09_generate_figures.py",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the complete E-commerce "
            "Data Analysis Pipeline."
        )
    )

    parser.add_argument(
        "--fetch",
        action="store_true",
        help=(
            "Fetch the raw UCI dataset "
            "even if a local copy already exists."
        ),
    )

    parser.add_argument(
        "--test",
        action="store_true",
        help=(
            "Run the complete pytest suite "
            "after the pipeline completes."
        ),
    )

    return parser.parse_args()


def run_command(
    command: list[str],
    label: str,
) -> None:
    print()
    print("=" * 75)
    print(label)
    print("=" * 75)

    subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        check=True,
    )


def run_script(
    relative_path: str,
) -> None:
    script_path = (
        PROJECT_ROOT
        / relative_path
    )

    if not script_path.exists():
        raise FileNotFoundError(
            f"Pipeline script not found: "
            f"{script_path}"
        )

    run_command(
        [
            sys.executable,
            str(script_path),
        ],
        label=f"Running {relative_path}",
    )


def main() -> None:
    args = parse_args()

    print()
    print(
        "E-COMMERCE DATA ANALYSIS PIPELINE"
    )
    print("=" * 75)

    # --------------------------------------------------
    # Raw data
    # --------------------------------------------------
    should_fetch = (
        args.fetch
        or not RAW_DATA_PATH.exists()
    )

    if should_fetch:
        run_script(
            "scripts/00_fetch_raw_data.py"
        )
    else:
        print()
        print(
            "[pipeline] Using existing raw dataset:"
        )
        print(
            f"[pipeline] {RAW_DATA_PATH}"
        )

    # --------------------------------------------------
    # Pipeline stages
    # --------------------------------------------------
    for stage in PIPELINE_STAGES:
        run_script(stage)

    # --------------------------------------------------
    # Optional test suite
    # --------------------------------------------------
    if args.test:
        run_command(
            [
                sys.executable,
                "-m",
                "pytest",
                "-v",
            ],
            label="Running test suite",
        )

    print()
    print("=" * 75)
    print(
        "[pipeline] Full pipeline completed "
        "successfully."
    )
    print("=" * 75)


if __name__ == "__main__":
    main()