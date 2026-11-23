import pandas as pd


def clean_products(products):

    # Keep original data unchanged
    products = products.copy()

    # Remove extra spaces
    products["product_name"] = products["product_name"].str.strip()
    products["category"] = products["category"].str.strip()

    # Standardize product names and categories
    products["product_name"] = products["product_name"].str.title()
    products["category"] = products["category"].str.title()

    # Make sure price is numeric
    products["price"] = pd.to_numeric(products["price"])

    return products