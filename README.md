# RetailPulse — End-to-End Retail Data Engineering Pipeline

## Project Overview

RetailPulse is an end-to-end Data Engineering portfolio project designed to build a data pipeline for processing retail customers, products, and order information.

The project demonstrates how raw retail data can be ingested, cleaned, validated, transformed, stored, and made available for business analytics using Python, PySpark, PostgreSQL, and AWS services.

The pipeline covers both local data processing and cloud-based data processing using Amazon S3.

## Project Objectives

- Build an end-to-end ETL pipeline.
- Perform data cleaning and transformation using Python, Pandas, and PySpark.
- Implement data quality checks and validation.
- Store structured data in PostgreSQL.
- Integrate AWS S3 for cloud data storage.
- Store processed datasets in Parquet format.
- Use AWS Glue Data Catalog to discover processed datasets.
- Query and analyze retail data using Amazon Athena.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas, PySpark |
| Database | PostgreSQL |
| Query Language | SQL |
| Cloud Storage | Amazon S3 |
| Data Catalog | AWS Glue Crawler, Glue Data Catalog |
| Cloud Analytics | Amazon Athena |
| Version Control | Git, GitHub |

## Project Architecture

```text
              Raw Retail Data
                     |
          Customers, Products, Orders
                     |
             Python / Pandas
                     |
          Data Cleaning and Validation
                     |
               PostgreSQL
                     |
              SQL Analytics


              AWS Processing Flow

             Raw CSV Files
                     |
                  Amazon S3
                     |
              PySpark Pipeline
                     |
          Data Cleaning and Validation
                     |
             Parquet Files
                     |
                  Amazon S3
                     |
              AWS Glue Crawler
                     |
              Glue Data Catalog
                     |
                Athena SQL
                     |
             Business Analytics
```

## Dataset Information

The project uses synthetic retail datasets.

| Dataset | Number of Records |
|---|---:|
| Customers | 1,000 |
| Products | 100 |
| Orders | 10,000 |

### Dataset Fields

**Customers**
- customer_id
- customer_name
- email
- city
- registration_date

**Products**
- product_id
- product_name
- category
- price

**Orders**
- order_id
- customer_id
- product_id
- order_date
- quantity
- unit_price
- discount_percent
- total_amount
- payment_method
- order_status

## Key Features Implemented

### 1. Data Ingestion
- Loaded retail CSV datasets using Python and Pandas.
- Generated synthetic datasets for pipeline development.
- Integrated Amazon S3 for raw data storage.

### 2. Data Cleaning and Transformation
- Cleaned customer, product, and order datasets.
- Handled missing and inconsistent values.
- Standardized text and date columns.
- Created additional date-based columns for analysis.
- Implemented transformations using Pandas and PySpark.

### 3. Data Quality Validation
- Checked missing values.
- Identified duplicate records.
- Validated unique identifiers.
- Applied business-rule validations.
- Verified cleaned datasets before loading.

### 4. Database Integration
- Loaded cleaned datasets into PostgreSQL.
- Practised SQL joins, aggregations, CTEs, and window functions.
- Created analytical queries for retail business insights.

### 5. AWS Cloud Integration
- Uploaded raw datasets to Amazon S3.
- Read S3 data using PySpark.
- Processed and stored cleaned datasets in Parquet format.
- Used AWS Glue Crawler to create Data Catalog tables.
- Queried processed datasets using Amazon Athena.

## AWS S3 Structure

```text
RetailPulse/
    raw/
        customers.csv
        products.csv
        orders.csv

    processed/
        customers/
        products/
        orders/
```

## Project Folder Structure

```text
RetailPulse/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── scripts/
│
├── src/
│   └── retailpulse/
│       ├── database/
│       ├── ingestion/
│       ├── spark/
│       ├── transformations/
│       └── validation/
│
├── tests/
│
├── sql/
│
├── aws/
│
├── README.md
├── requirements.txt
├── pyproject.toml
└── .gitignore
```

## Project Outcomes

- Built a pipeline for processing 10,000 synthetic retail orders.
- Implemented data cleaning and validation using Pandas and PySpark.
- Integrated PostgreSQL for relational data storage and SQL analytics.
- Implemented S3-based cloud data processing.
- Stored processed datasets in Parquet format.
- Integrated AWS Glue Data Catalog and Amazon Athena for analytics.
- Successfully uploaded the project source code to GitHub.

## Future Improvements

- Automate pipeline execution and scheduling.
- Implement AWS Glue ETL jobs.
- Add advanced pipeline monitoring and alerting.
- Expand automated testing and data quality checks.

## Repository

GitHub: https://github.com/deekshabhatt887-cmyk/RetailPulse

## Author

Deeksha Bhatt

Data Engineering Portfolio Project

Data Engineering Portfolio Project
