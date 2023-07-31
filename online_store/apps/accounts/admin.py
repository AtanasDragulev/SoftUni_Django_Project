from django.contrib import admin
from django.contrib.auth import get_user_model

from online_store.apps.accounts.models import StoreUser, Profile, Address

UserModel = get_user_model()


@admin.register(StoreUser)
class UsersAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass