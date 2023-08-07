from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import models as auth_models

from online_store.tools.custom_validators import validate_characters_only, validate_characters_digits_only, \
    validate_numbers_plus_sign_only


class StoreUserManager(auth_models.BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given username must be set")

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class StoreUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_FIELD = 'email'

    objects = StoreUserManager()

    email = models.EmailField(
        null=False,
        blank=False,
        unique=True,

    )

    is_staff = models.BooleanField(
        default=False,
    )


class Profile(models.Model):
    FIRST_NAME_MAX_LENGTH = 50
    FIRST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 50
    LAST_NAME_MIN_LENGTH = 2

    user = models.OneToOneField(StoreUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH,
                               message=f"First name cannot have less than {FIRST_NAME_MIN_LENGTH} characters"),
            validate_characters_only,
        )
    )
    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH,
                               message=f"Last name cannot have less than {LAST_NAME_MIN_LENGTH} characters"),
            validate_characters_only,
        )
    )
    discount_modifier = models.SmallIntegerField(default=1)

    def __str__(self):
        return f"{self.user}"


class Address(models.Model):
    COUNTRY_MAX_LENGTH = 56
    COUNTRY_MIN_LENGTH = 4

    user = models.ForeignKey(StoreUser, on_delete=models.CASCADE)
    country = models.CharField(
        max_length=COUNTRY_MAX_LENGTH,
        validators=(
            MinLengthValidator(COUNTRY_MIN_LENGTH,
                               message=f"There is no country with less than {COUNTRY_MIN_LENGTH} characters"),
            validate_characters_only,
        )
    )
    state = models.CharField(max_length=60, validators=(validate_characters_only,))
    city = models.CharField(max_length=60, validators=(validate_characters_only,))
    address = models.CharField(max_length=100, validators=(validate_characters_digits_only,))
    postal_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15, validators=(validate_numbers_plus_sign_only,))
    primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.city} {self.address} {self.country}"
