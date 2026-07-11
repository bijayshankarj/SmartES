from django.contrib.auth.decorators import login_required
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import DeviceSession
from core.activity import log_activity


@login_required
def device_list(request):
    devices = DeviceSession.objects.filter(user=request.user)
    return render(request, "device_sessions/list.html", {"devices": devices})


@login_required
@require_POST
def terminate_device(request, pk):
    device = get_object_or_404(DeviceSession, pk=pk, user=request.user)

    # Actually invalidate that browser's session, not just our record of it
    SessionStore(session_key=device.session_key).delete()

    device.is_active = False
    device.logout_at = timezone.now()
    device.save(update_fields=["is_active", "logout_at"])

    log_activity(request, "device_terminated", {
        "terminated_browser": device.browser, "terminated_os": device.os
    })
    return redirect("device_sessions:list")