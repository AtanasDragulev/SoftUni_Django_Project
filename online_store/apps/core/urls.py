from django.urls import path
from . import views

urlpatterns = [
    path('get_product/<int:product_id>/', views.get_product_details, name='get_product_details'),
]