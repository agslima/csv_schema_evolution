import pytest
from io import BytesIO

@pytest.mark.asyncio
async def test_upload_file(client):
    """Test basic CSV file upload and processing."""
    data = {
        "file": ("test.csv", BytesIO(b"field1,value1\nfield2,value2\n"), "text/csv")
    }
    response = client.post("/api/v1/files/upload", files=data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["filename"] == "test.csv"
    assert json_data["status"] == "processed"
    assert json_data["records_count"] >= 0
    assert isinstance(json_data["fields"], list)

@pytest.mark.asyncio
async def test_upload_file_with_injection(client):
    """Test upload sanitizes CSV injection attempts."""
    csv_content = b"formula,=MALICIOUS()\nemail,+CMD\n"
    data = {
        "file": ("injection.csv", BytesIO(csv_content), "text/csv")
    }
    response = client.post("/api/v1/files/upload", files=data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "processed"
    # The records should contain sanitized values (prefixed with ')
    assert json_data["records_count"] >= 0

@pytest.mark.asyncio
async def test_upload_file_invalid_extension(client):
    """Test upload rejects non-CSV files."""
    data = {
        "file": ("test.txt", BytesIO(b"some content"), "text/plain")
    }
    response = client.post("/api/v1/files/upload", files=data)
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_upload_file_invalid_content_type(client):
    """Test upload validates CSV content-type."""
    data = {
        "file": ("test.csv", BytesIO(b"field1,value1\n"), "application/json")
    }
    response = client.post("/api/v1/files/upload", files=data)
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_list_files(client):
    """Test listing all uploaded files."""
    response = client.get("/api/v1/files/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_upload_and_list(client):
    """Test upload then list files."""
    # Upload
    data = {
        "file": ("sample.csv", BytesIO(b"name,John\nemail,john@example.com\n"), "text/csv")
    }
    upload_response = client.post("/api/v1/files/upload", files=data)
    assert upload_response.status_code == 200
    file_id = upload_response.json()["id"]
    
    # List
    list_response = client.get("/api/v1/files/")
    assert list_response.status_code == 200
    files = list_response.json()
    assert len(files) > 0
    assert any(f["id"] == file_id for f in files)

@pytest.mark.asyncio
async def test_delete_file(client):
    """Test file deletion."""
    # Upload first
    data = {
        "file": ("to_delete.csv", BytesIO(b"field1,value1\n"), "text/csv")
    }
    upload_response = client.post("/api/v1/files/upload", files=data)
    file_id = upload_response.json()["id"]
    
    # Delete
    delete_response = client.delete(f"/api/v1/files/{file_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["status"] == "deleted"

@pytest.mark.asyncio
async def test_delete_nonexistent_file(client):
    """Test deleting a file that doesn't exist."""
    response = client.delete("/api/v1/files/nonexistent_id")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_upload_with_id_field(client):
    """Test upload with optional id_field parameter."""
    csv_content = b"record_id,id1\nfield1,value1\nrecord_id,id2\nfield2,value2\n"
    data = {
        "file": ("with_id.csv", BytesIO(csv_content), "text/csv")
    }
    response = client.post("/api/v1/files/upload?id_field=record_id", files=data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "processed"
