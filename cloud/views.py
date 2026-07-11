from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
from django.views.decorators.http import require_POST

from .models import Folder, FileItem
from .storage import storage_backend


@login_required
def browse(request, folder_id=None):
    current_folder = None
    if folder_id:
        current_folder = get_object_or_404(Folder, pk=folder_id, owner=request.user)

    folders = Folder.objects.filter(owner=request.user, parent=current_folder)
    files = FileItem.objects.filter(owner=request.user, folder=current_folder)

    return render(request, "cloud/browse.html", {
        "current_folder": current_folder,
        "folders": folders,
        "files": files,
    })


@login_required
@require_POST
def create_folder(request):
    name = request.POST.get("name", "").strip()
    parent_id = request.POST.get("parent_id") or None
    if name:
        Folder.objects.create(owner=request.user, name=name, parent_id=parent_id)
    if parent_id:
        return redirect("cloud:browse_folder", folder_id=parent_id)
    return redirect("cloud:browse")


@login_required
@require_POST
def upload_file(request):
    uploaded = request.FILES.get("file")
    folder_id = request.POST.get("folder_id") or None

    if uploaded:
        FileItem.objects.create(
            owner=request.user,
            folder_id=folder_id,
            file=uploaded,
            original_name=uploaded.name,
            size=uploaded.size,
            content_type=uploaded.content_type or "",
        )
    if folder_id:
        return redirect("cloud:browse_folder", folder_id=folder_id)
    return redirect("cloud:browse")


@login_required
def download_file(request, pk):
    file_item = get_object_or_404(FileItem, pk=pk, owner=request.user)
    if not storage_backend.exists(file_item.file.name):
        raise Http404("File missing from storage")
    return FileResponse(file_item.file.open("rb"), as_attachment=True, filename=file_item.original_name)


@login_required
@require_POST
def delete_file(request, pk):
    file_item = get_object_or_404(FileItem, pk=pk, owner=request.user)
    folder_id = file_item.folder_id
    storage_backend.delete(file_item.file.name)
    file_item.delete()
    if folder_id:
        return redirect("cloud:browse_folder", folder_id=folder_id)
    return redirect("cloud:browse")


@login_required
@require_POST
def delete_folder(request, pk):
    folder = get_object_or_404(Folder, pk=pk, owner=request.user)
    parent_id = folder.parent_id
    folder.delete()  # cascades to child folders/files per model FK
    if parent_id:
        return redirect("cloud:browse_folder", folder_id=parent_id)
    return redirect("cloud:browse")