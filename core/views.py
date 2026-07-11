from core.activity import log_activity

@login_required
@require_POST
def note_create(request):
    note = Note.objects.create(
        owner=request.user,
        title=request.POST.get("title", "").strip(),
        body=request.POST.get("body", "").strip(),
    )
    log_activity(request.user, "note_created", {"note_id": note.id, "title": note.title})
    return redirect("notes:list")