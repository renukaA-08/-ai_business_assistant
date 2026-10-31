
import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from analytics.models import Sale
from analytics.data_cleaning import (
    build_product_mappings,
    impute_missing_values,
)


class Command(BaseCommand):
    help = "Import sales transactions from CSV"

    def handle(self, *args, **kwargs):

        # Locate the project root
        project_root = Path(__file__).resolve().parents[3]
        file_path = project_root / "data" / "sales.csv"

        self.stdout.write(f"Reading CSV from: {file_path}")

        if not file_path.exists():
            self.stderr.write(
                self.style.ERROR(f"File not found: {file_path}")
            )
            return

        with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            required_columns = {
                "Transaction_Id", "Order_date", "Product",
                "Category", "Region", "Sales_channel",
                "Quantity", "Unit_price", "Discount_amount", "Status",
            }

            if not reader.fieldnames or not required_columns.issubset(
                {name.strip() for name in reader.fieldnames}
            ):
                self.stderr.write(self.style.ERROR("Invalid CSV headers"))
                return

            normalized_rows = [
                {
                    key.strip(): (value or "").strip()
                    for key, value in row.items()
                    if key is not None
                }
                for row in reader
            ]

        prices, categories = build_product_mappings(normalized_rows)

        valid_records = []
        invalid_records = []
        imputation_report = []
        seen_ids = set()

        required_fields = [
            "Transaction_Id", "Order_date", "Product", "Category",
            "Region", "Sales_channel", "Quantity", "Unit_price", "Status",
        ]

        for row_number, row in enumerate(normalized_rows, start=2):
            try:
                row, imputed_fields = impute_missing_values(
                    row, prices, categories
                )

                if imputed_fields:
                    imputation_report.append(
                        f"Row {row_number}: {imputed_fields}"
                    )

                missing = [
                    field for field in required_fields
                    if not row.get(field, "").strip()
                ]

                if missing:
                    raise ValueError(f"Missing fields: {missing}")

                transaction_id = row["Transaction_Id"]

                if transaction_id in seen_ids:
                    raise ValueError("Duplicate transaction ID in CSV")

                if Sale.objects.filter(
                    transaction_id=transaction_id
                ).exists():
                    raise ValueError("Transaction already exists")

                order_date = datetime.strptime(
                    row["Order_date"], "%d-%m-%Y"
                ).date()

                quantity = int(row["Quantity"])
                unit_price = Decimal(row["Unit_price"])
                discount_amount = Decimal(row["Discount_amount"] or "0")

                if quantity < 0:
                    raise ValueError("Negative quantity")

                if not unit_price.is_finite() or not discount_amount.is_finite():
                    raise ValueError("Invalid monetary value")

                if unit_price < 0 or discount_amount < 0:
                    raise ValueError("Negative price or discount")

                if discount_amount > quantity * unit_price:
                    raise ValueError("Discount exceeds gross value")

                valid_records.append(
                    Sale(
                        transaction_id=transaction_id,
                        order_date=order_date,
                        product=row["Product"],
                        category=row["Category"],
                        region=row["Region"],
                        sales_channel=row["Sales_channel"],
                        quantity=quantity,
                        unit_price=unit_price,
                        discount_amount=discount_amount,
                        status=row["Status"],
                    )
                )

                seen_ids.add(transaction_id)

            except (ValueError, KeyError, InvalidOperation, TypeError) as error:
                invalid_records.append(f"Row {row_number}: {error}")

        with transaction.atomic():
            Sale.objects.bulk_create(valid_records)

        self.stdout.write(self.style.SUCCESS(
            f"Imported: {len(valid_records)}"
        ))
        self.stdout.write(self.style.WARNING(
            f"Rejected: {len(invalid_records)}"
        ))

        self.stdout.write("Imputation report:")
        for item in imputation_report:
            self.stdout.write(item)

        self.stdout.write("Invalid records:")
        for item in invalid_records:
            self.stdout.write(item)
