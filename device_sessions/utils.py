from user_agents import parse


def get_client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def parse_device_info(request):
    ua_string = request.META.get("HTTP_USER_AGENT", "")
    ua = parse(ua_string)

    if ua.is_mobile:
        device_type = "Mobile"
    elif ua.is_tablet:
        device_type = "Tablet"
    elif ua.is_pc:
        device_type = "PC"
    else:
        device_type = "Other"

    return {
        "ip_address": get_client_ip(request),
        "user_agent_raw": ua_string,
        "device_type": device_type,
        "browser": f"{ua.browser.family} {ua.browser.version_string}".strip(),
        "os": f"{ua.os.family} {ua.os.version_string}".strip(),
    }