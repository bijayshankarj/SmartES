from pymongo import MongoClient
from django.conf import settings

_client = None


def get_mongo_client():
    global _client
    if _client is None:
        _client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT, tz_aware=True)
    return _client


def get_mongo_db():
    return get_mongo_client()[settings.MONGO_DB_NAME]


def get_collection(name):
    """
    Central place every app should go through to reach a Mongo collection.
    e.g. get_collection('activity_logs'), get_collection('audit_logs')
    """
    return get_mongo_db()[name]