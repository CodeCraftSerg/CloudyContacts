from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from . import views
from .forms import LoginForm

app_name = "users"

urlpatterns = [
    path(
        "signup",
        views.RegisterView.as_view(),
        name="signup",
    ),
    path(
        "signin",
        LoginView.as_view(template_name="users/signin.html", form_class=LoginForm),
        name="signin",
    ),
    path(
        "signout",
        LogoutView.as_view(template_name="users/signout.html"),
        name="signout",
    ),
]
