from django.urls import path

from online_store.apps.backoffice.views import *

urlpatterns = (
    path('', Dashboard.as_view(), name='dashboard'),
    path('delivery/create', create_delivery_view, name='create_delivery'),
    path('delivery/view', DeliveryList.as_view(), name='view_delivery'),
    path('orders/view', OrderManagementView.as_view(), name='orders_view'),
    path('orders/process', OrderManagementView.as_view(), name='order_process'),
    path('categories', CategoryManagementView.as_view(), name='category_management'),
    path('categories/edit/<int:pk>', EditCategoryView.as_view(), name='category_edit'),
    path('products', ProductManagementView.as_view(), name='product_management'),
    path('products/create', CreateProductView.as_view(), name='product_create'),
    path('products/edit', EditProductView.as_view(), name='product_edit'),
    path('admin/users', UserManagement.as_view(), name='manage_users'),
    path('admin/users/edit/<int:user_pk>', UserPermissionsView.as_view(), name='user_permissions'),

)
