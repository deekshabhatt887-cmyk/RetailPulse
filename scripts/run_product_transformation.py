import pandas as pd

from retailpulse.transformations.clean_products import clean_products

# Read product data
products = pd.read_csv("data/raw/products.csv")

# Clean product data
cleaned_products = clean_products(products)

# Display first 5 rows
print(cleaned_products.head())

# Save cleaned data
cleaned_products.to_csv(
    "data/processed/products_cleaned.csv",
    index=False
)

print("Product data cleaned successfully!")