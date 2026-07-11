from django.apps import AppConfig


class DeviceSessionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "device_sessions"

    def ready(self):
        import device_sessions.signals  # noqa