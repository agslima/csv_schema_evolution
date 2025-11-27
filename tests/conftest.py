import pytest
import sys
import os
from unittest.mock import AsyncMock, MagicMock, patch

# Add backend directory to path so 'app' module can be imported
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Set environment variables early
os.environ["MONGO_URI"] = "mongodb://localhost:27017"
os.environ["DB_NAME"] = "csv_uploader_test"

# Mock Motor client BEFORE importing any app modules
mock_client = MagicMock()
mock_db = MagicMock()
mock_fs_bucket = MagicMock()

# Setup mock methods
mock_db.files = MagicMock()
mock_db.files.insert_one = AsyncMock(return_value=MagicMock(inserted_id="test_id"))
mock_db.files.find_one = AsyncMock(return_value={"_id": "test_id", "filename": "test.csv", "status": "processed"})
mock_db.files.update_one = AsyncMock()
mock_db.files.delete_one = AsyncMock()
mock_db.files.find = AsyncMock(return_value=[])

# Patch before importing app
sys.modules['motor'] = MagicMock()
sys.modules['motor.motor_asyncio'] = MagicMock()

with patch.dict('sys.modules', {
    'motor': MagicMock(),
    'motor.motor_asyncio': MagicMock(AsyncIOMotorClient=MagicMock(return_value=mock_client))
}):
    with patch('app.db.mongo.AsyncIOMotorClient', return_value=mock_client):
        with patch('app.db.mongo.client', mock_client):
            with patch('app.db.mongo.db', mock_db):
                with patch('app.db.mongo.fs_bucket', mock_fs_bucket):
                    from fastapi.testclient import TestClient
                    from app.main import app

@pytest.fixture
def client():
    """Create test client."""
    with TestClient(app) as c:
        yield c
