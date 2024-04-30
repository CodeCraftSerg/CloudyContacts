from django.urls import path, include

from . import views

app_name = "app_notes"

urlpatterns = [
    path("", views.main, name="notes"),
    path("tag/", views.tag, name="tag"),
    path("note/", views.note, name="note"),
    path("detail/<int:note_id>", views.detail, name="detail"),
    path("done/<int:note_id>", views.set_done, name="set_done"),
    path("delete/<int:note_id>", views.delete_note, name="delete"),
    path('edit/<int:note_id>', views.edit_note, name='edit_note'),
    path('search/', views.search, name='search'),
    path('sort/', views.sort, name='sort'),
]
