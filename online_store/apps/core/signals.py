from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from online_store.apps.inventory.models import Inventory
from online_store.apps.sales.models import Order

User = get_user_model()


@receiver(post_save, sender=Inventory)
def increase_product_quantity(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        product.quantity += 1
        product.save(update_fields=['quantity'])


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Our Website'
        message = 'Thank you for joining our website!'
        from_email = 'your_email@gmail.com'
        recipient_list = [instance.email]

        send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=Order)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = f'Order {instance.id} created'
        message = f'Thank you for shopping from us\nYour order number is {instance.id}'
        from_email = 'your_email@gmail.com'
        recipient_list = [instance.customer.email]

        send_mail(subject, message, from_email, recipient_list)