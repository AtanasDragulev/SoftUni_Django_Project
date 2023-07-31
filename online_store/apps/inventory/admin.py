from django.contrib import admin

from online_store.apps.inventory.models import Inventory, Delivery, Supplier


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    pass


@admin.register(Delivery)
class InventoryAdmin(admin.ModelAdmin):

    class Meta:
        verbose_name_plural = 'Categories'
