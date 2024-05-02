from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bs4 import BeautifulSoup
import requests


@login_required
def main(request):
    return render(request, "app_news/news_page.html")


@login_required
def sport_news(request):
    # Initialize an empty list to store sport news
    sport_news = []

    # URL of the website to scrape news from
    base_url = "https://suspilne.media/sport/"

    # Get response from the server
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        # Return an error message if there's a problem with getting the response
        return render(
            request,
            "app_news/error.html",
            {"message": "Could not get response from server."},
        )

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the main news container
    news_containers = soup.find_all(
        "div",
        class_=[
            "c-article-card-bgimage",
            "c-article-card",
            "c-article-card--big-headline",
        ],
    )

    # Get sport news items from each container
    for container in news_containers:
        result = {}
        time_tag = container.find("time")
        title_tag = container.find("h3", class_="c-article-card__headline-inner")
        url_tag = container.find("a", class_="c-article-card__headline")

        if time_tag and title_tag and url_tag:
            original_datetime_str = time_tag.get("datetime", "")
            hours_offset = int(original_datetime_str[-6:-3])
            original_datetime = datetime.fromisoformat(
                original_datetime_str.replace("T", " ").split("+")[0]
            )
            original_datetime = original_datetime + timedelta(hours=hours_offset)
            new_datetime_str = original_datetime.strftime("%Y-%m-%d %H:%M")

            result["time"] = new_datetime_str

            # print(result["time"])
            # print(type(result["time"]))
            result["sport"] = (
                "Sport"  # Since this website is specifically for sport news
            )
            result["url"] = url_tag.get("href", "")
            result["news"] = title_tag.text.strip()

            sport_news.append(result)

    # Check if any sport news found
    if not sport_news:
        # Return an error message if no sport news found
        return render(
            request, "app_news/error.html", {"message": "No sport news found."}
        )

    # Paginate the news
    paginator = Paginator(sport_news, 5)  # Show 5 news per page
    page_number = request.GET.get("page")
    try:
        sport_news_page = paginator.page(page_number)
    except PageNotAnInteger:
        sport_news_page = paginator.page(1)
    except EmptyPage:
        sport_news_page = paginator.page(paginator.num_pages)

    # Render the sport_news template with paginated sport news data
    return render(request, "app_news/sport_news.html", {"sport_news": sport_news_page})


@login_required
def politic_news(request):
    # Initialize an empty list to store politic news
    politic_news = []
    # URL of the website to scrape news from
    base_url = "https://suspilne.media/"
    # Get response from the server
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        # Return an error message if there's a problem with getting the response
        return render(
            request,
            "app_news/error.html",
            {"message": "Could not get response from server."},
        )
    soup = BeautifulSoup(response.text, "html.parser")
    # Find the main news container
    news_containers = soup.find_all(
        "div",
        class_=[
            "c-article-card-bgimage",
            "c-article-card",
            "c-article-card--big-headline",
        ],
    )
    # Get news items from each container
    for container in news_containers:
        result = {}
        try:
            original_datetime_str = container.find("time")["datetime"]
            hours_offset = int(original_datetime_str[-6:-3])
            original_datetime = datetime.fromisoformat(
                original_datetime_str.replace("T", " ").split("+")[0]
            )
            original_datetime = original_datetime + timedelta(hours=hours_offset)
            new_datetime_str = original_datetime.strftime("%Y-%m-%d %H:%M")
            result["time"] = new_datetime_str
            result["title"] = container.find(
                "h3", class_="c-article-card__headline-inner"
            ).text.strip()
            result["url"] = container.find("a", class_="c-article-card__headline")[
                "href"
            ]
        except AttributeError as e:
            # Skip if any attribute error occurs
            continue
        politic_news.append(result)
    # Check if any news found
    if not politic_news:
        # Return an error message if no news found
        return render(
            request, "app_news/error.html", {"message": "No political news available."}
        )
    # Paginate the news
    paginator = Paginator(politic_news, 5)  # Show 5 news per page
    page_number = request.GET.get("page")
    try:
        politic_news_page = paginator.page(page_number)
    except PageNotAnInteger:
        politic_news_page = paginator.page(1)
    except EmptyPage:
        politic_news_page = paginator.page(paginator.num_pages)
    # Render the politic_news template with paginated news data
    return render(request, "app_news/politic_news.html", {"news": politic_news_page})


@login_required
def culture_news(request):
    # Initialize an empty list to store culture news
    culture_news = []

    # URL of the website to scrape news from
    base_url = "https://suspilne.media/culture/"

    # Get response from the server
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        # Return an error message if there's a problem with getting the response
        return render(
            request,
            "app_news/error.html",
            {"message": "Could not get response from server."},
        )

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the main news container
    news_containers = soup.find_all("div", class_=["c-article-card__content"])

    # Get culture news items from each container
    for container in news_containers:
        result = {}
        time_tag = container.find("time")
        title_tag = container.find("h3", class_="c-article-card__headline-inner")
        url_tag = container.find("a", class_="c-article-card__headline")

        if time_tag and title_tag and url_tag:
            original_datetime_str = time_tag.get("datetime", "")
            hours_offset = int(original_datetime_str[-6:-3])
            original_datetime = datetime.fromisoformat(
                original_datetime_str.replace("T", " ").split("+")[0]
            )
            original_datetime = original_datetime + timedelta(hours=hours_offset)
            new_datetime_str = original_datetime.strftime("%Y-%m-%d %H:%M")

            result["time"] = new_datetime_str
            result["culture"] = (
                "Culture"  # Since this website is specifically for culture news
            )
            result["url"] = url_tag.get("href", "")
            result["news"] = title_tag.text.strip()

            culture_news.append(result)

    # Check if any culture news found
    if not culture_news:
        # Return an error message if no culture news found
        return render(
            request, "app_news/error.html", {"message": "No culture news found."}
        )

    # Paginate the news
    paginator = Paginator(culture_news, 5)  # Show 5 news per page
    page_number = request.GET.get("page")
    try:
        culture_news_page = paginator.page(page_number)
    except PageNotAnInteger:
        culture_news_page = paginator.page(1)
    except EmptyPage:
        culture_news_page = paginator.page(paginator.num_pages)

    # Render the culture_news template with paginated culture news data
    return render(
        request, "app_news/culture_news.html", {"culture_news": culture_news_page}
    )
