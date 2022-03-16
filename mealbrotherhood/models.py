from django.db import models
from django.utils.translation import gettext_lazy as _


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.restaurant_name
