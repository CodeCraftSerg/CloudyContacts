from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests


def main(request):
    return render(request, "app_news/news_page.html")

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
        return render(request, 'app_news/error.html', {'message': 'Could not get response from server.'})

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the main news container
    news_containers = soup.find_all('div', class_=['c-article-card-bgimage', 'c-article-card', 'c-article-card--big-headline'])

    # Get sport news items from each container
    for container in news_containers:
        result = {}
        time_tag = container.find('time')
        title_tag = container.find('h3', class_='c-article-card__headline-inner')
        url_tag = container.find('a', class_='c-article-card__headline')

        if time_tag and title_tag and url_tag:
            result['time'] = time_tag.get('datetime', '')
            result['sport'] = 'Sport'  # Since this website is specifically for sport news
            result['url'] = url_tag.get('href', '')
            result['news'] = title_tag.text.strip()

            sport_news.append(result)

    # Check if any sport news found
    if not sport_news:
        # Return an error message if no sport news found
        return render(request, 'app_news/error.html', {'message': 'No sport news found.'})

    # Render the sport_news template with sport news data
    return render(request, 'app_news/sport_news.html', {'sport_news': sport_news})


def politic_news(request):
    # Initialize an empty list to store news
    news = []

    # URL of the website to scrape news from
    base_url = "https://suspilne.media/"

    # Get response from the server
    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        # Return an error message if there's a problem with getting the response
        return render(request, 'app_news/error.html', {'message': 'Could not get response from server.'})

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the main news container
    news_containers = soup.find_all('div', class_=['c-article-card-bgimage', 'c-article-card', 'c-article-card--big-headline'])

    # Get news items from each container
    for container in news_containers:
        result = {}
        try:
            result['time'] = container.find('time')['datetime']
            result['title'] = container.find('h3', class_='c-article-card__headline-inner').text.strip()
            result['url'] = container.find('a', class_='c-article-card__headline')['href']
        except AttributeError as e:
            # Skip if any attribute error occurs
            continue

        news.append(result)

    # Check if any news found
    if not news:
        # Return an error message if no news found
        return render(request, 'app_news/error.html', {'message': 'No news found.'})

    # Render the politic_news template with news data
    return render(request, 'app_news/politic_news.html', {'news': news})

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
        return render(request, 'app_news/error.html', {'message': 'Could not get response from server.'})

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the main news container
    news_containers = soup.find_all('div', class_=['c-article-card__content'])

    # Get culture news items from each container
    for container in news_containers:
        result = {}
        time_tag = container.find('time')
        title_tag = container.find('h3', class_='c-article-card__headline-inner')
        url_tag = container.find('a', class_='c-article-card__headline')

        if time_tag and title_tag and url_tag:
            result['time'] = time_tag.get('datetime', '')
            result['culture'] = 'Culture'  # Since this website is specifically for culture news
            result['url'] = url_tag.get('href', '')
            result['news'] = title_tag.text.strip()

            culture_news.append(result)

    # Check if any culture news found
    if not culture_news:
        # Return an error message if no culture news found
        return render(request, 'app_news/error.html', {'message': 'No culture news found.'})

    # Render the culture_news template with culture news data
    return render(request, 'app_news/culture_news.html', {'culture_news': culture_news})