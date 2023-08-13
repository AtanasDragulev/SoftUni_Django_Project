from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Group

from django.views import generic as views

from online_store.tools.access_control import AccessRequiredMixin, group_required
from online_store.apps.backoffice.forms import *
from online_store.apps.core.models import Product, Category
from online_store.apps.inventory.models import Delivery, Inventory
from online_store.apps.sales.models import Order, OrderItem

UserModel = get_user_model()


class Dashboard(AccessRequiredMixin, views.TemplateView):
    REQUIRED_GROUP = "Staff"
    template_name = 'backoffice/dashboard.html'


class CreateDelivery(AccessRequiredMixin, views.CreateView):
    REQUIRED_GROUP = "Staff"
    model = Delivery
    template_name = 'backoffice/delivery/create_delivery.html'
    success_url = reverse_lazy('dashboard')
    fields = '__all__'


@group_required("Staff")
def create_delivery_view(request):
    if request.method == 'POST':
        delivery_form = DeliveryForm(request.POST)
        forms_count = sum(1 for key in request.POST if key.startswith('form-')) / 5
        inventory_forms = [InventoryForm(request.POST, prefix=f'form-{i}') for i in range(int(forms_count))]

        if delivery_form.is_valid() and all(form.is_valid() for form in inventory_forms):
            if delivery_form.cleaned_data['cost'] != sum(form.cleaned_data['cost'] for form in inventory_forms):
                raise ValidationError("The total delivery amount is different from the sum of items cost")
            delivery = Delivery.objects.create(
                delivery_number=delivery_form.cleaned_data['delivery_number'],
                invoice_number=delivery_form.cleaned_data['invoice_number'],
                delivery_date=delivery_form.cleaned_data['delivery_date'],
                cost=delivery_form.cleaned_data['cost'],
                created_by=request.user
            )

            for form in inventory_forms:
                inventory = form.save(commit=False)

                product_slug = form.cleaned_data['product_slug']
                try:
                    product = Product.objects.get(slug=product_slug)
                    inventory.product = product
                    inventory.delivery = delivery
                    inventory.in_stock = True
                    inventory.save()
                except Product.DoesNotExist:
                    raise ValidationError('Product does not exist')

            return redirect('dashboard')
    else:
        delivery_form = DeliveryForm()
        inventory_forms = [InventoryForm(prefix=f'form-{i}') for i in range(1)]

    return render(request, 'backoffice/delivery/create_delivery.html', {
        'delivery_form': delivery_form,
        'inventory_forms': inventory_forms,
    })


class DeliveryList(AccessRequiredMixin, views.ListView):
    REQUIRED_GROUP = "Staff"
    model = Delivery
    template_name = 'backoffice/delivery/delivery_list.html'
    context_object_name = 'objects_list'


class DeliveryDetailView(AccessRequiredMixin, views.ListView):
    REQUIRED_GROUP = "Staff"
    model = Inventory
    template_name = 'backoffice/delivery/delivery_details.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        delivery_id = self.kwargs['delivery_id']
        return queryset.filter(delivery_id=delivery_id)


class UserManagement(AccessRequiredMixin, views.ListView):
    REQUIRED_GROUP = "Admins"
    model = UserModel
    template_name = 'backoffice/user/user_management.html'


class UserPermissionsView(AccessRequiredMixin, views.View):
    REQUIRED_GROUP = "Admins"
    template_name = 'backoffice/user/user_permissions.html'

    def get(self, request, user_pk):
        user = get_object_or_404(UserModel, pk=user_pk)
        groups = Group.objects.all()
        return render(request, self.template_name, {'user': user, 'groups': groups})

    def post(self, request, user_pk):
        user = get_object_or_404(UserModel, pk=user_pk)
        groups = Group.objects.all()
        for group in groups:
            is_checked = request.POST.get(group.name, False)
            if is_checked:
                user.groups.add(group)
            else:
                user.groups.remove(group)
        return redirect('manage_users')


class CategoryManagementView(AccessRequiredMixin, views.ListView):
    REQUIRED_GROUP = "Managers"
    model = Category
    template_name = 'backoffice/category/category_management.html'


class CreateCategoryView(AccessRequiredMixin, views.CreateView):
    REQUIRED_GROUP = "Managers"
    model = Category
    fields = ('name', 'parent_category', 'order',)
    template_name = 'backoffice/category/category_create.html'
    success_url = reverse_lazy('category_management')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['attribute_formset'] = CategoryAttributeFormSet(self.request.POST)
        else:
            context['attribute_formset'] = CategoryAttributeFormSet()
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        categories = Category.objects.filter(parent_category=None)
        form.fields['parent_category'].queryset = categories
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        context = self.get_context_data()
        attribute_formset = context['attribute_formset']
        category = form.save()
        if attribute_formset.is_valid():
            for form in attribute_formset:
                a = form
                if form.cleaned_data.get('name'):
                    attribute = form.save(commit=False)
                    attribute.category = category
                    attribute.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class EditCategoryView(AccessRequiredMixin, views.UpdateView):
    REQUIRED_GROUP = "Managers"
    model = Category
    fields = ('name', 'parent_category', 'order',)
    template_name = 'backoffice/category/category_edit.html'
    success_url = reverse_lazy('category_management')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        categories = Category.objects.filter(parent_category=None)
        categories.exclude(pk=self.object.pk)
        form.fields['parent_category'].queryset = categories
        return form


class ProductManagementView(AccessRequiredMixin, views.ListView):
    REQUIRED_GROUP = "Staff"
    model = Product
    template_name = 'backoffice/product/product_management.html'
    paginate_by = 15
    ordering = ['pk']


class CreateProductView(AccessRequiredMixin, views.CreateView):
    REQUIRED_GROUP = "Staff"
    model = Product
    fields = '__all__'
    template_name = 'backoffice/product/product_create.html'


class DeactivateProductView(AccessRequiredMixin, views.UpdateView):
    REQUIRED_GROUP = "Staff"
    model = Product
    fields = []
    template_name = 'backoffice/product/product_deactivate.html'
    success_url = reverse_lazy('product_management')

    def form_valid(self, form):
        self.object.active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@login_required
@group_required("Staff")
def edit_product(request, pk):
    product = Product.objects.get(pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductAttributeFormSet(request.POST, instance=product)
        if form.is_valid() and formset.is_valid():
            formset.save()
            form.save()
            return redirect('product_management')

    else:
        form = ProductForm(instance=product)
        formset = ProductAttributeFormSet(instance=product)

    context = {
        'product': product,
        'form': form,
        'formset': formset,
    }
    return render(request, 'backoffice/product/product_edit.html', context)


class DeleteProductView(AccessRequiredMixin, views.DeleteView):
    REQUIRED_GROUP = "Managers"
    model = Product
    template_name = 'backoffice/product/product_delete.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        has_items = Inventory.objects.filter(product=self.object).exists()
        context.update({'has_items': has_items})
        return context


class OrderManagementView(AccessRequiredMixin, views.ListView):
    REQUIRED_GROUP = "Staff"
    model = Order
    template_name = 'backoffice/order/order_management.html'


class OrderProcessView(AccessRequiredMixin, views.UpdateView):
    REQUIRED_GROUP = "Staff"
    model = Order
    template_name = 'backoffice/order/order_process.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders_view')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        order_items = OrderItem.objects.filter(order=self.object)
        context.update({'order_items': order_items})
        return context


class OrderItemEditView(AccessRequiredMixin, views.UpdateView):
    REQUIRED_GROUP = "Staff"
    model = OrderItem
    template_name = 'backoffice/order/orderitem_edit.html'
    fields = ['serial_number']

    def get_success_url(self):
        order = self.object.order
        return reverse('order_process', kwargs={"pk": order.pk})

    def form_valid(self, form):
        old_serial = self.get_object().serial_number
        new_serial = form.cleaned_data["serial_number"]

        old_item = Inventory.objects.get(serial_number=old_serial)
        old_item.in_stock = True
        old_item.save()

        new_item = Inventory.objects.get(serial_number=new_serial)
        new_item.in_stock = False
        new_item.save()

        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
