from django.conf import settings
from django.db import models


class ClipboardEntry(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clipboard_entries",
    )
    content = models.TextField()
    is_snippet = models.BooleanField(default=False)  # saved/starred vs plain history
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_snippet", "-created_at"]

    def __str__(self):
        return self.content[:40]