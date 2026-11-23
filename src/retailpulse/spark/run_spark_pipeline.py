
from pathlib import Path

import logging
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    trim,
    lower,
    initcap,
    to_date,
    year,
    month,
    sum as spark_sum,
    when
)

# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

project_folder = Path(__file__).resolve().parents[3]

customers_file = project_folder / "data" / "raw" / "customers.csv"
products_file = project_folder / "data" / "raw" / "products.csv"
orders_file = project_folder / "data" / "raw" / "orders.csv"

output_folder = project_folder / "data" / "processed" / "pyspark"


# --------------------------------------------------
# 2. LOGGING
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --------------------------------------------------
# 3. START SPARK
# --------------------------------------------------

spark = (
    SparkSession.builder
    .appName("RetailPulse_Complete_Pipeline")
    .master("local[*]")
    .getOrCreate()
)

try:

    logging.info("Spark pipeline started")

    # --------------------------------------------------
    # 4. EXTRACT - READ DATA
    # --------------------------------------------------

    customers = spark.read.option("header", True).option("inferSchema", True).csv(str(customers_file))
    products = spark.read.option("header", True).option("inferSchema", True).csv(str(products_file))
    orders = spark.read.option("header", True).option("inferSchema", True).csv(str(orders_file))

    logging.info("All raw datasets loaded")

    # --------------------------------------------------
    # 5. TRANSFORM - CLEAN DATA
    # --------------------------------------------------

    customers = customers.withColumn(
        "customer_name", initcap(trim(col("customer_name")))
    ).withColumn(
        "email", lower(trim(col("email")))
    ).withColumn(
        "city", initcap(trim(col("city")))
    ).withColumn(
        "registration_date", to_date(col("registration_date"))
    ).withColumn(
        "registration_year", year(col("registration_date"))
    )

    products = products.withColumn(
        "product_name", initcap(trim(col("product_name")))
    ).withColumn(
        "category", initcap(trim(col("category")))
    ).withColumn(
        "price", col("price").cast("double")
    )

    orders = orders.withColumn(
        "order_date", to_date(col("order_date"))
    ).withColumn(
        "payment_method", initcap(trim(col("payment_method")))
    ).withColumn(
        "order_status", initcap(trim(col("order_status")))
    ).withColumn(
        "order_year", year(col("order_date"))
    ).withColumn(
        "order_month", month(col("order_date"))
    )

    logging.info("All datasets cleaned")

    # --------------------------------------------------
    # 6. VALIDATE - MISSING VALUES
    # --------------------------------------------------

    def count_missing(df):
        result = df.select([
            spark_sum(when(col(column).isNull(), 1).otherwise(0)).alias(column)
            for column in df.columns
        ]).first()

        return sum(value for value in result if value is not None)

    customers_missing = count_missing(customers)
    products_missing = count_missing(products)
    orders_missing = count_missing(orders)

    logging.info("Missing values - Customers: %s", customers_missing)
    logging.info("Missing values - Products: %s", products_missing)
    logging.info("Missing values - Orders: %s", orders_missing)

    # --------------------------------------------------
    # 7. VALIDATE - DUPLICATE IDs
    # --------------------------------------------------

    duplicate_customers = customers.groupBy("customer_id").count().filter(
        col("count") > 1
    ).count()

    duplicate_products = products.groupBy("product_id").count().filter(
        col("count") > 1
    ).count()

    duplicate_orders = orders.groupBy("order_id").count().filter(
        col("count") > 1
    ).count()

    logging.info("Duplicate customer IDs: %s", duplicate_customers)
    logging.info("Duplicate product IDs: %s", duplicate_products)
    logging.info("Duplicate order IDs: %s", duplicate_orders)

    # --------------------------------------------------
    # 8. VALIDATE - BUSINESS RULES
    # --------------------------------------------------

    invalid_prices = products.filter(col("price") <= 0).count()
    invalid_quantities = orders.filter(col("quantity") <= 0).count()
    invalid_unit_prices = orders.filter(col("unit_price") <= 0).count()

    invalid_discounts = orders.filter(
        (col("discount_percent") < 0) |
        (col("discount_percent") > 100)
    ).count()

    invalid_amounts = orders.filter(col("total_amount") < 0).count()

    logging.info("Invalid prices: %s", invalid_prices)
    logging.info("Invalid quantities: %s", invalid_quantities)
    logging.info("Invalid unit prices: %s", invalid_unit_prices)
    logging.info("Invalid discounts: %s", invalid_discounts)
    logging.info("Invalid order amounts: %s", invalid_amounts)

    # --------------------------------------------------
    # 9. VALIDATE - REFERENCES
    # --------------------------------------------------

    invalid_customers = orders.join(
        customers.select("customer_id"),
        on="customer_id",
        how="left_anti"
    ).count()

    invalid_products = orders.join(
        products.select("product_id"),
        on="product_id",
        how="left_anti"
    ).count()

    logging.info("Invalid customer references: %s", invalid_customers)
    logging.info("Invalid product references: %s", invalid_products)

    # --------------------------------------------------
    # 10. STOP IF VALIDATION FAILS
    # --------------------------------------------------

    validation_results = [
        customers_missing,
        products_missing,
        orders_missing,
        duplicate_customers,
        duplicate_products,
        duplicate_orders,
        invalid_prices,
        invalid_quantities,
        invalid_unit_prices,
        invalid_discounts,
        invalid_amounts,
        invalid_customers,
        invalid_products
    ]

    if any(value > 0 for value in validation_results):
        raise ValueError("Data validation failed. Output was not saved.")

    logging.info("All validation checks passed")

    # --------------------------------------------------
    # 11. LOAD - SAVE CLEANED DATA
    # --------------------------------------------------

    # This saves to local CSV folders.
    # --------------------------------------------------

    output_folder.mkdir(parents=True, exist_ok=True)

    customers.toPandas().to_csv(
    output_folder / "customers_cleaned.csv",
    index=False
)

    products.toPandas().to_csv(
    output_folder / "products_cleaned.csv",
    index=False
)

    orders.toPandas().to_csv(
    output_folder / "orders_cleaned.csv",
    index=False
)

    logging.info("All cleaned datasets saved successfully")
    logging.info("RETAILPULSE SPARK PIPELINE COMPLETED!")

except Exception:
    logging.exception("Pipeline failed!")
    raise

finally:
    spark.stop()
