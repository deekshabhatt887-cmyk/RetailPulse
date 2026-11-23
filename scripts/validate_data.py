
import pandas as pd
from pathlib import Path

from retailpulse.validation.data_quality import (
    check_order_references,
    check_missing_values,
    check_duplicate_ids
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load datasets
customers = pd.read_csv(PROJECT_ROOT / "data/raw/customers.csv")
products = pd.read_csv(PROJECT_ROOT / "data/raw/products.csv")
orders = pd.read_csv(PROJECT_ROOT / "data/raw/orders.csv")

# Run validation functions
reference_results = check_order_references(orders, customers, products)

missing_results = check_missing_values(customers, products, orders)

duplicate_results = check_duplicate_ids(customers, products, orders)

# Display report
print("\n========== RETAILPULSE DATA QUALITY REPORT ==========")

print("\n1. ORDER REFERENCE CHECKS")
for check, result in reference_results.items():
    print(f"{check}: {result}")

print("\n2. MISSING VALUE CHECKS")
for check, result in missing_results.items():
    print(f"{check}: {result}")

print("\n3. DUPLICATE ID CHECKS")
for check, result in duplicate_results.items():
    print(f"{check}: {result}")

    from retailpulse.validation.data_quality import (
    check_order_references,
    check_missing_values,
    check_duplicate_ids,
    check_business_rules
)

business_results = check_business_rules(products, orders)

print("\n4. BUSINESS RULE CHECKS")

for check, result in business_results.items():
    print(f"{check}: {result}")

