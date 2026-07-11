from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import ClipboardEntry
from core.activity import log_activity


@login_required
def clip_list(request):
    clips = ClipboardEntry.objects.filter(owner=request.user)
    return render(request, "clipboard/list.html", {"clips": clips})


@login_required
@require_POST
def clip_create(request):
    content = request.POST.get("content", "").strip()
    if content:
        clip = ClipboardEntry.objects.create(owner=request.user, content=content)
        log_activity(request, "clip_added", {"clip_id": clip.id, "preview": clip.content[:40]})
    return redirect("clipboard:list")


@login_required
@require_POST
def clip_toggle_snippet(request, pk):
    clip = get_object_or_404(ClipboardEntry, pk=pk, owner=request.user)
    clip.is_snippet = not clip.is_snippet
    clip.save(update_fields=["is_snippet"])
    log_activity(request, "clip_snippet_toggled", {"clip_id": clip.id, "is_snippet": clip.is_snippet})
    return redirect("clipboard:list")


@login_required
@require_POST
def clip_delete(request, pk):
    clip = get_object_or_404(ClipboardEntry, pk=pk, owner=request.user)
    log_activity(request, "clip_deleted", {"clip_id": clip.id, "preview": clip.content[:40]})
    clip.delete()
    return redirect("clipboard:list")