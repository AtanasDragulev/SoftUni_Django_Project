from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import Group

from django.views import generic as views

from online_store.apps.backoffice.forms import DeliveryForm, InventoryForm
from online_store.apps.core.models import Product, Category
from online_store.apps.inventory.models import Delivery
from online_store.apps.sales.models import Order

UserModel = get_user_model()


# Create your views here.
class Dashboard(views.TemplateView):
    template_name = 'backoffice/dashboard.html'


class CreateDelivery(views.CreateView):
    model = Delivery
    template_name = 'backoffice/create_delivery.html'
    success_url = reverse_lazy('dashboard')
    fields = '__all__'


def create_delivery_view(request):
    if request.method == 'POST':
        delivery_form = DeliveryForm(request.POST)
        inventory_forms = [InventoryForm(request.POST, prefix=f'form-{i}') for i in range(3)]
        if delivery_form.is_valid() and all(form.is_valid() for form in inventory_forms):
            delivery = delivery_form.save()

            for form in inventory_forms:
                inventory = form.save(commit=False)

                product_slug = form.cleaned_data['product_slug']
                try:
                    product = Product.objects.get(slug=product_slug)
                    inventory.product = product  # Assign the product instance to the inventory item
                    inventory.delivery = delivery
                    inventory.save()
                except Product.DoesNotExist:
                    # Handle the case where the product does not exist (optional)
                    print(f"Product with slug '{product_slug}' does not exist.")
                    continue

            # Redirect to a success page or do something else
            return redirect('dashboard')
    else:
        delivery_form = DeliveryForm()
        inventory_forms = [InventoryForm(prefix=f'form-{i}') for i in range(3)]

    return render(request, 'backoffice/create_delivery.html', {
        'delivery_form': delivery_form,
        'inventory_forms': inventory_forms,
    })


class DeliveryList(views.ListView):
    model = Delivery
    paginate_by = 30
    template_name = 'backoffice/delivery_list.html'
    context_object_name = 'objects_list'


class UserManagement(views.ListView):
    model = UserModel
    template_name = 'backoffice/user_management.html'
    paginate_by = 20


class UserPermissionsView(views.View):
    template_name = 'backoffice/user_permissions.html'

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


class CategoryManagementView(views.ListView):
    model = Category
    template_name = 'backoffice/category_management.html'


class CreateCategoryView(views.CreateView):
    model = Category


class EditCategoryView(views.UpdateView):
    model = Category
    fields = ('name', 'parent_category', 'order',)
    template_name = 'backoffice/category_edit.html'
    success_url = reverse_lazy('category_management')


class ProductManagementView(views.ListView):
    model = Product
    template_name = 'backoffice/product_management.html'


class CreateProductView(views.CreateView):
    model = Product
    fields = '__all__'
    template_name = 'backoffice/product_create.html'


class EditProductView(views.UpdateView):
    model = Product
    fields = ('name', 'parent_category', 'order',)


class OrderManagementView(views.ListView):
    model = Order
    template_name = 'backoffice/order_management.html'
