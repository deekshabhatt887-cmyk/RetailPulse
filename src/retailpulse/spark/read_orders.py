
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, count

project_folder = Path(__file__).resolve().parents[3]

orders_file = project_folder / "data" / "raw" / "orders.csv"
products_file = project_folder / "data" / "raw" / "products.csv"

spark = (
    SparkSession.builder
    .appName("RetailPulse")
    .master("local[*]")
    .getOrCreate()
)

# Read datasets
orders_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(orders_file))
)

products_df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(str(products_file))
)

# Join orders and products
sales_df = orders_df.join(
    products_df,
    on="product_id",
    how="inner"
)

# Calculate category-wise revenue
print("Category-wise revenue:")

category_sales = sales_df.groupBy("category").agg(
    sum("total_amount").alias("total_revenue")
)

category_sales.orderBy(
    col("total_revenue").desc()
).show()

# Calculate category-wise order count
print("Category-wise order count:")

category_orders = sales_df.groupBy("category").agg(
    count("order_id").alias("total_orders")
)

category_orders.show()

# Calculate average order value by category
print("Average order value by category:")

category_average = sales_df.groupBy("category").agg(
    avg("total_amount").alias("average_revenue")
)

category_average.show()

spark.stop()
