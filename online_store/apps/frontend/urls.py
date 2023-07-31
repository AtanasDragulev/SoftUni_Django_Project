from django.urls import path

from online_store.apps.frontend.views import Index, create_product, CategoryProductsView, ProductDetailView, \
    ProductDeleteView, edit_product, SearchResultsView

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('category/<str:category_name>/', CategoryProductsView.as_view(), name='category_products'),

    path('product/create/<str:category_name>', create_product, name='create_product'),
    path('product/details/<str:slug>', ProductDetailView.as_view(), name='product_details'),
    path('product/edit/<str:slug>', edit_product, name='edit_product'),
    path('product/delete/<str:slug>', ProductDeleteView.as_view(), name='delete_product'),
    path('search_results', SearchResultsView.as_view(), name='search_results')
]
