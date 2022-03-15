from django.shortcuts import render, redirect
from django.views import View

from accounts.models import Account


# @TODO: At last disable for all users who have 'want_food'-field TRUE

class HomeView(View):
    template_name = 'meal_brotherhood/home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        user = Account.objects.get(id=request.user.id)
        user.want_food = True
        user.save()
        return redirect('meal_brotherhood:restaurant_choices')


class RestaurantView(View):
    template_name = 'meal_brotherhood/restaurant_choices.html'

    def get(self, request, *args, **kwargs):
        # @TODO: Restrict this endpoint for users who dont want food (want_food=False)
        return render(request, self.template_name, {'want_food': request.user.want_food})
