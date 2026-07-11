# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import FileResponse, Http404
# from django.views.decorators.http import require_POST

# from .models import Folder, FileItem
# from .storage import storage_backend


# @login_required
# def browse(request, folder_id=None):
#     current_folder = None
#     if folder_id:
#         current_folder = get_object_or_404(Folder, pk=folder_id, owner=request.user)

#     folders = Folder.objects.filter(owner=request.user, parent=current_folder)
#     files = FileItem.objects.filter(owner=request.user, folder=current_folder)

#     return render(request, "cloud/browse.html", {
#         "current_folder": current_folder,
#         "folders": folders,
#         "files": files,
#     })


# @login_required
# @require_POST
# def create_folder(request):
#     name = request.POST.get("name", "").strip()
#     parent_id = request.POST.get("parent_id") or None
#     if name:
#         Folder.objects.create(owner=request.user, name=name, parent_id=parent_id)
#     if parent_id:
#         return redirect("cloud:browse_folder", folder_id=parent_id)
#     return redirect("cloud:browse")


# @login_required
# @require_POST
# def upload_file(request):
#     uploaded = request.FILES.get("file")
#     folder_id = request.POST.get("folder_id") or None

#     if uploaded:
#         FileItem.objects.create(
#             owner=request.user,
#             folder_id=folder_id,
#             file=uploaded,
#             original_name=uploaded.name,
#             size=uploaded.size,
#             content_type=uploaded.content_type or "",
#         )
#     if folder_id:
#         return redirect("cloud:browse_folder", folder_id=folder_id)
#     return redirect("cloud:browse")


# @login_required
# def download_file(request, pk):
#     file_item = get_object_or_404(FileItem, pk=pk, owner=request.user)
#     if not storage_backend.exists(file_item.file.name):
#         raise Http404("File missing from storage")
#     return FileResponse(file_item.file.open("rb"), as_attachment=True, filename=file_item.original_name)


# @login_required
# @require_POST
# def delete_file(request, pk):
#     file_item = get_object_or_404(FileItem, pk=pk, owner=request.user)
#     folder_id = file_item.folder_id
#     storage_backend.delete(file_item.file.name)
#     file_item.delete()
#     if folder_id:
#         return redirect("cloud:browse_folder", folder_id=folder_id)
#     return redirect("cloud:browse")


# @login_required
# @require_POST
# def delete_folder(request, pk):
#     folder = get_object_or_404(Folder, pk=pk, owner=request.user)
#     parent_id = folder.parent_id
#     folder.delete()  # cascades to child folders/files per model FK
#     if parent_id:
#         return redirect("cloud:browse_folder", folder_id=parent_id)
#     return redirect("cloud:browse")


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
from django.views.decorators.http import require_POST

from .models import Folder, FileItem
from .storage import storage_backend
from core.activity import log_activity


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
        folder = Folder.objects.create(owner=request.user, name=name, parent_id=parent_id)
        log_activity(request, "folder_created", {"folder_id": folder.id, "name": folder.name})
    if parent_id:
        return redirect("cloud:browse_folder", folder_id=parent_id)
    return redirect("cloud:browse")


@login_required
@require_POST
def upload_file(request):
    uploaded = request.FILES.get("file")
    folder_id = request.POST.get("folder_id") or None

    if uploaded:
        file_item = FileItem.objects.create(
            owner=request.user,
            folder_id=folder_id,
            file=uploaded,
            original_name=uploaded.name,
            size=uploaded.size,
            content_type=uploaded.content_type or "",
        )
        log_activity(request, "file_uploaded", {
            "file_id": file_item.id, "name": file_item.original_name, "size": file_item.size
        })
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
    log_activity(request, "file_deleted", {"file_id": file_item.id, "name": file_item.original_name})
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
    log_activity(request, "folder_deleted", {"folder_id": folder.id, "name": folder.name})
    folder.delete()
    if parent_id:
        return redirect("cloud:browse_folder", folder_id=parent_id)
    return redirect("cloud:browse")