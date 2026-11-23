import boto3

# Connect to AWS S3
s3 = boto3.client(
    "s3",
    region_name="ap-southeast-2"
)

bucket_name = "deeksha-retail-data-learning-882464895342-ap-southeast-2-an"

# S3 file location
s3_file = "retailpulse/raw/customers.csv"

# Local file location
local_file = "data/customers_from_s3.csv"

try:
    # Download the CSV file from S3
    s3.download_file(
        bucket_name,
        s3_file,
        local_file
    )

    print("File downloaded successfully!")
    print("Saved at:", local_file)

except Exception as e:
    print("Download failed!")
    print(e)
