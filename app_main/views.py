from django.shortcuts import render


def main(request):
    return render(request, "app_main/index.html", context={})


def about_team(request):
    return render(request, "app_main/about_team.html", context={})


def about_application(request):
    return render(request, "app_main/about_application.html", context={})
