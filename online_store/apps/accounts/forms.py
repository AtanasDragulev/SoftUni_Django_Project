from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.utils.translation import gettext_lazy as _
from online_store.apps.accounts.models import Profile, Address

UserModel = get_user_model()


class RegisterUserForm(auth_forms.UserCreationForm):
    password2 = forms.CharField(
        label=_("Repeat Password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Repeat password, please"),
    )

    def save(self, commit=True):
        user = super().save(commit)

        profile = Profile(
            user=user,
        )
        if commit:
            profile.save()

        return user

    class Meta(auth_forms.UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)


GROUP_CHOICES = (
    ('clients', 'Clients'),
    ('staff', 'Staff'),
    ('management', 'Management'),
    ('administration', 'Administration'),
)


class AddAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ("country", "state", "city", "address", "postal_code", "phone_number")
