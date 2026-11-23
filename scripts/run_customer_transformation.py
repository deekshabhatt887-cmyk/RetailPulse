import pandas as  pd

from retailpulse.transformations.clean_customers import clean_customers

customers = pd.read_csv("data/raw/customers.csv")

cleaned_customers = clean_customers(customers)

print(cleaned_customers.head())

cleaned_customers.to_csv("data/processed/customers_cleaned.csv",
    index=False
)

print("Customer data cleaned successfully!")