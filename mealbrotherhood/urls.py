from django.contrib.auth.decorators import login_required as lr
from django.urls import path

from mealbrotherhood.views import MealQuestionnaireView, HomeView, WantFoodOrNotChoiceView

app_name: str = 'meal_brotherhood'

urlpatterns = [
    path('', lr(HomeView.as_view()), name='home'),
    path('meal_questionnaire/', lr(MealQuestionnaireView.as_view()), name='meal_questionnaire'),
    path('want_food/', lr(WantFoodOrNotChoiceView.as_view()), name='want_food_or_not'),
]
