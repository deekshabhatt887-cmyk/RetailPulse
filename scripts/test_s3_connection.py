
import boto3

# Connect to AWS S3
s3 = boto3.client(
    "s3",
    region_name="ap-southeast-2"
)

bucket_name = "deeksha-retail-data-learning-882464895342-ap-southeast-2-an"

try:
    # Get files from the RetailPulse raw folder
    response = s3.list_objects_v2(
        Bucket=bucket_name,
        Prefix="retailpulse/raw/"
    )

    print("Successfully connected to S3!")
    print("\nFiles available in RetailPulse raw folder:")

    if "Contents" in response:
        for file in response["Contents"]:
            print(file["Key"])
    else:
        print("No files found in this folder.")

except Exception as e:
    print("Error accessing S3:")
    print(e)
