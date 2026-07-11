from datetime import datetime, timezone

from .mongo import get_collection
from device_sessions.utils import parse_device_info


def log_activity(request, action, details=None):
    """
    Call with the request object (not just user) so every log entry
    carries which device/browser/IP performed the action.
    """
    user = request.user
    info = parse_device_info(request)

    get_collection("activity_logs").insert_one({
        "user_id": user.id,
        "username": user.username,
        "action": action,
        "details": details or {},
        "ip_address": info["ip_address"],
        "device_type": info["device_type"],
        "browser": info["browser"],
        "os": info["os"],
        "session_key": request.session.session_key,
        "timestamp": datetime.now(timezone.utc),
    })