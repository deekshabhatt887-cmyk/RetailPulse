
import pandas as pd
from pathlib import Path

from retailpulse.transformations.clean_orders import clean_orders

# Find project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Read raw orders
orders = pd.read_csv(PROJECT_ROOT / "data/raw/orders.csv")

print("Before transformation:")
print(orders.dtypes)

# Apply transformation
cleaned_orders = clean_orders(orders)

print("\nAfter transformation:")
print(cleaned_orders.dtypes)

# Display transformed data
print("\nTransformed orders:")
print(cleaned_orders.head())

# Display new columns
print("\nNew columns:")
print(cleaned_orders[["order_date", "order_year", "order_month"]].head())

# Save transformed data
output_path = PROJECT_ROOT / "data/processed/orders_cleaned.csv"

cleaned_orders.to_csv(output_path, index=False)

print("\nCleaned data saved successfully!")
print("File location:", output_path)