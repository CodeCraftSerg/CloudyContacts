from django.urls import path, include

from . import views

app_name = "app_sort"

urlpatterns = [
    path("", views.main, name="sort"),
]
