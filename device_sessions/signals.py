from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone

from .models import DeviceSession
from .utils import parse_device_info


@receiver(user_logged_in)
def create_device_session(sender, request, user, **kwargs):
    info = parse_device_info(request)
    DeviceSession.objects.update_or_create(
        session_key=request.session.session_key,
        defaults={
            "user": user,
            "is_active": True,
            "logout_at": None,
            **info,
        },
    )


@receiver(user_logged_out)
def close_device_session(sender, request, user, **kwargs):
    if request.session.session_key:
        DeviceSession.objects.filter(session_key=request.session.session_key).update(
            is_active=False, logout_at=timezone.now()
        )