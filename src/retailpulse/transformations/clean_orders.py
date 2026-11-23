import pandas as pd
def clean_orders(orders):

    # Create a copy so the original data is not changed
    orders = orders.copy()

    # Convert order_date from string to datetime
    orders["order_date"] = pd.to_datetime(
        orders["order_date"]
    )

    # Standardize text columns
    orders["payment_method"] = (
        orders["payment_method"].str.strip().str.title()
    )

    orders["order_status"] = (
        orders["order_status"].str.strip().str.title()
    )

    # Extract year and month from order date
    orders["order_year"] = orders["order_date"].dt.year

    orders["order_month"] = orders["order_date"].dt.month

    return orders
