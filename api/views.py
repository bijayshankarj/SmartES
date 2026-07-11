import secrets

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from devices.models import Device

import json


@csrf_exempt
def register_device(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "POST required"},
            status=405
        )

    data = json.loads(request.body)

    api_key = secrets.token_hex(32)

    device = Device.objects.create(
        device_name=data["device_name"],
        device_type=data["device_type"],
        operating_system=data["operating_system"],
        api_key=api_key
    )

    return JsonResponse({
        "device_id": str(device.id),
        "api_key": api_key
    })