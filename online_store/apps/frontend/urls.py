from django.urls import path

from online_store.apps.frontend.views import Index, create_product, ProductDetailView, \
    ProductDeleteView, edit_product, SearchResultsView, products_by_category, like_product, add_wishlist

urlpatterns = [
    path('', Index.as_view(), name='index'),
    # path('category/<str:category_name>/', CategoryProductsView.as_view(), name='category_products'),
    path('category/<str:category_name>/', products_by_category, name='category_products'),
    path('product/create/<str:category_name>', create_product, name='create_product'),
    path('product/details/<str:slug>', ProductDetailView.as_view(), name='product_details'),
    path('product/edit/<str:slug>', edit_product, name='edit_product'),
    path('product/delete/<str:slug>', ProductDeleteView.as_view(), name='delete_product'),
    path('product/like/<str:slug>', like_product, name='like_product'),
    path('product/wishlist/<str:slug>', add_wishlist, name='add_product_to_wishlist'),
    path('search_results', SearchResultsView.as_view(), name='search_results'),

]

