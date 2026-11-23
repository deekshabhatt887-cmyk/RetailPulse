
import boto3
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    trim,
    lower,
    initcap,
    to_date,
    year,
    month
)

# 1. Get AWS credentials
aws_session = boto3.Session(region_name="ap-southeast-2")
credentials = aws_session.get_credentials()

if credentials is None:
    raise Exception("AWS credentials not found!")

frozen_credentials = credentials.get_frozen_credentials()

# 2. Start Spark
spark = (
    SparkSession.builder
    .appName("RetailPulse_S3_ETL_Pipeline")
    .master("local[*]")
    .config(
        "spark.jars.packages",
        "org.apache.hadoop:hadoop-aws:3.5.0"
    )
    .config("spark.hadoop.fs.s3a.endpoint.region", "ap-southeast-2")
    .getOrCreate()
)

# 3. Configure AWS credentials
hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()

hadoop_conf.set("fs.s3a.access.key", frozen_credentials.access_key)
hadoop_conf.set("fs.s3a.secret.key", frozen_credentials.secret_key)

hadoop_conf.set(
    "fs.s3a.aws.credentials.provider",
    "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider"
)
# Use memory instead of local disk for S3 uploads
hadoop_conf.set(
    "fs.s3a.fast.upload",
    "true"
)

hadoop_conf.set(
    "fs.s3a.fast.upload.buffer",
    "array"
)

bucket_name = "deeksha-retail-data-learning-882464895342-ap-southeast-2-an"

raw_path = f"s3a://{bucket_name}/retailpulse/raw/"
processed_path = f"s3a://{bucket_name}/retailpulse/processed/"

try:
    # 4. Read raw datasets from S3
    print("Reading raw data from S3...")

    customers_df = spark.read.option("header", True).option(
        "inferSchema", True
    ).csv(raw_path + "customers.csv")

    products_df = spark.read.option("header", True).option(
        "inferSchema", True
    ).csv(raw_path + "products.csv")

    orders_df = spark.read.option("header", True).option(
        "inferSchema", True
    ).csv(raw_path + "orders.csv")

    print("All raw datasets loaded successfully!")

    # 5. Clean customers
    customers_cleaned = customers_df.withColumn(
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

    # 6. Clean products
    products_cleaned = products_df.withColumn(
        "product_name", initcap(trim(col("product_name")))
    ).withColumn(
        "category", initcap(trim(col("category")))
    ).withColumn(
        "price", col("price").cast("double")
    )

    # 7. Clean orders
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

    # 8. Check record counts
    print("Customers:", customers_cleaned.count())
    print("Products:", products_cleaned.count())
    print("Orders:", orders_cleaned.count())

    # 9. Save cleaned datasets to S3 as Parquet
    print("Saving cleaned data to S3...")

    customers_cleaned.write.mode("overwrite").parquet(
        processed_path + "customers/"
    )

    products_cleaned.write.mode("overwrite").parquet(
        processed_path + "products/"
    )

    orders_cleaned.write.mode("overwrite").parquet(
        processed_path + "orders/"
    )

    print("All cleaned datasets saved successfully to S3!")

finally:
    spark.stop()
