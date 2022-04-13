from django.db import models

from accounts.models import Account


class Restaurant(models.Model):
    restaurant_name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.restaurant_name


class Question(models.Model):
    user = models.ForeignKey(to=Account, on_delete=models.CASCADE)
    want_eat = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} want_eat={self.want_eat} {self.created_date}'


class Poll(models.Model):
    class InRestaurantOrInOffice(models.TextChoices):
        IN_RESTAURANT = 'რესტორანში', 'რესტორანში'
        IN_OFFICE = 'ოფისში', 'ოფისში'

    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(to=Restaurant, on_delete=models.SET_NULL, null=True, blank=True)
    menu = models.TextField()

    pays_or_not = models.BooleanField(default=False)
    eating_location = models.CharField(max_length=150, choices=InRestaurantOrInOffice.choices,
                                       default=InRestaurantOrInOffice.IN_RESTAURANT)

    def __str__(self):
        return f'{self.question.user.first_name} -> {self.restaurant}'
