from django.urls import path, include

from . import views

app_name = "app_files"

urlpatterns = [
    path("", views.main, name="files_page"),
]
