from django.contrib import admin
from .models import Device, PairingSession

admin.site.register(Device)
admin.site.register(PairingSession)