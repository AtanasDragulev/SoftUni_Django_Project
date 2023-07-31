import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView

from .forms import CheckoutForm

from ..accounts.models import Profile, Address
from ..core.models import Product
from ..sales.models import Order, OrderItem, ShippingDetails


class CartView(View):
    template_name = 'cart/cart.html'

    def get(self, request):
        cart_items, total_price = self.get_cart_items(request)
        context = {'cart_items': cart_items, 'total_price': total_price}
        return render(request, self.template_name, context)

    @staticmethod
    def get_cart_items(request):
        cart = request.session.get('cart', {})
        cart_items = []
        cart_total = 0

        for product_id, quantity in cart.items():
            try:
                product = Product.objects.get(pk=product_id)
                total = product.price * quantity
                cart_items.append(
                    {'product': product,
                     'quantity': quantity,
                     'total': total, }
                )
                cart_total += total
            except Product.DoesNotExist:
                pass
        return cart_items, cart_total


class UpdateCartView(View):
    def post(self, request):
        data = json.loads(request.body)
        product_id = data.get('product_id')
        action = data.get('action')

        cart = request.session.get('cart', {})
        quantity = cart.get(str(product_id), 0)

        if action == 'add' and quantity < Product.objects.get(pk=product_id).quantity:
            quantity += 1
        elif action == 'remove':
            quantity -= 1

        quantity = max(quantity, 0)
        if quantity <= 0:
            del cart[str(product_id)]

        cart[str(product_id)] = quantity
        request.session['cart'] = cart

        return JsonResponse({'message': 'Cart updated successfully', "quantity": quantity})


class GetCartView(View):
    def get(self, request):
        cart = request.session.get('cart', {})
        return JsonResponse(cart)


class DeleteCartItemView(View):
    def post(self, request):
        data = json.loads(request.body)
        product_id = data.get('product_id')

        if product_id:
            cart = request.session.get('cart', {})
            if str(product_id) in cart:
                del cart[str(product_id)]
                request.session['cart'] = cart
                return JsonResponse({'message': 'Item removed successfully'})
            else:
                return JsonResponse({'error': 'Item not found in cart'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid product_id'}, status=400)


class CheckoutView(LoginRequiredMixin, FormView):
    template_name = 'cart/checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('complete_checkout', context={'status': 'success'})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items, total_price = self.get_cart_items(self.request)
        profile = Profile.objects.get(pk=self.request.user.pk)
        context.update({
            'profile': profile,
            'cart_items': cart_items,
            'total_price': total_price
        })
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        cart_items = self.get_context_data()['cart_items']

        for item in cart_items:
            if item['quantity'] > item['product'].quantity:
                self.request.session['cart'][str(item['product'].pk)] = item['product'].quantity
                self.request.session.save()

                return render(self.request, template_name='cart/complete_checkout.html',
                              context={'status': 'failed', 'item': item})

        order = Order.objects.create(
            customer=self.request.user,
            payment_type=form.cleaned_data['payment_type']
        )
        for cart_item in cart_items:
            product = cart_item['product']
            quantity = cart_item['quantity']
            OrderItem.objects.create(
                product=product,
                order=order,
                price=product.price,
                quantity=quantity,
            )
        address = Address.objects.get(pk=form.cleaned_data['selected_address'].pk)
        shipping_details = ShippingDetails.objects.create(
            customer=self.request.user,
            order=order,
            country=address.country,
            state=address.state,
            city=address.city,
            address=address.address,
            postal_code=address.postal_code,
            phone_number=address.phone_number,
        )
        order.save()
        self.request.session['cart'] = {}

        return super().form_valid(form)

    @staticmethod
    def get_cart_items(request):
        cart = request.session.get('cart', {})
        cart_items = []
        cart_total = 0

        for product_id, quantity in cart.items():
            try:
                product = Product.objects.get(pk=product_id)
                total = product.price * quantity
                cart_items.append(
                    {'product': product,
                     'quantity': quantity,
                     'total': total, }
                )
                cart_total += total
            except Product.DoesNotExist:
                pass
        return cart_items, cart_total


class CompleteOrder(LoginRequiredMixin, TemplateView):
    template_name = 'cart/complete_checkout.html'
