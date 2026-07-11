# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

# @login_required
# def home(request):
#     return render(request, "dashboard/home.html")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    # Placeholder stats until file/notes/devices apps expose real data.
    # Replace each with a real query once that app's models exist.
    stats = {
        "files_count": 0,
        "notes_count": 0,
        "active_sessions": 1,
        "devices_online": 0,
    }
    return render(request, "dashboard/home.html", {"stats": stats})