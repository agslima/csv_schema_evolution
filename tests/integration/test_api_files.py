import pytest
from io import BytesIO

@pytest.mark.asyncio
async def test_upload_file(client):
    data = {
        "file": ("test.csv", BytesIO(b"field1,value1\nfield2,value2\n"), "text/csv")
    }
    response = client.post("/api/v1/files/upload", files=data)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["filename"] == "test.csv"
    assert json_data["status"] == "processed"

@pytest.mark.asyncio
async def test_list_files(client):
    response = client.get("/api/v1/files/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
