from django.contrib.auth import views as auth_views, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.views import generic as views

from online_store.apps.accounts.forms import RegisterUserForm, AddAddressForm
from online_store.apps.accounts.models import Profile, Address

UserModel = get_user_model()


class RegisterUserView(views.CreateView):
    template_name = 'accounts/register.html'
    form_class = RegisterUserForm

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result

    def get_success_url(self):
        pk = self.object.pk

        return reverse_lazy('edit_profile', kwargs={'pk': pk})


class LoginUserView(auth_views.LoginView):
    template_name = 'accounts/login.html'


class LogoutUserView(auth_views.LogoutView):
    pass


class ProfileDetails(views.DetailView):
    model = Profile
    template_name = 'accounts/profile.html'
    fields = '__all__'


class ProfileEdit(views.UpdateView):
    model = Profile
    template_name = 'accounts/profile_edit.html'
    fields = ('first_name', 'last_name',)

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('profile_details', kwargs={'pk': pk})


class AddAdressView(LoginRequiredMixin, views.CreateView):
    template_name = 'accounts/add_address.html'
    form_class = AddAddressForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        pk = self.request.user.pk
        return reverse_lazy('profile_details', kwargs={'pk': pk})


class DeleteAddressView(LoginRequiredMixin, views.DeleteView):
    template_name = 'accounts/delete_address.html'
    model = Address

    def get_success_url(self):
        pk = self.request.user.pk
        return reverse_lazy('profile_details', kwargs={'pk': pk})
