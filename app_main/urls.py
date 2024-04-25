from django.urls import path, include

from . import views

app_name = "app_main"

urlpatterns = [
    path("", views.main, name="root"),  # app_main:root
    path("app_main/about_team/", views.about_team, name="about_team"),
    path(
        "app_main/about_application/", views.about_application, name="about_application"
    ),
]
