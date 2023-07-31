from django.http import JsonResponse
from .models import Product


def get_product_details(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        product_data = {
            'pk': product.pk,
            'name': product.name,
            'slug': product.slug,
        }
        return JsonResponse(product_data)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
