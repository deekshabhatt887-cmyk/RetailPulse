
import pandas as pd
import logging

from retailpulse.database.connection import engine

logging.basicConfig(level=logging.INFO)


def load_data():

    # STEP 1: Read cleaned CSV files
    customers = pd.read_csv("data/processed/customers_cleaned.csv")
    products = pd.read_csv("data/processed/products_cleaned.csv")
    orders = pd.read_csv("data/processed/orders_cleaned.csv")

    logging.info("Cleaned CSV files loaded successfully!")

    # STEP 2: Load customers
    customers.to_sql(
        name="retailpulse_customers",
        con=engine,
        if_exists="replace",
        index=False
    )

    logging.info("RetailPulse customers table loaded!")

    # STEP 3: Load products
    products.to_sql(
        name="retailpulse_products",
        con=engine,
        if_exists="replace",
        index=False
    )

    logging.info("RetailPulse products table loaded!")

    # STEP 4: Load orders
    orders.to_sql(
        name="retailpulse_orders",
        con=engine,
        if_exists="replace",
        index=False
    )

    logging.info("RetailPulse orders table loaded!")

    logging.info("All RetailPulse data loaded successfully!")


if __name__ == "__main__":
    load_data()
