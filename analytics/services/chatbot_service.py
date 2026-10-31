
from analytics.services.question_interpreter import interpret_question

from analytics.services.analytics_service import (
    get_total_revenue,
    get_top_product,
    get_lowest_product,
    get_product_revenue,
    get_top_category,
    get_top_region,
    get_lowest_region,
    get_regional_revenue,
    get_region_revenue,
    get_monthly_revenue,
    get_highest_revenue_month,
    get_average_monthly_revenue,
    get_monthly_revenue_change,
    get_total_transactions,
    get_total_quantity_sold,
    get_average_order_value,
    get_total_discount,
    get_top_sales_channel,
    get_returned_transactions,
)


def money(value):
    """Format a numeric value as Indian rupees."""
    return f"₹{value:,.2f}"


def no_sales_response(intent):
    return {
        "intent": intent,
        "answer": "No completed sales records were found.",
        "data": None,
    }


def process_question(question):
    """
    Interpret a user's question and execute the corresponding
    analytics function.

    Gemini identifies the intent and extracts parameters.
    Django ORM performs all business calculations.
    """

    classification = interpret_question(question)
    intent = classification["intent"]

    # 1. TOTAL REVENUE
    if intent == "total_revenue":
        revenue = get_total_revenue()

        return {
            "intent": intent,
            "answer": f"Your total revenue is {money(revenue)}.",
            "data": {"total_revenue": float(revenue)},
        }

    # 2. HIGHEST-REVENUE PRODUCT
    elif intent == "top_product":
        result = get_top_product()

        if not result:
            return no_sales_response(intent)

        product = result["product"]
        revenue = result["revenue"]

        return {
            "intent": intent,
            "answer": (
                f"{product} generated the highest revenue "
                f"of {money(revenue)}."
            ),
            "data": {
                "product": product,
                "revenue": float(revenue),
            },
        }

    # 3. LOWEST-REVENUE PRODUCT
    elif intent == "lowest_product":
        result = get_lowest_product()

        if not result:
            return no_sales_response(intent)

        product = result["product"]
        revenue = result["revenue"]

        return {
            "intent": intent,
            "answer": (
                f"{product} generated the lowest revenue "
                f"of {money(revenue)}."
            ),
            "data": {
                "product": product,
                "revenue": float(revenue),
            },
        }

    # 4. REVENUE OF A PARTICULAR PRODUCT
    elif intent == "product_revenue":
        product_name = classification["product_name"]
        revenue = get_product_revenue(product_name)

        if revenue is None:
            return {
                "intent": intent,
                "answer": (
                    f"No completed sales were found for "
                    f"the product '{product_name}'."
                ),
                "data": None,
            }

        return {
            "intent": intent,
            "answer": (
                f"{product_name} generated revenue "
                f"of {money(revenue)}."
            ),
            "data": {
                "product": product_name,
                "revenue": float(revenue),
            },
        }

    # 5. HIGHEST-REVENUE CATEGORY
    elif intent == "top_category":
        result = get_top_category()

        if not result:
            return no_sales_response(intent)

        category = result["category"]
        revenue = result["revenue"]

        return {
            "intent": intent,
            "answer": (
                f"{category} generated the highest category "
                f"revenue of {money(revenue)}."
            ),
            "data": {
                "category": category,
                "revenue": float(revenue),
            },
        }

    # 6. HIGHEST-REVENUE REGION
    elif intent == "top_region":
        result = get_top_region()

        if not result:
            return no_sales_response(intent)

        region = result["region"]
        revenue = result["revenue"]

        return {
            "intent": intent,
            "answer": (
                f"{region} generated the highest regional "
                f"revenue of {money(revenue)}."
            ),
            "data": {
                "region": region,
                "revenue": float(revenue),
            },
        }

    # 7. LOWEST-REVENUE REGION
    elif intent == "lowest_region":
        result = get_lowest_region()

        if not result:
            return no_sales_response(intent)

        region = result["region"]
        revenue = result["revenue"]

        return {
            "intent": intent,
            "answer": (
                f"{region} generated the lowest regional "
                f"revenue of {money(revenue)}."
            ),
            "data": {
                "region": region,
                "revenue": float(revenue),
            },
        }

    # 8. REGIONAL REVENUE COMPARISON
    elif intent == "regional_comparison":
        results = get_regional_revenue()

        if not results:
            return no_sales_response(intent)

        data = [
            {
                "region": item["region"],
                "revenue": float(item["revenue"]),
            }
            for item in results
        ]

        lines = [
            f"{item['region']}: {money(item['revenue'])}"
            for item in data
        ]

        answer = (
            "Here is your revenue comparison across regions:\n\n"
            + "\n".join(lines)
        )

        return {
            "intent": intent,
            "answer": answer,
            "data": data,
        }

    # 9. REVENUE OF A PARTICULAR REGION
    elif intent == "region_revenue":
        region_name = classification["region_name"]
        revenue = get_region_revenue(region_name)

        if revenue is None:
            return {
                "intent": intent,
                "answer": (
                    f"No completed sales were found for "
                    f"the region '{region_name}'."
                ),
                "data": None,
            }

        return {
            "intent": intent,
            "answer": (
                f"{region_name} generated revenue "
                f"of {money(revenue)}."
            ),
            "data": {
                "region": region_name,
                "revenue": float(revenue),
            },
        }

    # 10. MONTHLY REVENUE
    elif intent == "monthly_revenue":
        results = get_monthly_revenue()

        if not results:
            return no_sales_response(intent)

        data = [
            {
                "month": item["month"].strftime("%B %Y"),
                "revenue": float(item["revenue"]),
            }
            for item in results
        ]

        lines = [
            f"{item['month']}: {money(item['revenue'])}"
            for item in data
        ]

        answer = (
            "Here is your monthly revenue breakdown:\n\n"
            + "\n".join(lines)
        )

        return {
            "intent": intent,
            "answer": answer,
            "data": data,
        }

    # 11. HIGHEST-REVENUE MONTH
    elif intent == "highest_revenue_month":
        result = get_highest_revenue_month()

        if not result:
            return no_sales_response(intent)

        month = result["month"].strftime("%B %Y")
        revenue = result["revenue"]

        return {
            "intent": intent,
            "answer": (
                f"{month} generated the highest monthly revenue "
                f"of {money(revenue)}."
            ),
            "data": {
                "month": month,
                "revenue": float(revenue),
            },
        }

    # 12. AVERAGE MONTHLY REVENUE
    elif intent == "average_monthly_revenue":
        revenue = get_average_monthly_revenue()

        return {
            "intent": intent,
            "answer": (
                f"Your average monthly revenue is {money(revenue)}."
            ),
            "data": {
                "average_monthly_revenue": float(revenue),
            },
        }

    # 13. MONTH-TO-MONTH REVENUE CHANGE
    elif intent == "monthly_revenue_change":
        results = get_monthly_revenue_change()

        if not results:
            return no_sales_response(intent)

        data = [
            {
                "month": item["month"].strftime("%B %Y"),
                "previous_revenue": float(item["previous_revenue"]),
                "current_revenue": float(item["current_revenue"]),
                "change": float(item["change"]),
                "percentage_change": (
                    float(item["percentage_change"])
                    if item["percentage_change"] is not None
                    else None
                ),
            }
            for item in results
        ]

        lines = []

        for item in data:
            if item["change"] > 0:
                direction = "increased"
            elif item["change"] < 0:
                direction = "decreased"
            else:
                direction = "remained unchanged"

            if item["percentage_change"] is not None:
                percentage = (
                    f" ({abs(item['percentage_change']):.2f}%)"
                )
            else:
                percentage = ""

            lines.append(
                f"{item['month']}: Revenue {direction} by "
                f"{money(abs(item['change']))}{percentage}."
            )

        answer = (
            "Here is your month-to-month revenue comparison:\n\n"
            + "\n".join(lines)
        )

        return {
            "intent": intent,
            "answer": answer,
            "data": data,
        }

    # 14. TOTAL COMPLETED TRANSACTIONS
    elif intent == "total_transactions":
        count = get_total_transactions()

        return {
            "intent": intent,
            "answer": (
                f"You have {count:,} completed transactions."
            ),
            "data": {"total_transactions": count},
        }

    # 15. TOTAL QUANTITY SOLD
    elif intent == "total_quantity_sold":
        quantity = get_total_quantity_sold()

        return {
            "intent": intent,
            "answer": (
                f"The total quantity of products sold is "
                f"{quantity:,} units."
            ),
            "data": {"total_quantity_sold": quantity},
        }

    # 16. AVERAGE ORDER VALUE
    elif intent == "average_order_value":
        value = get_average_order_value()

        return {
            "intent": intent,
            "answer": (
                f"Your average order value is {money(value)}."
            ),
            "data": {"average_order_value": float(value)},
        }

    # 17. TOTAL DISCOUNT
    elif intent == "total_discount":
        discount = get_total_discount()

        return {
            "intent": intent,
            "answer": (
                f"The total discount provided on completed "
                f"transactions is {money(discount)}."
            ),
            "data": {"total_discount": float(discount)},
        }

    # 18. HIGHEST-REVENUE SALES CHANNEL
    elif intent == "top_sales_channel":
        result = get_top_sales_channel()

        if not result:
            return no_sales_response(intent)

        channel = result["sales_channel"]
        revenue = result["revenue"]

        return {
            "intent": intent,
            "answer": (
                f"{channel} generated the highest sales-channel "
                f"revenue of {money(revenue)}."
            ),
            "data": {
                "sales_channel": channel,
                "revenue": float(revenue),
            },
        }

    # 19. RETURNED TRANSACTIONS
    elif intent == "returned_transactions":
        count = get_returned_transactions()

        return {
            "intent": intent,
            "answer": (
                f"You have {count:,} returned transactions."
            ),
            "data": {"returned_transactions": count},
        }

    # UNSUPPORTED QUESTIONS
    return {
        "intent": "unknown",
        "answer": (
            "I couldn't understand that business question. "
            "You can ask about revenue, products, categories, "
            "regions, monthly trends, transactions, quantities, "
            "average order value, discounts, sales channels, "
            "or returned transactions."
        ),
        "data": None,
    }
