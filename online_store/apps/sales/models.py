from django.contrib.auth import get_user_model
from django.db import models

from online_store.apps.core.models import Product

User = get_user_model()


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.RESTRICT)
    date_ordered = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    payment_type = models.CharField(max_length=30)

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.price for item in orderitems])
        return total

    @property
    def get_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    order = models.ForeignKey(Order, on_delete=models.RESTRICT)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    serial_number = models.CharField(max_length=100, unique=True, null=True)
    date_added = models.DateField(auto_now_add=True)


class ShippingDetails(models.Model):
    customer = models.ForeignKey(User, on_delete=models.RESTRICT)
    order = models.ForeignKey(Order, on_delete=models.RESTRICT)
    country = models.CharField(max_length=56)
    state = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.city} {self.address} {self.country}"
