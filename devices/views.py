from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Device


@login_required
def device_list(request):

    devices = Device.objects.all()

    return render(
        request,
        "devices/list.html",
        {"devices": devices}
    )