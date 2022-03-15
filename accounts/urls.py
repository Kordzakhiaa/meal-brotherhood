from django.urls import path

from accounts.views import RegisterView, LoginView, logout_page

app_name: str = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_page, name='logout'),
]
