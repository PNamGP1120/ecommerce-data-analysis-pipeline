from __future__ import annotations

import subprocess
import sys


STAGES = [
    "scripts/03_clean_data.py",
    "scripts/04_build_features.py",
]


def run_script(
    path: str,
) -> None:
    print(
        f"\n>>> Running {path}"
    )

    subprocess.run(
        [
            sys.executable,
            path,
        ],
        check=True,
    )


def main() -> None:
    for stage in STAGES:
        run_script(stage)

    print(
        "\nFeature engineering "
        "stage completed."
    )


if __name__ == "__main__":
    main()