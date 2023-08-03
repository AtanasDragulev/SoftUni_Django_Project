from django.contrib.auth import get_user_model
from django.db import models
from online_store.apps.accounts.models import StoreUser
from online_store.apps.core.models import Product

User = get_user_model()


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    serial_number = models.CharField(max_length=100, unique=True)
    in_stock = models.BooleanField(default=True)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    deliveries = models.ManyToManyField('Delivery', related_name='items')

    class Meta:
        verbose_name_plural = 'Inventory'


class Delivery(models.Model):
    delivery_number = models.IntegerField(unique=True)
    invoice_number = models.IntegerField(unique=True)
    delivery_date = models.DateField()
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    created_by = models.ForeignKey(StoreUser, on_delete=models.RESTRICT, null=True, editable=False)

    class Meta:
        verbose_name_plural = 'Deliveries'

    def __str__(self):
        return f"Number: {self.delivery_number} Cost: {self.cost} - Created by: {self.created_by}"


class Supplier(models.Model):
    company_name = models.CharField(max_length=50)
    tax_id = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    comments = models.TextField(blank=True, null=True)
