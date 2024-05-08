from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import TagForm, NoteForm
from .models import Tag, Note


@login_required
def main(request):
    notes = (
        Note.objects.filter(user=request.user).all()
        if request.user.is_authenticated
        else []
    )
    tags = (
        Tag.objects.filter(user=request.user).all()
        if request.user.is_authenticated
        else []
    )
    return render(request, "app_notes/notes.html", {"notes": notes, "tags": tags})


@login_required
def tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to="app_notes:tag")
        else:
            return render(request, "app_notes/tag.html", {"form": form})

    return render(request, "app_notes/tag.html", {"form": TagForm()})


@login_required
def note(request):
    tags = Tag.objects.filter(user=request.user).all()

    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()
            choice_tags = Tag.objects.filter(
                name__in=request.POST.getlist("tags"), user=request.user
            )
            for tag_ in choice_tags.iterator():
                new_note.tag.add(tag_)

            return redirect(to="app_notes:notes")
        else:
            return render(request, "app_notes/note.html", {"tags": tags, "form": form})

    return render(request, "app_notes/note.html", {"tags": tags, "form": NoteForm()})


@login_required
def detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    return render(request, "app_notes/detail.html", {"note": note})


@login_required
def set_done(request, note_id):
    Note.objects.filter(pk=note_id, user=request.user).update(is_done=True)
    return redirect(to="app_notes:notes")


@login_required
def delete_note(request, note_id):
    Note.objects.get(pk=note_id, user=request.user).delete()
    return redirect(to="app_notes:notes")


@login_required
def search(request):
    if "query" in request.GET:
        query = request.GET["query"]
        notes = Note.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query), user=request.user
        )
        # search_notes = pagination(request, notes)
        return render(request, "app_notes/search_results.html", {"notes": notes})
    else:
        return redirect(to="app_notes:notes")


@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    tags = Tag.objects.filter(user=request.user).all()

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            edited_note = form.save(commit=False)
            edited_note.user = request.user
            edited_note.save()
            edited_note.tag.clear()
            choice_tags = Tag.objects.filter(
                name__in=request.POST.getlist("tags"), user=request.user
            )
            for tag_ in choice_tags.iterator():
                edited_note.tag.add(tag_)

            return redirect(to="app_notes:notes")
        else:
            return render(
                request,
                "app_notes/edit_note.html",
                {
                    "note": note,
                    "tags": tags,
                    "form": form,
                },
            )

    form = NoteForm(instance=note)
    return render(
        request,
        "app_notes/edit_note.html",
        {
            "note": note,
            "tags": tags,
            "form": form,
        },
    )


@login_required
def sort(request):
    if request.method == "GET":
        selected_tags = request.GET.getlist("selected_tags")
        notes = Note.objects.filter(
            tag__name__in=selected_tags, user=request.user
        ).distinct()
        return render(
            request,
            "app_notes/search_results.html",
            {"notes": notes, "selected_tags": selected_tags},
        )
    else:
        return redirect(to="app_notes:notes")
