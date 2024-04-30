import requests
import environ

from datetime import date
from django.shortcuts import render

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)


def main(request):
    API_WEATHER_KEY = env("API_WEATHER_KEY")
    url_1 = (
        "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid="
        + API_WEATHER_KEY
    )

    city = "Kyiv"

    city_weather = requests.get(url_1.format(city)).json()

    weather = {
        "city": city,
        "temperature": city_weather["main"]["temp"],
        "description": city_weather["weather"][0]["description"],
        "icon": city_weather["weather"][0]["icon"],
        "temperature_max": city_weather["main"]["temp_max"],
        "temperature_min": city_weather["main"]["temp_min"],
        "feelslike_weather": city_weather["main"]["feels_like"],
    }

    url_2 = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date.today().strftime('%d.%m.%Y')}"

    currency_exchange = requests.get(url_2).json()

    exchange_rates = {}
    for item in currency_exchange["exchangeRate"]:
        currency = item["currency"]
        if currency in ["USD", "EUR"]:
            if date.today().strftime("%d.%m.%Y") not in exchange_rates:
                exchange_rates[date.today().strftime("%d.%m.%Y")] = {}
            exchange_rates[date.today().strftime("%d.%m.%Y")][currency] = {
                "sale": float(item["saleRate"]),
                "purchase": float(item["purchaseRate"]),
            }

    return render(
        request,
        "app_main/index.html",
        {"weather": weather, "exchange_rates": exchange_rates},
    )


def about_team(request):
    return render(request, "app_main/about_team.html", context={})


def about_application(request):
    return render(request, "app_main/about_application.html", context={})
