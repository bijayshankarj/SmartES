from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Note
from core.activity import log_activity


@login_required
def note_list(request):
    notes = Note.objects.filter(owner=request.user)
    return render(request, "notes/list.html", {"notes": notes})


@login_required
@require_POST
def note_create(request):
    note = Note.objects.create(
        owner=request.user,
        title=request.POST.get("title", "").strip(),
        body=request.POST.get("body", "").strip(),
    )
    log_activity(request, "note_created", {"note_id": note.id, "title": note.title})
    return redirect("notes:list")


@login_required
@require_POST
def note_toggle_pin(request, pk):
    note = get_object_or_404(Note, pk=pk, owner=request.user)
    note.is_pinned = not note.is_pinned
    note.save(update_fields=["is_pinned"])
    log_activity(request, "note_pin_toggled", {"note_id": note.id, "is_pinned": note.is_pinned})
    return redirect("notes:list")


@login_required
@require_POST
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, owner=request.user)
    log_activity(request, "note_deleted", {"note_id": note.id, "title": note.title})
    note.delete()
    return redirect("notes:list")