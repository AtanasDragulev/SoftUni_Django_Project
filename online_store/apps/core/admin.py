from django.contrib import admin

from .models import Category, Brand, Product, CategoryAttribute, ProductAttribute


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('indented_name',)
    ordering = ("order", 'created_at')

    def indented_name(self, obj):
        if obj.parent_category_id is not None:
            return f'--- {obj.name}'
        return f'{obj.name}'

    indented_name.short_description = 'Category'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'brand', 'name', 'quantity', 'price', 'created_by')
    ordering = ("category", '-quantity')
    list_filter = ('category', 'brand', )


@admin.register(CategoryAttribute)
class CategoryAttributeAdmin(admin.ModelAdmin):
    list_display = ('category', 'name')
    ordering = ("category", 'name')
    list_filter = ('category', )


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'value')
    ordering = ("product", )
    list_filter = ('product', 'name', 'value')
