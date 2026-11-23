
def check_order_references(orders, customers, products):

    invalid_customers = orders[
        ~orders["customer_id"].isin(customers["customer_id"])
    ]

    invalid_products = orders[
        ~orders["product_id"].isin(products["product_id"])
    ]

    return {
        "total_orders": len(orders),
        "invalid_customers": len(invalid_customers),
        "invalid_products": len(invalid_products)
    }


def check_missing_values(customers, products, orders):

    return {
        "customers_missing_values": int(customers.isna().sum().sum()),
        "products_missing_values": int(products.isna().sum().sum()),
        "orders_missing_values": int(orders.isna().sum().sum())
    }


def check_duplicate_ids(customers, products, orders):

    return {
        "duplicate_customer_ids": int(customers["customer_id"].duplicated().sum()),
        "duplicate_product_ids": int(products["product_id"].duplicated().sum()),
        "duplicate_order_ids": int(orders["order_id"].duplicated().sum())
    }


def check_business_rules(products, orders):

    invalid_product_prices = products[
        products["price"] <= 0
    ]

    invalid_quantities = orders[
        orders["quantity"] <= 0
    ]

    invalid_unit_prices = orders[
        orders["unit_price"] <= 0
    ]

    invalid_discounts = orders[
        (orders["discount_percent"] < 0) |
        (orders["discount_percent"] > 100)
    ]

    invalid_order_amounts = orders[
        orders["total_amount"] < 0
    ]

    return {
        "invalid_product_prices": len(invalid_product_prices),
        "invalid_quantities": len(invalid_quantities),
        "invalid_unit_prices": len(invalid_unit_prices),
        "invalid_discounts": len(invalid_discounts),
        "invalid_order_amounts": len(invalid_order_amounts)
    }
