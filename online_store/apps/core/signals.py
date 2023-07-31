from django.db.models.signals import post_save
from django.dispatch import receiver

from online_store.apps.core.models import Product, CategoryAttribute, ProductAttribute
from online_store.apps.inventory.models import Inventory


# Creates product attributes for product form cattegory attributes when created in admin site
# @receiver(post_save, sender=Product)
# def add_attributes_to_product(sender, instance, created, **kwargs):
#     print(sender)
#     if created:
#         category_attributes = CategoryAttribute.objects.filter(category=instance.category)
#         for category_attribute in category_attributes:
#             ProductAttribute.objects.create(product=instance, name=category_attribute)

# @receiver(post_save, sender=Product)
# def add_attributes_to_product(sender, instance, created, **kwargs):
#     if created:
#         product_attributes = ProductAttribute.objects.filter(product=instance.pk)[0:5]
#         instance.title = f"{instance.brand.name} {instance.name},"
#         instance.title += ", ".join(a.value for a in product_attributes)
#         print("------------------------------------------------------------------------------------------------")
#         print(product_attributes)
#         print("------------------------------------------------------------------------------------------------")
#         instance.save(update_fields=['title'])

@receiver(post_save, sender=Inventory)
def increase_product_quantity(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        product.quantity += 1
        product.save(update_fields=['quantity'])

