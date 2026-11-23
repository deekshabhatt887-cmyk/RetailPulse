from pathlib import Path

from pyspark.sql import SparkSession
from  pyspark.sql.functions import(
    col,
    trim,
    lower,
    initcap,
    to_date,
    year,
    month
)

#find project folder
project_folder = Path(__file__).resolve().parents[3]

#file locations

customers_file = project_folder/"data"/ "raw"/ "customers.csv"
products_file = project_folder/ "data"/"raw"/"products.csv"
orders_file = project_folder/"data"/"raw"/ "orders.csv"

spark = (
    SparkSession.builder
    .appName("RetailPulse_Data_Cleaning")
    .master("local[*]")
    .getOrCreate()
)

customers_df = spark.read.option("header", True).option("inferSchema", True).csv(str(customers_file))
products_df = spark.read.option("header", True).option("inferSchema", True).csv(str(products_file))
orders_df = spark.read.option("header", True).option("inferSchema", True).csv(str(orders_file))

#clean customers
customers_cleaned = customers_df.withColumn(
    "customer_name",  initcap(trim(col("customer_name")))

).withColumn(
    "email", lower(trim(col("email")))
).withColumn(
    "city", initcap(trim(col("city")))
).withColumn(
    "registration_date", to_date(col("registration_date"))
).withColumn(
    "registration_year", year(col("registration_date"))
)

# 2. Clean products
# -------------------------

products_cleaned = products_df.withColumn(
    "product_name", initcap(trim(col("product_name")))
).withColumn(
    "category", initcap(trim(col("category")))
).withColumn(
    "price", col("price").cast("double")
)


# -------------------------
# 3. Clean orders
# -------------------------

orders_cleaned = orders_df.withColumn(
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


# Display results
print("Cleaned customers:")
customers_cleaned.show(5)

print("Cleaned products:")
products_cleaned.show(5)

print("Cleaned orders:")
orders_cleaned.show(5)


# Save cleaned datasets
output_folder = project_folder / "data" / "processed" / "pyspark"

print("Customers cleaned:", customers_cleaned.count())
print("Products cleaned:", products_cleaned.count())
print("Orders cleaned:", orders_cleaned.count())

# customers_cleaned.write.mode("overwrite").option("header", True).csv(str(output_folder / "customers"))
# products_cleaned.write.mode("overwrite").option("header", True).csv(str(output_folder / "products"))
# orders_cleaned.write.mode("overwrite").option("header", True).csv(str(output_folder / "orders"))

print("All cleaned datasets saved successfully!")

spark.stop()
