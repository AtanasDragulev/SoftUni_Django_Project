from django.contrib import admin

from online_store.apps.sales.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('date_ordered', 'customer', 'complete', 'payment_type', 'get_total',)
    ordering = ("-date_ordered", 'complete')
    list_filter = ("complete", 'date_ordered', 'payment_type')


@admin.register(OrderItem)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('date_added', 'order', 'product', 'serial_number', 'price',)
    ordering = ("order", 'date_added')
    list_filter = ("date_added", 'order', 'product')
