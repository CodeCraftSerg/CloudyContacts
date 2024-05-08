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
    """
    The sport_news function scrapes the Suspilne.Media website for sport news,
        and returns a list of dictionaries containing the following information:
        - time (datetime)
        - url (str)
        - news (str)
    
    :param request: Get the request object
    :return: The sport_news
    :doc-author: Trelent
    """
    sport_news = []
    base_url = "https://suspilne.media/sport/"

    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return render(
            request,
            "app_news/error.html",
            {"message": "Could not get response from server."},
        )

    soup = BeautifulSoup(response.text, "html.parser")

    news_containers = soup.find_all(
        "div",
        class_=[
            "c-article-card-bgimage",
            "c-article-card",
            "c-article-card--big-headline",
        ],
    )

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
            result["sport"] = ("Sport")
            result["url"] = url_tag.get("href", "")
            result["news"] = title_tag.text.strip()

            sport_news.append(result)

    if not sport_news:
        return render(
            request, "app_news/error.html", {"message": "No sport news found."}
        )

    paginator = Paginator(sport_news, 5)
    page_number = request.GET.get("page")
    try:
        sport_news_page = paginator.page(page_number)
    except PageNotAnInteger:
        sport_news_page = paginator.page(1)
    except EmptyPage:
        sport_news_page = paginator.page(paginator.num_pages)

    return render(request, "app_news/sport_news.html", {"sport_news": sport_news_page})


@login_required
def politic_news(request):
    """
    The politic_news function scrapes the Suspilne.Media website for political news and 
    returns a list of dictionaries containing the title, url, and time of each article.
    
    :param request: Get the request object that is sent from the user to your server
    :return: A render function
    :doc-author: Trelent
    """
    politic_news = []
    base_url = "https://suspilne.media/"
    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return render(
            request,
            "app_news/error.html",
            {"message": "Could not get response from server."},
        )
    soup = BeautifulSoup(response.text, "html.parser")
    news_containers = soup.find_all(
        "div",
        class_=[
            "c-article-card-bgimage",
            "c-article-card",
            "c-article-card--big-headline",
        ],
    )
    
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
            continue
        politic_news.append(result)
    if not politic_news:
        return render(
            request, "app_news/error.html", {"message": "No political news available."}
        )
    paginator = Paginator(politic_news, 5)
    page_number = request.GET.get("page")
    try:
        politic_news_page = paginator.page(page_number)
    except PageNotAnInteger:
        politic_news_page = paginator.page(1)
    except EmptyPage:
        politic_news_page = paginator.page(paginator.num_pages)
        
    return render(request, "app_news/politic_news.html", {"news": politic_news_page})


@login_required
def culture_news(request):
    """
    The culture_news function scrapes the Suspilne.Media website for culture news,
        and then renders a template with the results.
    
    :param request: Get the request object
    :return: A render function, not a dictionary
    :doc-author: Trelent
    """
    culture_news = []
    base_url = "https://suspilne.media/culture/"

    try:
        response = requests.get(base_url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return render(
            request,
            "app_news/error.html",
            {"message": "Could not get response from server."},
        )

    soup = BeautifulSoup(response.text, "html.parser")

    news_containers = soup.find_all("div", class_=["c-article-card__content"])

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
            result["culture"] = ("Culture")
            result["url"] = url_tag.get("href", "")
            result["news"] = title_tag.text.strip()

            culture_news.append(result)

    if not culture_news:
        return render(
            request, "app_news/error.html", {"message": "No culture news found."}
        )

    paginator = Paginator(culture_news, 5)
    page_number = request.GET.get("page")
    try:
        culture_news_page = paginator.page(page_number)
    except PageNotAnInteger:
        culture_news_page = paginator.page(1)
    except EmptyPage:
        culture_news_page = paginator.page(paginator.num_pages)

    return render(request, "app_news/culture_news.html", {"culture_news": culture_news_page})
