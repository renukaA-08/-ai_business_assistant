from datetime import date
from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase

from analytics.models import Sale
from analytics.services.analytics_service import (
    get_total_revenue,
    get_top_product,
    get_top_region,
    get_monthly_revenue,
    get_monthly_revenue_change,
)
from analytics.services.chatbot_service import process_question


class AnalyticsServiceTests(TestCase):

    def setUp(self):
        Sale.objects.create(
            transaction_id="TEST001",
            order_date=date(2026, 1, 10),
            product="Keyboard",
            category="Accessories",
            region="South",
            sales_channel="Online",
            quantity=2,
            unit_price=Decimal("1000.00"),
            discount_amount=Decimal("100.00"),
            status="Completed",
        )

        Sale.objects.create(
            transaction_id="TEST002",
            order_date=date(2026, 2, 10),
            product="Monitor",
            category="Electronics",
            region="North",
            sales_channel="Retail",
            quantity=1,
            unit_price=Decimal("5000.00"),
            discount_amount=Decimal("0.00"),
            status="Completed",
        )

        Sale.objects.create(
            transaction_id="TEST003",
            order_date=date(2026, 2, 15),
            product="Keyboard",
            category="Accessories",
            region="South",
            sales_channel="Online",
            quantity=1,
            unit_price=Decimal("1000.00"),
            discount_amount=Decimal("0.00"),
            status="Returned",
        )

    def test_total_revenue(self):
        self.assertEqual(
            get_total_revenue(),
            Decimal("6900.00")
        )

    def test_top_product(self):
        result = get_top_product()
        self.assertEqual(result["product"], "Monitor")

    def test_top_region(self):
        result = get_top_region()
        self.assertEqual(result["region"], "North")

    def test_monthly_revenue(self):
        result = get_monthly_revenue()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["revenue"], Decimal("1900.00"))

    def test_monthly_revenue_change(self):
        result = get_monthly_revenue_change()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["change"], Decimal("3100.00"))


class ChatbotTests(TestCase):

    @patch(
        "analytics.services.chatbot_service.interpret_question",
        return_value={
            "intent": "total_revenue",
            "analytics_type": "descriptive",
            "product_name": None,
            "region_name": None,
        },
    )
    def test_total_revenue_question(self, mock_interpreter):
        Sale.objects.create(
            transaction_id="CHAT001",
            order_date=date(2026, 1, 10),
            product="Keyboard",
            category="Accessories",
            region="South",
            sales_channel="Online",
            quantity=2,
            unit_price=Decimal("1000.00"),
            discount_amount=Decimal("100.00"),
            status="Completed",
        )

        result = process_question("What is the total revenue?")

        self.assertEqual(result["intent"], "total_revenue")
        self.assertEqual(
            result["data"]["total_revenue"],
            1900.0
        )
