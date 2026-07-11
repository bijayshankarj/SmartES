from django.urls import path
from . import views

app_name = "device_sessions"

urlpatterns = [
    path("", views.device_list, name="list"),
    path("<int:pk>/terminate/", views.terminate_device, name="terminate"),
]