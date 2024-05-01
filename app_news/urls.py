from django.urls import path, include

from . import views

app_name = "app_news"

urlpatterns = [
    path("", views.main, name="news_page"),
]
