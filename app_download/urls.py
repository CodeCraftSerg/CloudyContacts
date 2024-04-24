from django.urls import path, include

from . import views

app_name = "app_download"

urlpatterns = [
    path("", views.main, name="download"),
]
