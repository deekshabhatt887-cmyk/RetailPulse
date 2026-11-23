
import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


# 1. Make the generated data reproducible
random.seed(42)

# 2. Find the main project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 3. Define where CSV files will be stored
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw"
RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)


# 4. Define sample business information
first_names = [
    "Rahul", "Priya", "Amit", "Neha", "Karan",
    "Anjali", "Rohit", "Sneha", "Vikas", "Pooja"
]

last_names = [
    "Sharma", "Mehta", "Verma", "Patel", "Gupta",
    "Singh", "Kumar", "Joshi", "Agarwal", "Reddy"
]

cities = [
    "Pune", "Mumbai", "Delhi", "Bengaluru",
    "Jaipur", "Hyderabad", "Chennai", "Kolkata",
    "Ahmedabad", "Bhilwara"
]

categories = [
    "Electronics", "Fashion", "Home & Kitchen",
    "Beauty", "Sports", "Books"
]

payment_methods = [
    "UPI", "Credit Card", "Debit Card",
    "Net Banking", "Cash on Delivery"
]

order_statuses = [
    "Delivered", "Shipped", "Processing", "Cancelled"
]


# 5. Generate customers
customers = []

for i in range(1, 1001):
    customer_id = f"C{i:04d}"

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)

    customer = {
        "customer_id": customer_id,
        "customer_name": f"{first_name} {last_name}",
        "email": f"customer{i}@example.com",
        "city": random.choice(cities),
        "registration_date": (
            date(2024, 1, 1)
            + timedelta(days=random.randint(0, 365))
        )
    }

    customers.append(customer)

customers_df = pd.DataFrame(customers)


# 6. Generate products
products = []

for i in range(1, 101):
    category = random.choice(categories)

    product = {
        "product_id": f"P{i:04d}",
        "product_name": f"{category} Product {i}",
        "category": category,
        "price": round(random.uniform(200, 50000), 2)
    }

    products.append(product)

products_df = pd.DataFrame(products)


# 7. Generate orders
orders = []

for i in range(1, 10001):
    customer = random.choice(customers)
    product = random.choice(products)

    quantity = random.randint(1, 5)
    unit_price = product["price"]
    discount_percent = random.choice([0, 5, 10, 15])

    total_amount = (
        quantity * unit_price
        * (1 - discount_percent / 100)
    )

    order = {
        "order_id": f"O{i:06d}",
        "customer_id": customer["customer_id"],
        "product_id": product["product_id"],
        "order_date": (
            date(2025, 1, 1)
            + timedelta(days=random.randint(0, 668))
        ),
        "quantity": quantity,
        "unit_price": unit_price,
        "discount_percent": discount_percent,
        "total_amount": round(total_amount, 2),
        "payment_method": random.choice(payment_methods),
        "order_status": random.choice(order_statuses)
    }

    orders.append(order)

orders_df = pd.DataFrame(orders)


# 8. Save all datasets as CSV files
customers_df.to_csv(
    RAW_DATA_PATH / "customers.csv",
    index=False
)

products_df.to_csv(
    RAW_DATA_PATH / "products.csv",
    index=False
)

orders_df.to_csv(
    RAW_DATA_PATH / "orders.csv",
    index=False
)


# 9. Display generation results
print("RetailPulse datasets generated successfully!")

print(f"Customers: {len(customers_df)}")
print(f"Products: {len(products_df)}")
print(f"Orders: {len(orders_df)}")

print(f"\nFiles saved in: {RAW_DATA_PATH}")
