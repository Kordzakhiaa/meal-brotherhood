from django import forms

from mealbrotherhood.models import Restaurant


class RestaurantForm(forms.ModelForm):
    restaurant_name = forms.CharField(max_length=250, label='დასახელება')

    class Meta:
        model = Restaurant
        fields = ['restaurant_name']
