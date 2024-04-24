from django.urls import path, include

from . import views

app_name = "app_notes"

urlpatterns = [
    path("", views.main, name="notes"),
]
