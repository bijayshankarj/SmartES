from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.mongo import get_collection


@login_required
def feed(request):
    logs = list(
        get_collection("activity_logs")
        .find({"user_id": request.user.id})
        .sort("timestamp", -1)
        .limit(50)
    )
    return render(request, "activity/feed.html", {"logs": logs})