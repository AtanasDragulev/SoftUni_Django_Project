from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify

User = get_user_model()


class Category(models.Model):
    NAME_MAX_LENGTH = 30
    NAME_MIN_LENGTH = 2

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(NAME_MIN_LENGTH,
                               message=f"The category name must be a minimum of {NAME_MIN_LENGTH} chars"),
        ))

    parent_category = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.RESTRICT,
        validators=[]

    )
    order = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, related_name='created_categories')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class CategoryAttribute(models.Model):
    NAME_MAX_LENGTH = 30
    NAME_MIN_LENGTH = 2

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(NAME_MIN_LENGTH,
                               message=f"The attribute name must be a minimum of {NAME_MIN_LENGTH} chars"),)
    )

    def __str__(self):
        return self.name


class Brand(models.Model):
    NAME_MAX_LENGTH = 30
    NAME_MIN_LENGTH = 2

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(NAME_MIN_LENGTH,
                               message=f"The brand name must be a minimum of {NAME_MIN_LENGTH} chars"),)
    )
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    NAME_MAX_LENGTH = 60
    NAME_MIN_LENGTH = 2

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(NAME_MIN_LENGTH,
                               message=f"The product name must be a minimum of {NAME_MIN_LENGTH} chars"),)
    )
    brand = models.ForeignKey(Brand, default="1", on_delete=models.SET_DEFAULT)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to="product_images/", null=True, blank=True)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=(MinValueValidator(0.01, message="Product price cannot be negative or zero"),)
    )
    quantity = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, related_name='created_products')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(f"{self.brand}-{self.name}")

        old_title = self.title
        product_attributes = ProductAttribute.objects.filter(product=self.pk)[:5]
        new_title = f"{self.brand.name} {self.name}, "
        new_title += ", ".join(a.value for a in product_attributes)
        if old_title != new_title:
            self.title = new_title

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand.name}-{self.name}"


class ProductAttribute(models.Model):
    NAME_MAX_LENGTH = 30
    NAME_MIN_LENGTH = 2
    VALUE_MAX_LENGTH = 30
    VALUE_MIN_LENGTH = 1

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(NAME_MIN_LENGTH,
                               message=f"The attribute name must be a minimum of {NAME_MIN_LENGTH} chars"),)
    )
    value = models.CharField(
        max_length=VALUE_MAX_LENGTH,
        validators=(
            MinLengthValidator(NAME_MIN_LENGTH,
                               message=f"The attribute value must be a minimum of {VALUE_MIN_LENGTH} chars"),)
    )

    def __str__(self):
        return f"{self.product} - {self.name}: {self.value}"


class ProductLike(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)