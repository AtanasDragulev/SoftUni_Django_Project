from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView, FormView
from django.views.generic.base import TemplateView

from .forms import ProductCreationForm, ProductForm, ProductAttributeFormSet, SearchForm
from online_store.tools.access_control import AccessRequiredMixin, group_required

from ..core.models import Category, Product, ProductAttribute, ProductLike, Wishlist
from online_store.tools.functions import get_attribute_filters
from ..inventory.models import Inventory

main_categories = Category.objects.filter(parent_category__isnull=True)


class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_form = SearchForm
        context.update({'search_form': search_form})
        return context


class CategoryProductsView(TemplateView):
    template_name = 'frontend/catalogue/category_products.html'

    def get_context_data(self, category_name, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(name=category_name)
        products = Product.objects.filter(category=category, active=True)
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
                created_by=request.user
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

    return render(request, 'frontend/product/create_product.html', context)


class ProductDetailView(TemplateView):
    template_name = 'frontend/product/product_detail.html'

    def get_context_data(self, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, slug=slug)
        attributes = product.productattribute_set.all()
        liked = ProductLike.objects.filter(product=product, user=self.request.user).exists()
        wished = Wishlist.objects.filter(product=product, user=self.request.user).exists()
        total_likes = product.productlike_set.count()
        context.update(
            {'product': product,
             'attributes': attributes,
             'total_likes': total_likes,
             'liked': liked,
             'wished': wished,
             }
        )
        return context


@login_required
@group_required("Staff")
def edit_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if product.created_by != request.user:
        raise PermissionDenied
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
    return render(request, 'frontend/product/product_edit.html', context)


class ProductDeleteView(AccessRequiredMixin, DeleteView):
    REQUIRED_GROUP = "Staff"
    model = Product
    template_name = 'frontend/product/product_delete.html'

    def get_success_url(self):
        product = self.get_object()
        return reverse_lazy('category_products', kwargs={'category_name': product.category.name})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        has_items = Inventory.objects.filter(product=product).exists()
        context.update({'canot_delete': has_items, "message": 'You cannot delete product that has items'})
        if product.created_by != self.request.user:
            context.update({'canot_delete': True, "message": 'You are not the product creator'})
        return context


class SearchResultsView(FormView):
    template_name = 'frontend/catalogue/search_results.html'
    form_class = SearchForm
    model = Product

    def form_valid(self, form):
        query = form.cleaned_data['query']
        results = self.model.objects.filter(title__icontains=query)
        context = self.get_context_data(form=form, results=results)
        return self.render_to_response(context)


def products_by_category(request, category_name):
    category = Category.objects.get(name=category_name)
    products = Product.objects.filter(category=category, active=True)
    attributes = ProductAttribute.objects.filter(product__category=category).order_by('product__modified_at')
    attribute_groups = get_attribute_filters(attributes)
    paginator = Paginator(products, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':

        filtered_products = []
        filter_set = request.POST

        for name, value in filter_set.items():
            filtered_products.append(set(products.filter(productattribute__name=name, productattribute__value=value)))

        if len(filtered_products) > 1:
            products = list(set.intersection(*map(set, [x for x in filtered_products if x])))
            attributes = ProductAttribute.objects.filter(product__category=category)
            attribute_groups = get_attribute_filters(attributes)
            paginator = Paginator(products, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'products': products,
        'attribute_groups': attribute_groups,
        'page_obj': page_obj,

    }
    return render(request, 'frontend/catalogue/category_products.html', context)


@login_required
def like_product(request, slug):
    product = Product.objects.get(slug=slug)

    kwargs = {
        'product': product,
        'user': request.user
    }

    liked = ProductLike.objects \
        .filter(**kwargs) \
        .first()

    if liked:
        liked.delete()
    else:
        new_like_object = ProductLike(**kwargs)
        new_like_object.save()

    return redirect(request.META['HTTP_REFERER'] + f"#{slug}")


@login_required
def add_wishlist(request, slug):
    product = Product.objects.get(slug=slug)

    kwargs = {
        'product': product,
        'user': request.user
    }

    wished = Wishlist.objects \
        .filter(**kwargs) \
        .first()

    if wished:
        wished.delete()
    else:
        new_wished_object = Wishlist(**kwargs)
        new_wished_object.save()

    return redirect(request.META['HTTP_REFERER'] + f"#{slug}")
