import os
from motor.motor_asyncio import AsyncIOMotorClient
from gridfs import GridFSBucket
from bson import ObjectId

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
DB_NAME = os.getenv("DB_NAME", "csv_uploader")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# Lazy initialization of fs_bucket to avoid issues with mocking
_fs_bucket = None

def get_fs_bucket():
    """Get or initialize GridFS bucket."""
    global _fs_bucket
    if _fs_bucket is None:
        _fs_bucket = GridFSBucket(db)
    return _fs_bucket

# For backward compatibility, provide fs_bucket as a property-like object
class _FSBucketProxy:
    def __getattr__(self, name):
        return getattr(get_fs_bucket(), name)

fs_bucket = _FSBucketProxy()

