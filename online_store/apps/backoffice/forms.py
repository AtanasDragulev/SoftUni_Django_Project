from django import forms

from online_store.apps.core.models import Product
from online_store.apps.inventory.models import Inventory, Delivery
from online_store.apps.sales.models import Order


class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['delivery_number', 'invoice_number', 'delivery_date', 'cost']


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['product', 'product_slug', 'serial_number', 'in_stock', 'cost']

    product_id = forms.IntegerField(label='Product ID', required=False)
    product_slug = forms.CharField(required=False)


InventoryFormSet = forms.modelformset_factory(Inventory, form=InventoryForm, extra=1)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['complete',]
