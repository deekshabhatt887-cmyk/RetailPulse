
import pandas as pd
import logging

# Import cleaning functions
from retailpulse.transformations.clean_customers import clean_customers
from retailpulse.transformations.clean_products import clean_products
from retailpulse.transformations.clean_orders import clean_orders

# Import validation functions
from retailpulse.validation.data_quality import (
    check_order_references,
    check_missing_values,
    check_duplicate_ids,
    check_business_rules
)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)


def run_pipeline():

    try:
        # STEP 1: Load raw datasets
        customers = pd.read_csv("data/raw/customers.csv")
        products = pd.read_csv("data/raw/products.csv")
        orders = pd.read_csv("data/raw/orders.csv")

        logging.info("All raw datasets loaded successfully!")

        # STEP 2: Validate datasets
        reference_result = check_order_references(
            orders, customers, products
        )

        missing_result = check_missing_values(
            customers, products, orders
        )

        duplicate_result = check_duplicate_ids(
            customers, products, orders
        )

        business_result = check_business_rules(
            products, orders
        )

        # STEP 3: Display validation results
        logging.info("Reference validation: %s", reference_result)
        logging.info("Missing values: %s", missing_result)
        logging.info("Duplicate IDs: %s", duplicate_result)
        logging.info("Business rules: %s", business_result)

        # STEP 4: Stop pipeline if validation fails
        if (
            reference_result["invalid_customers"] > 0
            or reference_result["invalid_products"] > 0
        ):
            raise ValueError("Invalid customer or product references found!")

        if any(value > 0 for value in missing_result.values()):
            raise ValueError("Missing values found!")

        if any(value > 0 for value in duplicate_result.values()):
            raise ValueError("Duplicate IDs found!")

        if any(value > 0 for value in business_result.values()):
            raise ValueError("Business rule violations found!")

        logging.info("All data validation checks passed!")

        # STEP 5: Clean datasets
        cleaned_customers = clean_customers(customers)
        cleaned_products = clean_products(products)
        cleaned_orders = clean_orders(orders)

        logging.info("All datasets cleaned successfully!")

        # STEP 6: Save cleaned datasets
        cleaned_customers.to_csv(
            "data/processed/customers_cleaned.csv",
            index=False
        )

        cleaned_products.to_csv(
            "data/processed/products_cleaned.csv",
            index=False
        )

        cleaned_orders.to_csv(
            "data/processed/orders_cleaned.csv",
            index=False
        )

        logging.info("All cleaned datasets saved successfully!")
        logging.info("ETL PIPELINE COMPLETED SUCCESSFULLY!")

    except Exception:
        logging.exception("ETL PIPELINE FAILED!")
        raise


if __name__ == "__main__":
    run_pipeline()
