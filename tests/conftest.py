import pytest
import sys
import os
from unittest.mock import AsyncMock, MagicMock, patch, PropertyMock

# Add backend directory to path so 'app' module can be imported
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Set environment variables early
os.environ["MONGO_URI"] = "mongodb://localhost:27017"
os.environ["DB_NAME"] = "csv_uploader_test"


@pytest.fixture(scope="session", autouse=True)
def mock_mongo_db():
    """Mock MongoDB connections for all tests."""
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
    
    # Patch at module level before importing app
    with patch('app.db.mongo.client', mock_client):
        with patch('app.db.mongo.db', mock_db):
            with patch('app.db.mongo.fs_bucket', mock_fs_bucket):
                with patch('app.db.mongo.get_fs_bucket', return_value=mock_fs_bucket):
                    yield


from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client(mock_mongo_db):
    """Create test client with mocked MongoDB."""
    with TestClient(app) as c:
        yield c

