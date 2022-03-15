from django.urls import path

from accounts.views import RegisterView, LoginView, HomeView, GetPerm

app_name: str = 'meal_brotherhood'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
