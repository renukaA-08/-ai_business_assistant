
from collections import defaultdict
from decimal import Decimal, InvalidOperation


def build_product_mappings(rows):
    """
    Build mappings using reliable, existing records.

    Product -> Category
    Product -> Unit Price
    """

    prices = defaultdict(set)
    categories = defaultdict(set)

    for row in rows:

        product = row.get("Product", "").strip()
        category = row.get("Category", "").strip()
        price = row.get("Unit_price", "").strip()

        if not product:
            continue

        if category:
            categories[product].add(category)

        if price:
            try:
                value = Decimal(price)

                if value.is_finite() and value >= 0:
                    prices[product].add(value)

            except InvalidOperation:
                continue

    return prices, categories


def impute_missing_values(row, prices, categories):

    imputed_fields = []

    product = row.get("Product", "").strip()

    # Fill missing category
    if not row.get("Category", "").strip() and product:

        known_categories = categories.get(product, set())

        if len(known_categories) == 1:
            row["Category"] = next(iter(known_categories))
            imputed_fields.append("Category")

    # Fill missing unit price
    if not row.get("Unit_price", "").strip() and product:

        known_prices = prices.get(product, set())

        if len(known_prices) == 1:
            row["Unit_price"] = str(next(iter(known_prices)))
            imputed_fields.append("Unit_price")

    # Missing discount is treated as zero
    if not row.get("Discount_amount", "").strip():

        row["Discount_amount"] = "0"
        imputed_fields.append("Discount_amount")

    return row, imputed_fields
