from django.urls import path
from . import views

app_name = "cloud"

urlpatterns = [
    path("", views.browse, name="browse"),
    path("folder/<int:folder_id>/", views.browse, name="browse_folder"),
    path("folder/create/", views.create_folder, name="create_folder"),
    path("upload/", views.upload_file, name="upload"),
    path("file/<int:pk>/download/", views.download_file, name="download"),
    path("file/<int:pk>/delete/", views.delete_file, name="delete_file"),
    path("folder/<int:pk>/delete/", views.delete_folder, name="delete_folder"),
]