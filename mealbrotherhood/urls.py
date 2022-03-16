from django.contrib.auth.decorators import login_required as lr
from django.urls import path

from mealbrotherhood.views import HomeView, RestaurantView, EatingPlaceView

app_name: str = 'meal_brotherhood'

urlpatterns = [
    path('', lr(HomeView.as_view()), name='home'),
    path('eating_place/', lr(EatingPlaceView.as_view()), name='eating_place'),
    path('restaurant_choices/', lr(RestaurantView.as_view()), name='restaurant_choices'),
]
