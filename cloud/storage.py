from django.core.files.storage import default_storage


class StorageBackend:
    """
    Thin wrapper around Django's storage API. Views should call this,
    never Django's storage classes directly, so swapping to S3/MinIO/etc.
    later only requires changing this file.
    """

    def save(self, path, file_obj):
        return default_storage.save(path, file_obj)

    def delete(self, path):
        if default_storage.exists(path):
            default_storage.delete(path)

    def url(self, path):
        return default_storage.url(path)

    def exists(self, path):
        return default_storage.exists(path)


storage_backend = StorageBackend()