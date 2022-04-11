from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.views import View

from accounts.models import Account
from mealbrotherhood.forms import RestaurantForm, PollForm

from mealbrotherhood.models import Restaurant, Question, Poll


# @TODO: dont want to eat button:))
# @TODO: add account number and show it on home page for all users

class HomeView(View):
    template_name = 'meal_brotherhood/home.html'

    def get(self, request: WSGIRequest, *args, **kwargs):
        polls = Poll.objects.all()
        data: dict = {}

        # for restaurant in restaurants:
        #     for user in users:
        #         if  restaurant == user.restaurant:
        #             data[restaurant] = Account.objects.filter(restaurant=restaurant)

        return render(request, self.template_name, {'polls': polls})


class WantFoodOrNotChoiceView(View):
    template_name = 'meal_brotherhood/want_food.html'

    def get(self, request: WSGIRequest, *args, **kwargs):
        """ @TODO: doc """

        return render(request, self.template_name)

    def post(self, request: WSGIRequest, *args, **kwargs):
        """ @TODO: doc """

        if request.POST.get('choice') == 'დიახ':
            Question.objects.create(user_id=request.user.id, want_eat=True)
            return redirect('meal_brotherhood:meal_questionnaire')
        return redirect('meal_brotherhood:home')


class MealQuestionnaireView(View):
    """ @TODO: DOC """
    template_name = 'meal_brotherhood/meal_questionnaire.html'
    form = PollForm

    def get(self, request: WSGIRequest, *args, **kwargs):
        """ @TODO: doc """

        return render(request, self.template_name, {'form': self.form})

    def post(self, request: WSGIRequest, *args, **kwargs):
        """ @TODO: doc """
        form = self.form(request.POST)

        if form.is_valid():
            # @TODO: Check if user has already chosen...
            choice = form.save(commit=False)
            choice.question = Question.objects.order_by('-created_date').filter(user_id=request.user.id).first()
            choice.save()

        return redirect('meal_brotherhood:home')


class CanPay(View):
    """ @TODO: DOC """
    template_name = 'meal_brotherhood/can_pay.html'

    def get(self, request: WSGIRequest, *args, **kwargs):
        """ @TODO: doc """

        return render(request, self.template_name)

    def post(self, request: WSGIRequest, *args, **kwargs):
        """ @TODO: doc """
        user = Account.objects.get(id=request.user.id)

        if request.POST['choice'] == 'დიახ':
            user.pays = True
            user.save()
            return redirect('meal_brotherhood:eating_place')

        # IF CHOICE == 'არა' (NO)
        user.pays = False
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
