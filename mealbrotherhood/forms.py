from django import forms

from mealbrotherhood.models import Restaurant


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['restaurant_name']


class CustomRestaurantForm(forms.ModelForm):
    restaurant_name = forms.CharField(max_length=150, min_length=3)

    class Meta:
        model = Restaurant
        fields = ['restaurant_name']
