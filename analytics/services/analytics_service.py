
from decimal import Decimal

from django.db.models import (
    Sum,
    F,
    Count,
    DecimalField,
    ExpressionWrapper,
)
from django.db.models.functions import TruncMonth

from analytics.models import Sale


# Revenue = quantity * unit price - discount
# Only completed transactions contribute to revenue.
REVENUE_EXPRESSION = ExpressionWrapper(
    F("quantity") * F("unit_price") - F("discount_amount"),
    output_field=DecimalField(max_digits=15, decimal_places=2),
)


def completed_sales():
    return Sale.objects.filter(status__iexact="Completed")


# --------------------------------------------------
# REVENUE ANALYTICS
# --------------------------------------------------

def get_total_revenue():
    result = completed_sales().aggregate(
        total=Sum(REVENUE_EXPRESSION)
    )
    return result["total"] or Decimal("0.00")


# --------------------------------------------------
# PRODUCT ANALYTICS
# --------------------------------------------------

def get_top_product():
    return (
        completed_sales()
        .values("product")
        .annotate(revenue=Sum(REVENUE_EXPRESSION))
        .order_by("-revenue")
        .first()
    )


def get_lowest_product():
    return (
        completed_sales()
        .values("product")
        .annotate(revenue=Sum(REVENUE_EXPRESSION))
        .order_by("revenue")
        .first()
    )


def get_product_revenue(product_name):
    result = completed_sales().filter(
        product__iexact=product_name
    ).aggregate(
        revenue=Sum(REVENUE_EXPRESSION),
        transaction_count=Count("id"),
    )

    if result["transaction_count"] == 0:
        return None

    return result["revenue"] or Decimal("0.00")


# --------------------------------------------------
# CATEGORY ANALYTICS
# --------------------------------------------------

def get_top_category():
    return (
        completed_sales()
        .values("category")
        .annotate(revenue=Sum(REVENUE_EXPRESSION))
        .order_by("-revenue")
        .first()
    )


# --------------------------------------------------
# REGION ANALYTICS
# --------------------------------------------------

def get_top_region():
    return (
        completed_sales()
        .values("region")
        .annotate(revenue=Sum(REVENUE_EXPRESSION))
        .order_by("-revenue")
        .first()
    )


def get_lowest_region():
    return (
        completed_sales()
        .values("region")
        .annotate(revenue=Sum(REVENUE_EXPRESSION))
        .order_by("revenue")
        .first()
    )


def get_regional_revenue():
    return list(
        completed_sales()
        .values("region")
        .annotate(revenue=Sum(REVENUE_EXPRESSION))
        .order_by("-revenue")
    )


def get_region_revenue(region_name):
    result = completed_sales().filter(
        region__iexact=region_name
    ).aggregate(
        revenue=Sum(REVENUE_EXPRESSION),
        transaction_count=Count("id"),
    )

    if result["transaction_count"] == 0:
        return None

    return result["revenue"] or Decimal("0.00")


# --------------------------------------------------
# MONTHLY ANALYTICS
# --------------------------------------------------

def get_monthly_revenue():
    return list(
        completed_sales()
        .annotate(month=TruncMonth("order_date"))
        .values("month")
        .annotate(revenue=Sum(REVENUE_EXPRESSION))
        .order_by("month")
    )


def get_highest_revenue_month():
    monthly_data = get_monthly_revenue()

    if not monthly_data:
        return None

    return max(monthly_data, key=lambda item: item["revenue"])


def get_average_monthly_revenue():
    monthly_data = get_monthly_revenue()

    if not monthly_data:
        return Decimal("0.00")

    total = sum(
        (item["revenue"] for item in monthly_data),
        Decimal("0.00"),
    )

    return total / len(monthly_data)


def get_monthly_revenue_change():
    monthly_data = get_monthly_revenue()
    results = []

    for index in range(1, len(monthly_data)):
        previous = monthly_data[index - 1]["revenue"]
        current = monthly_data[index]["revenue"]

        change = current - previous

        percentage = (
            (change / previous) * 100
            if previous != 0
            else None
        )

        results.append({
            "month": monthly_data[index]["month"],
            "previous_revenue": previous,
            "current_revenue": current,
            "change": change,
            "percentage_change": percentage,
        })

    return results


# --------------------------------------------------
# SALES ANALYTICS
# --------------------------------------------------

def get_total_transactions():
    return completed_sales().count()


def get_total_quantity_sold():
    result = completed_sales().aggregate(
        quantity=Sum("quantity")
    )

    return result["quantity"] or 0


def get_average_order_value():
    transaction_count = get_total_transactions()

    if transaction_count == 0:
        return Decimal("0.00")

    return get_total_revenue() / transaction_count


# --------------------------------------------------
# DISCOUNT ANALYTICS
# --------------------------------------------------

def get_total_discount():
    result = completed_sales().aggregate(
        total_discount=Sum("discount_amount")
    )

    return result["total_discount"] or Decimal("0.00")


# --------------------------------------------------
# SALES CHANNEL ANALYTICS
# --------------------------------------------------

def get_top_sales_channel():
    return (
        completed_sales()
        .values("sales_channel")
        .annotate(revenue=Sum(REVENUE_EXPRESSION))
        .order_by("-revenue")
        .first()
    )


# --------------------------------------------------
# RETURN ANALYTICS
# --------------------------------------------------

def get_returned_transactions():
    return Sale.objects.filter(
        status__iexact="Returned"
    ).count()
