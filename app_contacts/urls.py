from django.urls import path, include

from . import views

app_name = "app_contacts"

urlpatterns = [
    path("", views.main, name="contacts"),
]
