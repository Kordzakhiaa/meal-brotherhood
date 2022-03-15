from django.urls import path

from accounts.views import RegisterView, LoginView, HomeView, GetPerm

app_name: str = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('perm/', GetPerm.as_view(), name='perm'),
]
