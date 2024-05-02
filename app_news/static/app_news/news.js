function showNews(category) {
    if (category === 'Sport') {
        window.location.href = "/app_news/sport-news/";
    } else if (category === 'Politics') {
        window.location.href = "/app_news/politic-news/";
    } else if (category === 'Culture') {
        window.location.href = "/app_news/culture-news/";
    } else {
        console.log("Showing " + category + " news.");
    }
}
