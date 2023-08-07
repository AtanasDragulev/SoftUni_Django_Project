from django import forms
from django.forms import inlineformset_factory
from online_store.apps.core.models import Product, ProductAttribute
from online_store.apps.inventory.models import Inventory, Delivery
from online_store.apps.sales.models import Order


class DeliveryForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['delivery_number', 'invoice_number', 'delivery_date', 'cost']
        widgets = {
            'delivery_date': forms.TextInput(attrs={'type': 'date'}),

        }


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['product', 'product_slug', 'serial_number', 'in_stock', 'cost']

    product_id = forms.IntegerField(label='Product ID', required=False)
    product_slug = forms.CharField(required=False)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['complete', ]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'category', 'image', 'description', 'price', 'active']


InventoryFormSet = forms.modelformset_factory(Inventory, form=InventoryForm, extra=1)

ProductAttributeFormSet = inlineformset_factory(
    Product,
    ProductAttribute,
    fields=('name', 'value',),
    extra=0,
    can_delete=False,
    labels={'name': '', 'value': ''}
)
