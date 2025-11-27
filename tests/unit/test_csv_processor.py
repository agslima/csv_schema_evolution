import pytest
from app.services import csv_processor, sanitize

def test_sanitize_value():
    """Test CSV injection prevention for dangerous prefixes."""
    assert sanitize.sanitize_value("=CMD") == "'=CMD"
    assert sanitize.sanitize_value("+SUM") == "'+SUM"
    assert sanitize.sanitize_value("-SYSTEM") == "'-SYSTEM"
    assert sanitize.sanitize_value("@IMPORT") == "'@IMPORT"
    assert sanitize.sanitize_value("normal") == "normal"
    assert sanitize.sanitize_value("") == ""
    assert sanitize.sanitize_value("123") == "123"

def test_sanitize_value_edge_cases():
    """Test sanitize with edge cases."""
    # Single character dangerous prefix
    assert sanitize.sanitize_value("=") == "'="
    # Dangerous prefix in middle (should not be sanitized)
    assert sanitize.sanitize_value("text=value") == "text=value"
    # Multiple characters of same dangerous prefix
    assert sanitize.sanitize_value("===DANGER") == "'===DANGER"

@pytest.mark.asyncio
async def test_process_csv(tmp_path):
    """Test CSV processing with basic fields and values."""
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

@pytest.mark.asyncio
async def test_process_csv_with_injection(tmp_path):
    """Test CSV processing sanitizes dangerous values."""
    csv_file = tmp_path / "injection.csv"
    csv_file.write_text("formula,=MALICIOUS()\nemail,+CMD\nname,@SYSTEM\n")

    class MockGridFS:
        def find(self, *args, **kwargs):
            class MockOut:
                def read(self):
                    return csv_file.read_bytes()
            return [MockOut()]
    csv_processor.fs_bucket = MockGridFS()

    csv_processor.db = type("DB", (), {"files": type("F", (), {"update_one": lambda *a, **k: None})()})()

    records = await csv_processor.process_csv("mock_id")
    assert records[0]["formula"] == "'=MALICIOUS()"
    assert records[1]["email"] == "'+CMD"
    assert records[2]["name"] == "'@SYSTEM"
