from datetime import datetime, timezone
from .mongo import get_collection


def log_activity(user, action, details=None):
    """
    Fire-and-forget activity log entry. Call this from any view
    after a meaningful user action (note created, file uploaded, etc).
    """
    get_collection("activity_logs").insert_one({
        "user_id": user.id,
        "username": user.username,
        "action": action,
        "details": details or {},
        "timestamp": datetime.now(timezone.utc),
    })