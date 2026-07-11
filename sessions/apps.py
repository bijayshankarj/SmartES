from django.apps import AppConfig


class SessionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "device_sessions"

    def ready(self):
        import sessions.signals  # noqa