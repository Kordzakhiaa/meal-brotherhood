from django import forms

from mealbrotherhood.models import Restaurant, Question, Poll


class RestaurantForm(forms.ModelForm):
    restaurant_name = forms.CharField(max_length=250, label='დასახელება')

    class Meta:
        model = Restaurant
        fields = ['restaurant_name']


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['restaurant', 'menu', 'eating_location', 'pays_or_not']
