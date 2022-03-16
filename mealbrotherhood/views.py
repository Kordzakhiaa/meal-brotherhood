from django.shortcuts import render, redirect
from django.views import View

from accounts.models import Account
from mealbrotherhood.forms import RestaurantForm

from mealbrotherhood.models import Restaurant


# @TODO: At last disable for all users who have 'want_food'-field TRUE

class HomeView(View):
    """ @TODO: DOC """
    template_name = 'meal_brotherhood/home.html'

    def get(self, request, *args, **kwargs):
        """ @TODO: doc """

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        """ @TODO: doc """

        user = Account.objects.get(id=request.user.id)
        user.want_food = True
        user.save()
        return redirect('meal_brotherhood:eating_place')


class EatingPlaceView(View):
    """ @TODO: doc """
    template_name = 'meal_brotherhood/location_choice.html'

    def get(self, request, *args, **kwargs):
        """ @TODO: DOC """

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        """ @TODO: DOC """

        if request.POST['location'] == 'გახსენით მენიუ':
            return render(request, self.template_name, {'error': 'გთხოვთ აირჩიოთ ადგილი თუ სად მიირთმევთ!'})
        user = Account.objects.get(id=request.user.id)
        eating_place = request.POST['location']
        user.eating_location = eating_place
        user.save()

        return redirect('meal_brotherhood:restaurant_choices')


class RestaurantView(View):
    """ @TODO: DOC """
    template_name = 'meal_brotherhood/restaurant_choices.html'
    query = Restaurant.objects.all()

    def get(self, request, *args, **kwargs):
        # @TODO: Restrict this endpoint for users who dont want food (want_food=False)
        return render(request, self.template_name,
                      {'want_food': request.user.want_food, 'restaurants': self.query})

    def post(self, request, *args, **kwargs):
        """ @TODO: doc """
        user = Account.objects.get(id=request.user.id)

        if request.POST['restaurant_name'] == 'გახსენით მენიუ':
            return render(request, self.template_name,
                          {'restaurants': self.query, 'error': 'გთხოვთ აირჩიოთ რესტორნის დასახელება!'})

        restaurant = Restaurant.objects.get(restaurant_name=request.POST['restaurant_name'])
        user.restaurant = restaurant
        user.save()

        return redirect('meal_brotherhood:home')
