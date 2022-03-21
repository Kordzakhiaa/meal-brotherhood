from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.views import View

from accounts.models import Account
from mealbrotherhood.forms import RestaurantForm

from mealbrotherhood.models import Restaurant


# @TODO: At last disable for all users who have 'want_food'-field TRUE
# @TODO: dont want to eat button:))
# @TODO: user can pay or not


class HomeView(View):
    """ @TODO: DOC """
    template_name = 'meal_brotherhood/home.html'

    def get(self, request: WSGIRequest, *args, **kwargs):
        """ @TODO: doc """

        return render(request, self.template_name)

    def post(self, request: WSGIRequest, *args, **kwargs):
        """ @TODO: doc """

        user = Account.objects.get(id=request.user.id)
        user.want_food = True
        user.save()
        return redirect('meal_brotherhood:pays_or_not')


class CanPay(View):
    """ @TODO: DOC """
    template_name = 'meal_brotherhood/can_pay.html'

    def get(self, request: WSGIRequest, *args, **kwargs):
        """ @TODO: doc """

        return render(request, self.template_name)

    def post(self, request: WSGIRequest, *args, **kwargs):
        """ @TODO: doc """

        if request.POST['choice'] == 'დიახ':
            user = Account.objects.get(id=request.user.id)
            user.pays = True
            user.save()
        return redirect('meal_brotherhood:eating_place')


class EatingPlaceView(View):
    """ @TODO: doc """
    template_name = 'meal_brotherhood/location_choice.html'

    def get(self, request: WSGIRequest, *args, **kwargs):
        """ @TODO: DOC """

        return render(request, self.template_name)

    def post(self, request: WSGIRequest, *args, **kwargs):
        """ @TODO: DOC """

        if request.POST['location'] == 'გახსენით მენიუ':
            return render(request, self.template_name, {'error': 'გთხოვთ აირჩიოთ ადგილი თუ სად მიირთმევთ!'})

        user = Account.objects.get(id=request.user.id)
        eating_place = request.POST['location']
        print(eating_place)
        user.eating_location = eating_place
        user.save()

        return redirect('meal_brotherhood:restaurant_choices')


class RestaurantChoiceView(View):
    """ @TODO: DOC """
    template_name = 'meal_brotherhood/restaurant_choices.html'
    query = Restaurant.objects.all()

    def get(self, request: WSGIRequest, *args, **kwargs):
        # @TODO: Restrict this endpoint for users who dont want food (want_food=False)
        return render(request, self.template_name, {'restaurants': self.query})

    def post(self, request: WSGIRequest, *args, **kwargs):
        """ @TODO: doc """

        if request.POST['restaurant_name'] == 'გახსენით მენიუ':
            return render(request, self.template_name,
                          {'restaurants': self.query,
                           'error': 'გთხოვთ აირჩიოთ რესტორნის დასახელება!'})

        elif request.POST['restaurant_name'] == 'სხვა':
            return redirect('meal_brotherhood:add_restaurant')

        restaurant = Restaurant.objects.get(restaurant_name=request.POST['restaurant_name'])
        user = Account.objects.get(id=request.user.id)
        user.restaurant = restaurant
        user.save()

        return redirect('meal_brotherhood:home')


class CustomRestaurantChoiceView(View):
    """ @TODO: DOC """
    template_name = 'meal_brotherhood/custom_restaurant_choice.html'
    form = RestaurantForm

    def get(self, request: WSGIRequest, *args, **kwargs):
        # @TODO: Restrict this endpoint for users who dont want food (want_food=False)
        return render(request, self.template_name, {'form': self.form})

    def post(self, request, *args, **kwargs):
        """ @TODO: doc """
        form = self.form(request.POST)

        # @TODO: QUESTION -> form always invalid if given input is in DB  !!!!! DATA | DACHI
        if form.is_valid():
            inputted_restaurant: str = form.data.get('restaurant_name')

            if self.check_restaurant(inputted_restaurant):
                return render(request, self.template_name,
                              {'form': form, 'error': 'რესტორანი ამ დასახელებით უკვე არსებობს, სცადეთ თავიდან!'})

            restaurant = Restaurant.objects.create(restaurant_name=inputted_restaurant)
            user = Account.objects.get(id=request.user.id)
            user.restaurant = restaurant
            user.save()

        return redirect('meal_brotherhood:home')

    @staticmethod
    def check_restaurant(given_restaurant_name: str) -> bool:
        # @TODO: change code location:))
        try:
            if Restaurant.objects.get(restaurant_name__istartswith=given_restaurant_name):
                return True
        except Restaurant.DoesNotExist:
            return False
