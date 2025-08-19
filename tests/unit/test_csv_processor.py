import pytest
from app.services import csv_processor, sanitize

def test_sanitize_value():
    assert sanitize.sanitize_value("=CMD") == "'=CMD"
    assert sanitize.sanitize_value("+SUM") == "'+SUM"
    assert sanitize.sanitize_value("normal") == "normal"

@pytest.mark.asyncio
async def test_process_csv(tmp_path):
    # cria CSV temporário
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("field1,value1\nfield2,value2\n")

    # mock file_id e GridFS interaction
    class MockGridFS:
        def find(self, *args, **kwargs):
            class MockOut:
                def read(self):
                    return csv_file.read_bytes()
            return [MockOut()]
    csv_processor.fs_bucket = MockGridFS()

    # mock db
    csv_processor.db = type("DB", (), {"files": type("F", (), {"update_one": lambda *a, **k: None})()})()

    records = await csv_processor.process_csv("mock_id")
    assert len(records) == 1
    assert records[0]["field1"] == "value1"
