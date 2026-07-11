# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

# @login_required
# def home(request):
#     return render(request, "dashboard/home.html")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from notes.models import Note
from cloud.models import FileItem
from datetime import timedelta
from django.utils import timezone
from device_sessions.models import DeviceSession


@login_required
def home(request):
    # Placeholder stats until file/notes/devices apps expose real data.
    # Replace each with a real query once that app's models exist.
    stats = {
        "files_count": FileItem.objects.filter(owner=request.user).count(),
        "notes_count": Note.objects.filter(owner=request.user).count(),
        "active_sessions": 1,
        "devices_online": DeviceSession.objects.filter(
            user=request.user,
            is_active=True,
            last_seen_at__gte=timezone.now() - timedelta(minutes=5),
        ).count(),
    }
    return render(request, "dashboard/home.html", {"stats": stats})


