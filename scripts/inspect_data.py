
import pandas as pd
from pathlib import Path

# Find project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Read CSV files
customers = pd.read_csv(PROJECT_ROOT / "data/raw/customers.csv")
products = pd.read_csv(PROJECT_ROOT / "data/raw/products.csv")
orders = pd.read_csv(PROJECT_ROOT / "data/raw/orders.csv")

# Inspect customers
print("\n========== CUSTOMERS ==========")
print(customers.head())
print("Shape:", customers.shape)
print(customers.info())

# Inspect products
print("\n========== PRODUCTS ==========")
print(products.head())
print("Shape:", products.shape)
print(products.info())

# Inspect orders
print("\n========== ORDERS ==========")
print(orders.head())
print("Shape:", orders.shape)
print(orders.info())
