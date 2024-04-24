from django.shortcuts import render


def main(request):
    return render(request, "app_download/download.html", context={})
