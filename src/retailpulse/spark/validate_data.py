
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, when

# Find the main RetailPulse project folder
project_folder = Path(__file__).resolve().parents[3]

# Raw dataset locations
customers_file = project_folder / "data" / "raw" / "customers.csv"
products_file = project_folder / "data" / "raw" / "products.csv"
orders_file = project_folder / "data" / "raw" / "orders.csv"

# Start Spark
spark = (
    SparkSession.builder
    .appName("RetailPulse_Data_Validation")
    .master("local[*]")
    .getOrCreate()
)

# Read datasets
customers = spark.read.option("header", True).option("inferSchema", True).csv(str(customers_file))
products = spark.read.option("header", True).option("inferSchema", True).csv(str(products_file))
orders = spark.read.option("header", True).option("inferSchema", True).csv(str(orders_file))


# 1. CHECK MISSING VALUES

def check_missing_values(df, dataset_name):
    print(f"\nMissing values in {dataset_name}:")

    missing_checks = df.select([
        sum(when(col(column).isNull(), 1).otherwise(0)).alias(column)
        for column in df.columns
    ])

    missing_checks.show()


check_missing_values(customers, "Customers")
check_missing_values(products, "Products")
check_missing_values(orders, "Orders")


# 2. CHECK DUPLICATE IDs

def check_duplicates(df, id_column, dataset_name):
    duplicates = (
        df.groupBy(id_column)
        .count()
        .filter(col("count") > 1)
    )

    print(f"\nDuplicate IDs in {dataset_name}:")
    duplicates.show()

    print("Number of duplicate IDs:", duplicates.count())


check_duplicates(customers, "customer_id", "Customers")
check_duplicates(products, "product_id", "Products")
check_duplicates(orders, "order_id", "Orders")


# 3. CHECK BUSINESS RULES

print("\nBusiness rule validation:")

invalid_product_prices = products.filter(col("price") <= 0).count()

invalid_quantities = orders.filter(col("quantity") <= 0).count()

invalid_unit_prices = orders.filter(col("unit_price") <= 0).count()

invalid_discounts = orders.filter(
    (col("discount_percent") < 0) |
    (col("discount_percent") > 100)
).count()

invalid_order_amounts = orders.filter(col("total_amount") < 0).count()

print("Invalid product prices:", invalid_product_prices)
print("Invalid quantities:", invalid_quantities)
print("Invalid unit prices:", invalid_unit_prices)
print("Invalid discounts:", invalid_discounts)
print("Invalid order amounts:", invalid_order_amounts)


# 4. CHECK CUSTOMER AND PRODUCT REFERENCES

invalid_customers = (
    orders.join(
        customers.select("customer_id"),
        on="customer_id",
        how="left_anti"
    ).count()
)

invalid_products = (
    orders.join(
        products.select("product_id"),
        on="product_id",
        how="left_anti"
    ).count()
)

print("\nReference validation:")
print("Orders with invalid customers:", invalid_customers)
print("Orders with invalid products:", invalid_products)


print("\nPySpark data validation completed!")

spark.stop()
