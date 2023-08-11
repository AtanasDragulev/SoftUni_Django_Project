from django import forms
from django.core.validators import MinLengthValidator, MinValueValidator
from django.forms import inlineformset_factory
from django.template.defaultfilters import slugify

from online_store.apps.core.models import CategoryAttribute, Brand, Product, ProductAttribute
from online_store.tools.custom_validators import validate_image_size


class ProductCreationForm(forms.Form):
    NAME_MAX_LENGTH = 60
    NAME_MIN_LENGTH = 2

    def __init__(self, category, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(
            label='Product Name', validators=(
                MinLengthValidator(
                    ProductCreationForm.NAME_MIN_LENGTH,
                    message=f"The product name must be a minimum of {ProductCreationForm.NAME_MIN_LENGTH} chars"),)
        )
        self.fields['brand'] = forms.ModelChoiceField(label='Brand', queryset=Brand.objects.all())
        self.fields['category'] = forms.CharField(label='Category', disabled=True, initial=category.name)
        self.fields['image'] = forms.ImageField(label='Product Image', validators=(validate_image_size,))
        self.fields['description'] = forms.CharField(widget=forms.Textarea, label='Product Description')
        self.fields['price'] = forms.DecimalField(
            label='Product Price', validators=(
                MinValueValidator(0.1, message="Product price cannot be negative or zero"),)
        )

        self.category = category
        category_attributes = CategoryAttribute.objects.filter(category=category)
        for attribute in category_attributes:
            self.fields[attribute.name] = forms.CharField(empty_value=attribute.name)

    def clean(self):
        cleaned_data = super().clean()
        brand = cleaned_data.get('brand')
        name = cleaned_data.get('name')
        slug = slugify(f"{brand}-{name}")

        if Product.objects.filter(slug=slug).exists():
            self.add_error('name', "Combination of brand and product name should be unique.")
        cleaned_data['slug'] = slug

        return cleaned_data


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'category', 'image', 'description', 'price']


ProductAttributeFormSet = inlineformset_factory(Product, ProductAttribute, fields=('name', 'value'), extra=1)


class ProductAttributeForm(forms.ModelForm):
    class Meta:
        model = ProductAttribute
        fields = ['name', 'value']


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, label='')
