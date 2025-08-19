import os
from motor.motor_asyncio import AsyncIOMotorClient
from gridfs import GridFSBucket
from bson import ObjectId

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
DB_NAME = os.getenv("DB_NAME", "csv_uploader")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
fs_bucket = GridFSBucket(db)
