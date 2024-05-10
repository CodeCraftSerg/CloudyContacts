from django.db import models
from django.contrib.auth.models import User


# Basic models for users widgets
class Widget(models.Model):
    sport = models.URLField()
    news = models.URLField()
    weather = models.URLField()
    is_sport = models.BooleanField(default=False)
    is_news = models.BooleanField(default=False)
    is_weather = models.BooleanField(default=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        if self.is_sport:
            return "Sport"
        elif self.is_news:
            return "News"
        else:
            return "Weather"
