from django.urls import path

from . import views

app_name = "app_contacts"

urlpatterns = [
    path("", views.main, name="contacts"),
    path("<int:page>", views.main, name="index_paginate"),
    path("add_contact/", views.add_contact, name="add_contact"),
    path("contact_details/<int:contact_id>/", views.contact_details, name="contact_details"),
    path("delete_contact/<int:contact_id>/", views.delete_contact, name="delete_contact"),
    path("contact_update/<int:contact_id>/", views.contact_update, name="contact_update"),
    path("contact_birthday/", views.contact_birthday, name="contact_birthday"),
    path("calendar/", views.calendar, name="calendar"),

]
