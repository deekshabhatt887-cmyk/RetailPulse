
import boto3
from pyspark.sql import SparkSession

# Step 1: Get AWS credentials
aws_session = boto3.Session(region_name="ap-southeast-2")
credentials = aws_session.get_credentials()

if credentials is None:
    raise Exception("AWS credentials not found!")

frozen_credentials = credentials.get_frozen_credentials()

# Step 2: Start Spark
spark = (
    SparkSession.builder
    .appName("RetailPulse_S3_Reader")
    .master("local[*]")
    .config(
        "spark.jars.packages",
        "org.apache.hadoop:hadoop-aws:3.5.0"
    )
    .config("spark.hadoop.fs.s3a.endpoint.region", "ap-southeast-2")
    .getOrCreate()
)

# Step 3: Configure AWS credentials for Spark
hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()

hadoop_conf.set("fs.s3a.access.key", frozen_credentials.access_key)
hadoop_conf.set("fs.s3a.secret.key", frozen_credentials.secret_key)

hadoop_conf.set(
    "fs.s3a.aws.credentials.provider",
    "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider"
)

# Step 4: Define S3 location
bucket_name = "deeksha-retail-data-learning-882464895342-ap-southeast-2-an"

s3_folder = f"s3a://{bucket_name}/retailpulse/raw/"

try:
    # Step 5: Read all three datasets
    customers_df = spark.read.option("header", True).csv(
        s3_folder + "customers.csv"
    )

    products_df = spark.read.option("header", True).csv(
        s3_folder + "products.csv"
    )

    orders_df = spark.read.option("header", True).csv(
        s3_folder + "orders.csv"
    )

    # Step 6: Display record counts
    print("CUSTOMERS:", customers_df.count())
    print("PRODUCTS:", products_df.count())
    print("ORDERS:", orders_df.count())

    # Step 7: Display sample records
    print("Customer data:")
    customers_df.show(5)

    print("Product data:")
    products_df.show(5)

    print("Order data:")
    orders_df.show(5)

finally:
    spark.stop()
