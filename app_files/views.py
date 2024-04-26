from django.shortcuts import render


def main(request):
    return render(request, "app_files/files_page.html", context={})
