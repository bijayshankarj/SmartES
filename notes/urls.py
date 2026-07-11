from django.urls import path
from . import views

app_name = "notes"

urlpatterns = [
    path("", views.note_list, name="list"),
    path("create/", views.note_create, name="create"),
    path("<int:pk>/pin/", views.note_toggle_pin, name="toggle_pin"),
    path("<int:pk>/delete/", views.note_delete, name="delete"),
]