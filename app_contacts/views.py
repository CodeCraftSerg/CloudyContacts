from django.shortcuts import render


def main(request):
    return render(request, "app_contacts/contacts.html", context={})
