import os

from django.shortcuts import render, redirect
from CloudyContacts import settings
from .forms import UploadFileForm
from .models import UserFile
from django.contrib.auth.decorators import login_required


def search_files_by_type(request, file_type: str):
    """
    Searches and returns files filtered by the specified type for the logged-in user.
    If no files are found, returns an empty list.

    Args:
    request: The HTTP request object.
    file_type (str): The type of files to search for.

    Returns:
    list: A list of UserFile instances that match the type.
    """
    try:
        files = UserFile.objects.filter(user=request.user)
        result = files.filter(file_type=file_type)
    except UserFile.DoesNotExist:
        result = []
    return result


@login_required
def main(request):
    """
    Renders the main file page which allows users to navigate to different file categories.

    Args:
    request: The HTTP request object.

    Returns:
    HttpResponse: The rendered main file page.
    """
    return render(request, "app_files/files_page.html", context={'title': 'Download files'})


@login_required
def upload_file(request):
    """
    Handles the uploading of files. If the request method is POST and the form is valid,
    saves the new file associated with the current user and redirects to a specified URL.

    Args:
    request: The HTTP request object.

    Returns:
    HttpResponse: The upload file page, potentially with a form populated with previous input.
    """
    form = UploadFileForm(instance=UserFile())
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES, instance=UserFile())
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            return redirect('app_files:files_page')
    return render(request, 'app_files/upload_files.html', context=
    {
        'title': 'Download files',
        'form': form,
        'media_url': settings.MEDIA_URL
    })


@login_required
def images(request):
    """
    Displays a page with all image files uploaded by the logged-in user.

    Args:
    request: The HTTP request object.

    Returns:
    HttpResponse: The image files page with the list of image files.
    """
    type = 'image'
    image_list = search_files_by_type(request, type)
    print(image_list)
    return render(request, 'app_files/image_files.html', context=
    {
        'title': 'Download files',
        'image_list': image_list,
        'media_url': settings.MEDIA_URL
    })


@login_required
def videos(request):
    """
    Displays a page with all video files uploaded by the logged-in user.

    Args:
    request: The HTTP request object.

    Returns:
    HttpResponse: The video files page with the list of video files.
    """
    type = 'video'
    video_list = search_files_by_type(request, type)
    return render(request, 'app_files/video_files.html', context=
    {
        'title': 'Download files',
        'video_list': video_list,
        'media_url': settings.MEDIA_URL
    })


@login_required
def audios(request):
    """
    Displays a page with all audio files uploaded by the logged-in user.

    Args:
    request: The HTTP request object.

    Returns:
    HttpResponse: The audio files page with the list of audio files.
    """
    type = 'audio'
    audio_list = search_files_by_type(request, type)
    return render(request, 'app_files/audio_files.html', context=
    {
        'title': 'Download files',
        'audio_list': audio_list,
        'media_url': settings.MEDIA_URL
    })


@login_required
def docs(request):
    """
    Displays a page with all document files uploaded by the logged-in user.

    Args:
    request: The HTTP request object.

    Returns:
    HttpResponse: The document files page with the list of document files.
    """
    type = 'document'
    document_list = search_files_by_type(request, type)
    return render(request, 'app_files/docs_files.html', context=
    {
        'title': 'Download files',
        'document_list': document_list,
        'media_url': settings.MEDIA_URL
    })


@login_required
def archives(request):
    """
    Displays a page with all archive files uploaded by the logged-in user.

    Args:
    request: The HTTP request object.

    Returns:
    HttpResponse: The archives page with the list of archive files.
    """
    type = 'archive'
    archive_list = search_files_by_type(request, type)
    return render(request, 'app_files/archives.html', context=
    {
        'title': 'Download files',
        'archive_list': archive_list,
        'media_url': settings.MEDIA_URL
    })


@login_required
def other(request):
    """
    Displays a page with all files categorized as 'other' uploaded by the logged-in user.

    Args:
    request: The HTTP request object.

    Returns:
    HttpResponse: The other files page with the list of other files.
    """
    type = 'other'
    other_list = search_files_by_type(request, type)
    return render(request, 'app_files/other_files.html', context=
    {
        'title': 'Download files',
        'other_list': other_list,
        'media_url': settings.MEDIA_URL
    })


@login_required
def delete_file(request, f_id):
    file = UserFile.objects.filter(pk=f_id, user=request.user)
    try:
        os.unlink(os.path.join(settings.MEDIA_ROOT, str(file.first().filepath)))
    except OSError as e:
        print(e)
    file.delete()
    return redirect(to="app_files:files_page")


@login_required
def edit_description(request, f_id):
    if request.method == "POST":
        file_description = request.POST["file_description"]
        UserFile.objects.filter(pk=f_id, user=request.user).update(file_description=file_description)
        return redirect(to="app_files:files_page")

    file = UserFile.objects.filter(pk=f_id, user=request.user).first()
    ctx = {"title": "CloudyContacts", "file": file, "media": settings.MEDIA_URL}
    return render(request, "app_files/edit_files.html", context=ctx)