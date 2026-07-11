from django.urls import path
from . import views

app_name = "clipboard"

urlpatterns = [
    path("", views.clip_list, name="list"),
    path("create/", views.clip_create, name="create"),
    path("<int:pk>/toggle-snippet/", views.clip_toggle_snippet, name="toggle_snippet"),
    path("<int:pk>/delete/", views.clip_delete, name="delete"),
]