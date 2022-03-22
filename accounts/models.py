from django.core.validators import validate_email
from django.db import models

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from mealbrotherhood.models import Restaurant


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        validate_email(email)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class Account(AbstractUser):
    """ Custom user model """

    class InRestaurantOrInOffice(models.TextChoices):
        NONE: str = 'None', 'None',
        IN_RESTAURANT: str = 'რესტორანში', ('რესტორანში')
        IN_OFFICE: str = 'ოფისში', ('ოფისში')

    username = None
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    # @TODO: create new model for restaurant, eating_location, want_food and pays or not
    restaurant = models.ForeignKey(to=Restaurant, on_delete=models.SET_NULL, null=True, blank=True)

    eating_location = models.CharField(max_length=150, choices=InRestaurantOrInOffice.choices,
                                       default=InRestaurantOrInOffice.NONE)
    want_food = models.BooleanField(default=False)
    pays = models.BooleanField(default=False)

    objects = AccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
