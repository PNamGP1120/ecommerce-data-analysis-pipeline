# ============================================================
# E-commerce Data Analysis Pipeline
# ============================================================

SHELL := /bin/bash

PYTHON := uv run python
PYTEST := uv run pytest

RAW_DATA := data/raw/online_retail.csv
INTERIM_DATA := data/interim/transactions_cleaned.csv
PROCESSED_DATA := data/processed/transactions_processed.csv
DATABASE := database/ecommerce.db

FIGURES_DIR := reports/figures


# ============================================================
# Default target
# ============================================================

.DEFAULT_GOAL := help


# ============================================================
# Phony targets
# ============================================================

.PHONY: \
	help \
	setup \
	sync \
	fetch \
	validate \
	quality \
	understand \
	clean \
	features \
	views \
	analysis \
	database \
	sql \
	figures \
	test \
	test-short \
	pipeline \
	pipeline-test \
	pipeline-fetch \
	rebuild \
	check \
	clean-cache \
	clean-interim \
	clean-processed \
	clean-database \
	clean-figures \
	clean-generated \
	clean \
	status \
	tree


# ============================================================
# Help
# ============================================================

help:
	@echo ""
	@echo "E-COMMERCE DATA ANALYSIS PIPELINE"
	@echo "============================================================"
	@echo ""
	@echo "Environment"
	@echo "  make setup              Install/sync project dependencies"
	@echo "  make sync               Alias for setup"
	@echo ""
	@echo "Data pipeline"
	@echo "  make fetch              Fetch raw UCI dataset"
	@echo "  make validate           Validate raw dataset structure"
	@echo "  make quality            Generate raw data-quality report"
	@echo "  make understand         Run dataset-understanding stage"
	@echo "  make clean              Run data cleaning"
	@echo "  make features           Run feature engineering"
	@echo "  make views              Build analytical views summary"
	@echo "  make analysis           Run Pandas business analysis"
	@echo "  make database           Build SQLite database"
	@echo "  make sql                Run SQL analysis"
	@echo "  make figures            Generate report figures"
	@echo ""
	@echo "Full pipeline"
	@echo "  make pipeline           Run full pipeline"
	@echo "  make pipeline-test      Run full pipeline + pytest"
	@echo "  make pipeline-fetch     Fetch raw data + run full pipeline"
	@echo "  make rebuild            Rebuild generated artifacts"
	@echo ""
	@echo "Testing"
	@echo "  make test               Run pytest with verbose output"
	@echo "  make test-short         Run pytest with compact output"
	@echo "  make check              Run tests after pipeline"
	@echo ""
	@echo "Cleanup"
	@echo "  make clean-cache        Remove Python/pytest caches"
	@echo "  make clean-interim      Remove interim dataset"
	@echo "  make clean-processed    Remove processed dataset"
	@echo "  make clean-database     Remove SQLite database"
	@echo "  make clean-figures      Remove generated figures"
	@echo "  make clean-generated    Remove all generated artifacts"
	@echo ""
	@echo "Utilities"
	@echo "  make status             Show Git status"
	@echo "  make tree               Show project tree"
	@echo ""


# ============================================================
# Environment
# ============================================================

setup:
	@echo "[make] Syncing Python environment..."
	uv sync


sync: setup


# ============================================================
# Milestone 02 — Dataset Understanding
# ============================================================

fetch:
	@echo "[make] Fetching raw dataset..."
	$(PYTHON) scripts/00_fetch_raw_data.py


validate:
	@echo "[make] Validating raw dataset..."
	$(PYTHON) scripts/01_validate_raw_data.py


quality:
	@echo "[make] Generating data-quality report..."
	$(PYTHON) scripts/02_data_quality_report.py


understand:
	@echo "[make] Running dataset-understanding stage..."
	$(PYTHON) scripts/run_dataset_understanding_stage.py


# ============================================================
# Milestone 03 — Cleaning
# ============================================================

clean:
	@echo "[make] Running cleaning stage..."
	$(PYTHON) scripts/03_clean_data.py


# Optional existing stage runner
clean-stage:
	@echo "[make] Running complete cleaning stage..."
	$(PYTHON) scripts/run_cleaning_stage.py


# ============================================================
# Milestone 04 — Feature Engineering
# ============================================================

features:
	@echo "[make] Building features..."
	$(PYTHON) scripts/04_build_features.py


feature-stage:
	@echo "[make] Running feature-engineering stage..."
	$(PYTHON) scripts/run_feature_engineering_stage.py


# ============================================================
# Milestone 05 — Analytical Views
# ============================================================

views:
	@echo "[make] Building analytical views..."
	$(PYTHON) scripts/05_build_analytical_views.py


# ============================================================
# Milestone 06 — Pandas Business Analysis
# ============================================================

analysis:
	@echo "[make] Running Pandas business analysis..."
	$(PYTHON) scripts/06_run_analysis.py


# ============================================================
# Milestone 07 — SQLite Database
# ============================================================

database:
	@echo "[make] Building SQLite database..."
	$(PYTHON) scripts/07_build_database.py


# ============================================================
# Milestone 08 — SQL Analysis
# ============================================================

sql:
	@echo "[make] Running SQL analysis..."
	$(PYTHON) scripts/08_run_sql_analysis.py


# ============================================================
# Milestone 09 — Visualization
# ============================================================

figures:
	@echo "[make] Generating figures..."
	$(PYTHON) scripts/09_generate_figures.py


# ============================================================
# Tests
# ============================================================

test:
	@echo "[make] Running test suite..."
	$(PYTEST) -v


test-short:
	@echo "[make] Running test suite..."
	$(PYTEST) -q


# ============================================================
# Full Pipeline
# ============================================================

pipeline:
	@echo "[make] Running full pipeline..."
	$(PYTHON) scripts/run_full_pipeline.py


pipeline-test:
	@echo "[make] Running full pipeline with tests..."
	$(PYTHON) scripts/run_full_pipeline.py --test


pipeline-fetch:
	@echo "[make] Fetching dataset and running full pipeline..."
	$(PYTHON) scripts/run_full_pipeline.py --fetch


check: pipeline-test


# ============================================================
# Rebuild
# ============================================================

rebuild: clean-generated pipeline
	@echo ""
	@echo "[make] Rebuild completed successfully."


# ============================================================
# Cleanup
# ============================================================

clean-cache:
	@echo "[make] Removing Python caches..."
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type d -name ".ipynb_checkpoints" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "[make] Cache cleanup completed."


clean-interim:
	@echo "[make] Removing interim dataset..."
	rm -f $(INTERIM_DATA)


clean-processed:
	@echo "[make] Removing processed dataset..."
	rm -f $(PROCESSED_DATA)


clean-database:
	@echo "[make] Removing SQLite database..."
	rm -f $(DATABASE)


clean-figures:
	@echo "[make] Removing generated figures..."
	rm -f $(FIGURES_DIR)/*.png


clean-generated: \
	clean-interim \
	clean-processed \
	clean-database \
	clean-figures \
	clean-cache
	@echo ""
	@echo "[make] Generated artifacts removed."
	@echo "[make] Raw dataset preserved: $(RAW_DATA)"


# ============================================================
# Utilities
# ============================================================

status:
	git status


tree:
	tree -L 3 -I ".venv|__pycache__|.pytest_cache"