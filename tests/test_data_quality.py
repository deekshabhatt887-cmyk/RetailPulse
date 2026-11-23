
import pandas as pd

from retailpulse.validation.data_quality import (
    check_order_references,
    check_missing_values,
    check_duplicate_ids,
    check_business_rules
)


def test_order_references():

    customers = pd.DataFrame({
        "customer_id": ["C001", "C002"]
    })

    products = pd.DataFrame({
        "product_id": ["P001", "P002"]
    })

    orders = pd.DataFrame({
        "customer_id": ["C001", "C999"],
        "product_id": ["P001", "P002"]
    })

    result = check_order_references(orders, customers, products)

    assert result["total_orders"] == 2
    assert result["invalid_customers"] == 1
    assert result["invalid_products"] == 0


def test_missing_values():

    customers = pd.DataFrame({
        "customer_id": ["C001", None]
    })

    products = pd.DataFrame({
        "product_id": ["P001"]
    })

    orders = pd.DataFrame({
        "order_id": ["O001", None]
    })

    result = check_missing_values(customers, products, orders)

    assert result["customers_missing_values"] == 1
    assert result["products_missing_values"] == 0
    assert result["orders_missing_values"] == 1


def test_duplicate_ids():

    customers = pd.DataFrame({
        "customer_id": ["C001", "C001"]
    })

    products = pd.DataFrame({
        "product_id": ["P001", "P002"]
    })

    orders = pd.DataFrame({
        "order_id": ["O001", "O001"]
    })

    result = check_duplicate_ids(customers, products, orders)

    assert result["duplicate_customer_ids"] == 1
    assert result["duplicate_product_ids"] == 0
    assert result["duplicate_order_ids"] == 1


def test_business_rules():

    products = pd.DataFrame({
        "price": [100, -50]
    })

    orders = pd.DataFrame({
        "quantity": [2, -1],
        "unit_price": [100, 0],
        "discount_percent": [10, 150],
        "total_amount": [180, -50]
    })

    result = check_business_rules(products, orders)

    assert result["invalid_product_prices"] == 1
    assert result["invalid_quantities"] == 1
    assert result["invalid_unit_prices"] == 1
    assert result["invalid_discounts"] == 1
    assert result["invalid_order_amounts"] == 1
