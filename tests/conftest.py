import pytest
import sys
import os
from unittest.mock import AsyncMock, MagicMock, patch

# Add backend directory to path so 'app' module can be imported
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Set environment variables early
os.environ["MONGO_URI"] = "mongodb://localhost:27017"
os.environ["DB_NAME"] = "csv_uploader_test"

# Create mock objects
mock_client = MagicMock()
mock_db = MagicMock()
mock_fs_bucket = MagicMock()

# Setup mock methods for db.files
mock_db.files = MagicMock()
mock_db.files.insert_one = AsyncMock(return_value=MagicMock(inserted_id="test_id"))
mock_db.files.find_one = AsyncMock(return_value={
    "_id": "test_id",
    "filename": "test.csv",
    "status": "processed",
    "records_count": 0,
    "fields": []
})
mock_db.files.update_one = AsyncMock()
mock_db.files.delete_one = AsyncMock()
mock_db.files.find = AsyncMock(return_value=[])

# Setup mock methods for fs_bucket
mock_fs_bucket.open_upload_stream = MagicMock()
mock_fs_bucket.open_download_stream_by_name = MagicMock()
mock_fs_bucket.find = MagicMock(return_value=[])
mock_fs_bucket.delete = MagicMock()

# Apply patches globally and keep them active
with patch('app.db.mongo.client', mock_client):
    with patch('app.db.mongo.db', mock_db):
        with patch('app.db.mongo.fs_bucket', mock_fs_bucket):
            # Import app AFTER patches are active
            from fastapi.testclient import TestClient as _TestClient
            from app.main import app as _app
            
            # Store references at module level
            TestClient = _TestClient
            app = _app

@pytest.fixture
def client():
    """Create test client with mocked MongoDB."""
    return TestClient(app)

