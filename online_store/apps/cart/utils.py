from online_store.apps.core.models import Product


def get_cart_items(request):
    cart = request.session.get('cart', {})
    items = []
    for product_id, quantity in cart.items():
        product = Product.objects.get(pk=product_id)
        item = {
            'product': product,
            'quantity': quantity
        }
        items.append(item)
    return items


def get_cart_data(request):
    cart = request.session.get('cart', {})
    total = 0
    cart_items = 0
    for quantity in cart.values():
        total += quantity
        cart_items += 1
    order = {
        'get_cart_total': total,
        'get_cart_items': cart_items,
        'shipping': False,  # You can set this based on your logic
    }
    return {
        'order': order,
        'items': get_cart_items(request),
    }
