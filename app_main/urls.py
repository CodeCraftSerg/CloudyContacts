from django.urls import path, include

from . import views

app_name = "app_main"

urlpatterns = [
    path("", views.main, name="root"),  # app_main:root
]
