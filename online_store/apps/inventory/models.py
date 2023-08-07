from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from online_store.apps.accounts.models import StoreUser
from online_store.apps.core.models import Product
from online_store.tools.custom_validators import validate_characters_digits_dashes_only

User = get_user_model()


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    serial_number = models.CharField(
        max_length=100,
        unique=True,
        validators=(validate_characters_digits_dashes_only,)
    )
    in_stock = models.BooleanField(default=True)
    cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=(MinValueValidator(0.1, message="Cost cannot be negative or zero "),)
    )
    date_created = models.DateTimeField(auto_now_add=True)
    delivery = models.ForeignKey('Delivery', on_delete=models.RESTRICT)

    class Meta:
        verbose_name_plural = 'Inventory'


class Delivery(models.Model):
    delivery_number = models.PositiveIntegerField(unique=True)
    invoice_number = models.PositiveIntegerField(unique=True)
    delivery_date = models.DateField()
    cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=(MinValueValidator(0.1, message="Cost cannot be negative or zero "),)
    )
    created_by = models.ForeignKey(StoreUser, on_delete=models.RESTRICT, null=True, editable=False)

    class Meta:
        verbose_name_plural = 'Deliveries'

    def __str__(self):
        return f"Number: {self.delivery_number} Cost: {self.cost} - Created by: {self.created_by}"


