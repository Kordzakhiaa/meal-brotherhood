from django.contrib.auth.decorators import login_required as lr
from django.urls import path

from accounts.decorators import restrict_access
from accounts.views import RegisterView, LoginView, UserProfileView, LogoutPageView

app_name: str = 'accounts'

urlpatterns = [
    path('register/', (RegisterView.as_view()), name='register'),
    path('login/', (LoginView.as_view()), name='login'),
    path('logout/', lr(LogoutPageView.as_view()), name='logout'),

    path('profile/', lr(UserProfileView.as_view()), name='user_profile'),
]
