from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'account'

urlpatterns = [
    path('login', views.LoginView.as_view(), name="login"),
    path('signup', views.SignUpView.as_view(), name="signup"),
    path('waiting', views.WaitingView.as_view(), name="waiting"),
    path('profile', login_required(views.ProfileView.as_view()), name="profile"),
    path('logout', login_required(views.LogoutView.as_view()), name="logout")
]
