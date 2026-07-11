from .models import DeviceSession
from django.utils import timezone

class UpdateLastSeenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated and request.session.session_key:
            DeviceSession.objects.filter(
                session_key=request.session.session_key, is_active=True
            ).update(last_seen_at=timezone.now())  # auto_now on last_seen_at bumps it even with an empty update
        return response