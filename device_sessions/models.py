from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone

ONLINE_THRESHOLD_MINUTES = 5


class DeviceSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="device_sessions"
    )
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent_raw = models.TextField(blank=True)
    device_type = models.CharField(max_length=20, blank=True)   # Mobile / Tablet / PC / Other
    browser = models.CharField(max_length=100, blank=True)
    os = models.CharField(max_length=100, blank=True)
    login_at = models.DateTimeField(auto_now_add=True)
    last_seen_at = models.DateTimeField(auto_now=True)
    logout_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-last_seen_at"]

    def __str__(self):
        return f"{self.browser} on {self.os} ({self.user.username})"

    @property
    def is_online(self):
        if not self.is_active:
            return False
        return timezone.now() - self.last_seen_at < timedelta(minutes=ONLINE_THRESHOLD_MINUTES)