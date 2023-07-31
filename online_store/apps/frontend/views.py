from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView, FormView
from django.views.generic.base import TemplateView

from .forms import ProductCreationForm, ProductForm, ProductAttributeFormSet, SearchForm
from ..accounts.access_control import AccessRequiredMixin, group_required

from ..core.models import Category, Product, ProductAttribute

main_categories = Category.objects.filter(parent_category__isnull=True)


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_form = SearchForm
        context.update({'search_form': search_form})
        return context


class CategoryProductsView(TemplateView):
    template_name = 'frontend/category_products.html'

    def get_context_data(self, category_name, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(name=category_name)
        products = Product.objects.filter(category=category)
        context.update({'category': category, 'products': products, })
        return context


@login_required
@group_required("Staff")
def create_product(request, category_name):
    category = Category.objects.get(name=category_name)

    if request.method == 'POST':
        form = ProductCreationForm(category, request.POST, request.FILES)
        if form.is_valid():
            product = Product.objects.create(
                name=form.cleaned_data['name'],
                brand=form.cleaned_data['brand'],
                category=category,
                image=form.cleaned_data['image'],
                description=form.cleaned_data['description'],
                price=form.cleaned_data['price'],
                created_by=form.cleaned_data['created_by']
            )
            for attribute in category.categoryattribute_set.all():
                attribute_value = form.cleaned_data[attribute.name]
                ProductAttribute.objects.create(product=product, name=attribute.name, value=attribute_value)
            product.save(update_fields=['title'])
            return redirect('category_products',
                            category_name=category_name)  # Redirect to a success page after product creation
    else:
        form = ProductCreationForm(category)

    context = {
        'form': form,
    }

    return render(request, 'frontend/create_product.html', context)


class ProductDetailView(TemplateView):
    template_name = 'frontend/product_detail.html'

    def get_context_data(self, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, slug=slug)
        attributes = product.productattribute_set.all()
        context.update({'product': product, 'attributes': attributes})
        return context


@login_required
@group_required("Staff")
def edit_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductAttributeFormSet(request.POST, instance=product)
        if form.is_valid() and formset.is_valid():
            formset.save()
            form.save()
            return redirect('category_products', product.category.name)
    else:
        form = ProductForm(instance=product)
        formset = ProductAttributeFormSet(instance=product)

    context = {
        'product': product,
        'form': form,
        'formset': formset,
    }
    return render(request, 'frontend/product_edit.html', context)


class ProductDeleteView(AccessRequiredMixin, DeleteView):
    REQUIRED_GROUP = "Admins"
    model = Product
    template_name = 'frontend/product_delete.html'

    def get_success_url(self):
        product = self.get_object()
        return reverse_lazy('category_products', kwargs={'category_name': product.category.name})


class SearchResultsView(FormView):
    template_name = 'frontend/search_results.html'
    form_class = SearchForm
    model = Product

    def form_valid(self, form):
        query = form.cleaned_data['query']
        results = self.model.objects.filter(title__icontains=query)
        context = self.get_context_data(form=form, results=results)
        return self.render_to_response(context)
