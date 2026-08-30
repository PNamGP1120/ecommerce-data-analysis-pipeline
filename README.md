# E-commerce Data Analysis Pipeline

A reproducible end-to-end data analysis project built with Python, Pandas, SQLite, SQL, Matplotlib, pytest, and Jupyter.

The project processes the UCI Online Retail dataset from raw transactional data into validated analytical datasets, a SQLite database, SQL analyses, and portfolio-ready visualizations.

## Project Overview

The objective of this project is to build a reproducible analytical pipeline for an e-commerce transaction dataset and answer business questions related to sales performance, customers, products, markets, purchasing patterns, and cancellations.

The pipeline covers:

* raw data acquisition;
* structural validation;
* data-quality investigation;
* cleaning and normalization;
* feature engineering;
* analytical view construction;
* Pandas business analysis;
* SQLite database construction;
* SQL analysis;
* data visualization;
* automated testing.

The project intentionally separates raw data, transformation logic, orchestration scripts, SQL queries, tests, and generated artifacts.

## Dataset

The project uses the **Online Retail** dataset from the UCI Machine Learning Repository, dataset ID `352`.

The source dataset contains transaction-level records for a UK-based online retailer covering the period from December 2010 through December 2011.

Raw dataset size:

* **541,909 transaction lines**
* **8 source columns**
* **25,900 invoice documents**
* **4,372 identified customers**
* **38 countries**

The observed date range is:

* Start: `2010-12-01`
* End: `2011-12-09`

December 2011 therefore represents a partial month and should not be directly compared with complete months without that limitation being stated.

## Tech Stack

* Python
* NumPy
* Pandas
* SQLite
* SQL
* Matplotlib
* pytest
* Jupyter
* Git
* uv

## Project Architecture

```text
.
├── data/
│   ├── raw/
│   ├── interim/
│   └── processed/
│
├── database/
│   └── ecommerce.db
│
├── notebooks/
│   └── 00_dataset_understanding.ipynb
│
├── reports/
│   ├── final_report.md
│   └── figures/
│       ├── 01_monthly_revenue.png
│       ├── 02_monthly_growth.png
│       ├── 03_top_products_revenue.png
│       ├── 04_top_international_markets.png
│       ├── 05_top_customers.png
│       ├── 06_orders_by_weekday.png
│       ├── 07_orders_by_hour.png
│       └── 08_top_cancelled_products.png
│
├── scripts/
│   ├── 00_fetch_raw_data.py
│   ├── 01_validate_raw_data.py
│   ├── 02_data_quality_report.py
│   ├── 03_clean_data.py
│   ├── 04_build_features.py
│   ├── 05_build_analytical_views.py
│   ├── 06_run_analysis.py
│   ├── 07_build_database.py
│   ├── 08_run_sql_analysis.py
│   ├── 09_generate_figures.py
│   └── run_full_pipeline.py
│
├── sql/
│   ├── 01_sales_overview.sql
│   ├── 02_product_analysis.sql
│   ├── 03_customer_analysis.sql
│   ├── 04_market_analysis.sql
│   ├── 05_time_analysis.sql
│   └── 06_cancellation_analysis.sql
│
├── src/ecommerce_analysis/
│   ├── analysis.py
│   ├── analytical_views.py
│   ├── config.py
│   ├── data_cleaner.py
│   ├── data_loader.py
│   ├── data_validator.py
│   ├── database.py
│   ├── feature_engineering.py
│   ├── sql_analysis.py
│   └── visualization.py
│
├── tests/
├── pyproject.toml
├── uv.lock
└── README.md
```

## Pipeline

```text
UCI Online Retail
        │
        ▼
Raw Dataset
541,909 rows
        │
        ▼
Structural Validation
        │
        ▼
Data Quality Investigation
        │
        ▼
Cleaning + Quality Flags
        │
        ▼
Interim Dataset
        │
        ▼
Feature Engineering
        │
        ▼
Processed Dataset
541,909 × 25
        │
        ├───────────────┐
        ▼               ▼
Pandas Analysis     SQLite Database
                        │
                        ▼
                    SQL Analysis
        │               │
        └───────┬───────┘
                ▼
          Visualizations
                │
                ▼
           Final Report
```

## Data Quality Strategy

The cleaning strategy follows:

> **Normalize + flag + preserve**

Records are not blindly deleted merely because they contain unusual business values.

The pipeline identifies and preserves:

* cancelled invoices;
* negative quantities;
* negative non-cancelled quantities;
* zero prices;
* negative prices;
* missing customer IDs;
* missing descriptions;
* duplicate groups;
* unusual StockCodes.

This allows downstream analyses to explicitly choose the appropriate analytical population.

### Important Data Quality Findings

The raw dataset contains:

* `135,080` rows without CustomerID;
* `1,454` rows without Description;
* `10,624` rows with negative Quantity;
* `9,288` cancellation rows;
* `1,336` negative-quantity rows that are not cancellation documents;
* `2,515` zero-price rows;
* `2` negative-price rows;
* `10,147` rows participating in exact duplicate groups.

Duplicate sensitivity analysis estimates that duplicate groups potentially affect approximately **0.44% of valid-sales revenue**.

Because the source dataset does not contain a unique line-item identifier, duplicate-looking rows are flagged rather than automatically removed.

## Analytical Views

The SQLite and Pandas layers use the same business definitions.

### Valid Sales

A valid sales transaction must satisfy:

```text
IsCancelled = False
IsNegativeQuantity = False
IsZeroQuantity = False
IsNegativePrice = False
IsZeroPrice = False
```

Customer identification is not required for general sales analysis.

### Customer Sales

Customer analysis uses:

```text
Valid Sale
+
HasCustomerID = True
```

### Cancellations

Cancellation records are identified by invoice numbers beginning with `C`.

Negative Quantity alone is not considered sufficient evidence of cancellation.

### Anomalies

An anomaly view captures records including:

* negative non-cancelled quantities;
* negative prices;
* zero prices;
* missing descriptions.

## Key Results

Using the valid-sales analytical view:

| Metric                                  |         Result |
| --------------------------------------- | -------------: |
| Valid sales rows                        |        530,104 |
| Valid orders                            |         19,960 |
| Total revenue                           | £10,666,684.54 |
| Average Order Value                     |        £534.40 |
| Average revenue per identified customer |      £2,054.27 |
| Cancellation document share             |         14.81% |
| UK revenue share                        |         84.61% |

### Revenue Trend

![Monthly Revenue](reports/figures/01_monthly_revenue.png)

Revenue increased strongly during the final part of 2011.

November 2011 produced approximately **£1.51 million**, the highest monthly revenue observed in the dataset.

December 2011 should not be interpreted as a complete month because the dataset ends on December 9.

### Month-over-Month Growth

![Monthly Growth](reports/figures/02_monthly_growth.png)

Notable revenue growth occurred in:

* March 2011: approximately `+37%`;
* May 2011: approximately `+43%`;
* September 2011: approximately `+39%`;
* November 2011: approximately `+31%`.

The apparent December decline is strongly affected by the partial-month dataset boundary.

### Product / StockCode Revenue

![Top StockCode Revenue](reports/figures/03_top_products_revenue.png)

The largest StockCode–Description pairs include both merchandise and non-merchandise records.

Examples of special codes include:

* `DOT` — DOTCOM POSTAGE;
* `M` — Manual;
* `POST` — POSTAGE;
* `AMAZONFEE` — AMAZON FEE.

For this reason, the analysis avoids assuming that every StockCode represents a normal retail product.

### International Markets

![International Markets](reports/figures/04_top_international_markets.png)

The United Kingdom accounts for approximately **84.61% of valid-sales revenue**.

Outside the UK, the leading markets are:

1. Netherlands
2. EIRE
3. Germany
4. France
5. Australia

### Customer Concentration

![Top Customers](reports/figures/05_top_customers.png)

Customer `14646` generated approximately **£280,206** in identified-customer revenue, followed by customer `18102` at approximately **£259,657**.

High revenue does not necessarily imply the highest order frequency. For example, some customers place relatively few but extremely large orders.

### Weekly Ordering Pattern

![Orders by Weekday](reports/figures/06_orders_by_weekday.png)

Thursday has the highest number of valid orders.

No Saturday transactions are present in the dataset.

### Hourly Ordering Pattern

![Orders by Hour](reports/figures/07_orders_by_hour.png)

Order activity is concentrated during daytime business hours, with the highest number of unique orders observed around **12:00**.

### Cancellations

![Top Cancelled Products](reports/figures/08_top_cancelled_products.png)

Several StockCodes contain unusually large cancelled quantities.

The dataset also contains extreme transactions such as quantities above 70,000 units. These records are preserved because the available source data is insufficient to classify them confidently as data errors.

## SQLite Database

The project builds a reproducible SQLite database containing:

### Tables

* `transactions`
* `customers`
* `products`

### Views

* `valid_sales`
* `customer_sales`
* `cancellations`
* `anomalies`

Database validation ensures the Pandas and SQLite analytical definitions produce consistent row counts and revenue.

Current database statistics:

| Object         |    Rows |
| -------------- | ------: |
| transactions   | 541,909 |
| customers      |   4,372 |
| products       |   4,783 |
| valid_sales    | 530,104 |
| customer_sales | 397,884 |
| cancellations  |   9,288 |
| anomalies      |   2,517 |

## SQL Analysis

SQL analysis covers:

* aggregation;
* filtering;
* `GROUP BY`;
* `HAVING`;
* CTEs;
* subqueries;
* `CASE`;
* `COUNT(DISTINCT ...)`;
* window functions;
* `RANK()`;
* `LAG()`.

Example:

```sql
WITH customer_metrics AS (
    SELECT
        CustomerID,
        COUNT(DISTINCT InvoiceNo) AS OrderCount,
        SUM(Revenue) AS Revenue
    FROM customer_sales
    GROUP BY CustomerID
)

SELECT
    CustomerID,
    OrderCount,
    ROUND(Revenue, 2) AS Revenue,
    RANK() OVER (
        ORDER BY Revenue DESC
    ) AS RevenueRank
FROM customer_metrics
ORDER BY RevenueRank
LIMIT 20;
```

## Testing

The project includes unit and integration tests covering:

* structural validation;
* cleaning;
* feature engineering;
* analytical views;
* Pandas analysis;
* SQLite database generation;
* SQL execution;
* visualization.

Current status:

```text
64 passed
```

## Running the Project

Install dependencies:

```bash
uv sync
```

Run the complete pipeline:

```bash
uv run python scripts/run_full_pipeline.py
```

Fetch the UCI dataset again:

```bash
uv run python scripts/run_full_pipeline.py --fetch
```

Run the pipeline and complete test suite:

```bash
uv run python scripts/run_full_pipeline.py --test
```

Run only tests:

```bash
uv run pytest -v
```

## Limitations

Several limitations should be considered when interpreting the results.

First, December 2011 contains only data through December 9 and therefore cannot be directly compared with full months.

Second, some StockCodes represent postage, manual adjustments, platform fees, or administrative records rather than normal merchandise.

Third, exact duplicate-looking transaction lines cannot be conclusively classified as errors because the dataset does not provide a unique transaction-line identifier.

Fourth, approximately one quarter of raw transaction lines do not contain CustomerID, meaning customer-level analysis represents only the identified-customer portion of the dataset.

Finally, extreme quantities and unusually large transaction values are preserved rather than automatically removed because there is insufficient evidence in the source dataset to classify them as invalid.

## Skills Demonstrated

This project demonstrates practical experience with:

* Python project structure;
* reproducible data pipelines;
* Pandas transformations;
* data validation;
* missing-value handling;
* data-quality investigation;
* feature engineering;
* business metric definition;
* analytical grain;
* SQLite database design;
* SQL aggregation and window functions;
* Pandas/SQL consistency validation;
* Matplotlib visualization;
* automated testing with pytest;
* Git-friendly project organization.

## Conclusion

The project transforms a large raw retail transaction dataset into a reproducible analytical system rather than treating analysis as a collection of notebook cells.

Business definitions are made explicit, unusual records are preserved and investigated, Pandas and SQL calculations are cross-validated, and generated visualizations communicate the major findings while documenting important data limitations.
