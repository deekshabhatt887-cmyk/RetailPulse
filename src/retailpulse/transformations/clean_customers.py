
import pandas as pd


def clean_customers(customers):

    # Keep original data unchanged
    customers = customers.copy()

    # Remove extra spaces from text columns
    customers["customer_name"] = customers["customer_name"].str.strip()
    customers["email"] = customers["email"].str.strip()
    customers["city"] = customers["city"].str.strip()

    # Standardize customer names and cities
    customers["customer_name"] = customers["customer_name"].str.title()
    customers["city"] = customers["city"].str.title()

    # Standardize email addresses
    customers["email"] = customers["email"].str.lower()

    # Convert registration date into datetime
    customers["registration_date"] = pd.to_datetime(
        customers["registration_date"]
    )

    # Extract registration year
    customers["registration_year"] = (
        customers["registration_date"].dt.year
    )

    return customers
