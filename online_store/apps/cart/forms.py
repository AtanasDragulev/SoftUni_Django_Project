from django import forms

from online_store.apps.sales.models import Order, OrderItem


class AddToCartForm(forms.Form):
    product_id = forms.IntegerField()
    quantity = forms.IntegerField(required=False, initial=1)


class RemoveFromCartForm(forms.Form):
    product_id = forms.IntegerField()


class CheckoutForm(forms.Form):
    payment_type = forms.ChoiceField(
        choices=[
            ('on_delivery', 'On Delivery'),
            ('credit_card', 'Credit Card'),
            ('bank_transfer', 'Bank Transfer'),
        ]
    )
    selected_address = forms.ModelChoiceField(
        queryset=None,
        empty_label="Select an address",
    )

    def __init__(self, *args, user=None, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['selected_address'].queryset = user.address_set.all()



