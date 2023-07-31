from django.urls import path, include
from .views import CartView, CheckoutView, UpdateCartView, GetCartView, DeleteCartItemView, CompleteOrder

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('update_cart/', UpdateCartView.as_view(), name='update_cart'),
    path('get_cart/', GetCartView.as_view(), name='get_cart'),
    path('delete_cart_item/', DeleteCartItemView.as_view(), name='delete_cart_item'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('complete_checkout/', CompleteOrder.as_view(), name='complete_checkout'),
]
