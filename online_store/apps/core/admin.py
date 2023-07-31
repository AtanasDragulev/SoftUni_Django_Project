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
    pass


@admin.register(CategoryAttribute)
class CategoryAttributeAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    pass
