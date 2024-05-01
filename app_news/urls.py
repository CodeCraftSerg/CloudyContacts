from django.urls import path, include

from . import views

app_name = "app_news"

urlpatterns = [
    path("", views.main, name="news_page"),
    path('sport-news/', views.sport_news, name='sport_news'),
    path('politic-news/', views.politic_news, name='politic_news'),
    path('culture-news/', views.culture_news, name='culture_news'),
]
