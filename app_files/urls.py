from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "app_files"

urlpatterns = [
    path("", views.main, name="files_page"),
    path("upload/", views.upload_file, name="upload_files"),
    path("image/", views.images, name="image_files"),
    path("video/", views.videos, name="video_files"),
    path("audio/", views.audios, name="audio_files"),
    path("document/", views.docs, name="docs_files"),
    path("archive/", views.archives, name="archives"),
    path("other/", views.other, name="other_files"),

    path("delete-file/<int:f_id>", views.delete_file, name='delete_file'),
    path("edit-description/<int:f_id>", views.edit_description, name='edit_description'),
]
