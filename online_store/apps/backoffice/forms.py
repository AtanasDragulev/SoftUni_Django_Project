from django import forms

from online_store.apps.core.models import Product
from online_store.apps.inventory.models import Inventory, Delivery


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


# class UserPermissionsForm(forms.Form):
#     staff = forms.BooleanField(label='Staff Member', required=False)
#     managers = forms.BooleanField(label='Manager', required=False)
#     admin = forms.BooleanField(label='Administrator', required=False)
