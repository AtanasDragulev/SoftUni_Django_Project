from django.contrib import admin
from django.contrib.auth import get_user_model

from online_store.apps.accounts.custom_admin.filters import GroupFilter
from online_store.apps.accounts.models import StoreUser, Profile, Address

UserModel = get_user_model()


@admin.register(StoreUser)
class UsersAdmin(admin.ModelAdmin):
    list_filter = ('is_staff', 'is_superuser', GroupFilter)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', ]



@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['city', 'address', 'state', 'country', ]
    list_filter = ('country', 'city')
