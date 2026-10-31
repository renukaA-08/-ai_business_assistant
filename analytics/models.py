from django.db import models

# Create your models here.

class Sale(models.Model):

    transaction_id = models.CharField(
        max_length=20,
        unique=True
    )

    order_date = models.DateField()

    product = models.CharField(max_length=100)

    category = models.CharField(max_length=100)

    region = models.CharField(max_length=50)

    sales_channel = models.CharField(max_length=50)

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    discount_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(max_length=30)

    def __str__(self):
        return self.transaction_id
