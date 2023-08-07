from django.contrib import admin

from online_store.apps.inventory.models import Inventory, Delivery


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'serial_number', 'in_stock', 'cost', 'date_created',)
    ordering = ("-in_stock", 'date_created')
    list_filter = ("in_stock", 'date_created', 'cost')


@admin.register(Delivery)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('delivery_date', 'delivery_number', 'invoice_number', 'cost', 'created_by',)
    ordering = ("delivery_date", 'delivery_number')
    list_filter = ("delivery_date",)
    search_fields = ("delivery_number",)

    class Meta:
        verbose_name_plural = 'Deliveries'
