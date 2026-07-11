from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta


class Device(models.Model):

    STATUS_CHOICES = [
        ("online", "Online"),
        ("offline", "Offline"),
        ("sleeping", "Sleeping"),
        ("busy", "Busy"),
    ]

    DEVICE_TYPES = [
        ("phone", "Phone"),
        ("tablet", "Tablet"),
        ("laptop", "Laptop"),
        ("desktop", "Desktop"),
        ("server", "Server"),
        ("raspberry_pi", "Raspberry Pi"),
        ("other", "Other"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # Identity
    device_name = models.CharField(max_length=100)
    friendly_name = models.CharField(max_length=100, blank=True)

    device_type = models.CharField(
        max_length=30,
        choices=DEVICE_TYPES,
        default="other"
    )

    # Platform
    manufacturer = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=100, blank=True)
    operating_system = models.CharField(max_length=100)
    os_version = models.CharField(max_length=50, blank=True)

    # Agent
    app_version = models.CharField(max_length=20, blank=True)

    # Authentication
    api_key = models.CharField(
        max_length=255,
        unique=True
    )

    is_trusted = models.BooleanField(default=False)

    # Network
    tailscale_ip = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    local_ip = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    # Status
    battery_level = models.PositiveSmallIntegerField(default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="offline"
    )

    last_seen = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.friendly_name or self.device_name
    

#Pairing Session
class PairingSession(models.Model):
    code = models.CharField(max_length=8, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    expires_at = models.DateTimeField()

    is_used = models.BooleanField(default=False)

    device = models.OneToOneField(
        Device,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="pairing_session"
    )

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return self.code