import io
import csv
from backend.processor import process_csv

def test_basic_transpose():
    input_data = """Name,Value\nAccount,user1@mail.com\ncn,User One\n"""
        infile = io.StringIO(input_data)
            outfile, log = process_csv(infile, delimiter=",", schema_evolution=True, generate_log=False)

                reader = csv.reader(io.StringIO(outfile.getvalue()))
                    rows = list(reader)
                        
                            assert rows[0] == ["Account", "cn"]
                                assert rows[1][0] == "user1@mail.com"
                                    assert rows[1][1] == "User One"

                                    def test_log_generation():
                                        input_data = "Name,Value\nAccount,user1@mail.com\nAccount,user2@mail.com\n"""
                                            infile = io.StringIO(input_data)
                                                outfile, log = process_csv(infile, delimiter=",", schema_evolution=True, generate_log=True)

                                                    log_reader = csv.reader(io.StringIO(log.getvalue()))
                                                        log_rows = list(log_reader)
                                                            assert log_rows[0] == ["Field", "Occurrences"]
                                                                assert any("Account" in row for row in log_rows)