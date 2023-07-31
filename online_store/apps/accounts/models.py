from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth import models as auth_models


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
    user = models.OneToOneField(StoreUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    discount_modifier = models.SmallIntegerField(default=1)


class Address(models.Model):
    user = models.ForeignKey(StoreUser, on_delete=models.CASCADE)
    country = models.CharField(max_length=56)
    state = models.CharField(max_length=60)
    city = models.CharField(max_length=60)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.city} {self.address} {self.country}"


class InvoiceData(models.Model):
    user = models.ForeignKey(StoreUser, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50)
    tax_id = models.CharField(max_length=50)
    billing_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    billing_name = models.CharField(max_length=100)
