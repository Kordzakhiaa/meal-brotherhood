from django.urls import path

from accounts.views import RegisterView, LoginView, logout_page, UserProfileView

app_name: str = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_page, name='logout'),

    path('profile/', UserProfileView.as_view(), name='user_profile'),
]
