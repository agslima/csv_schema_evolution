# ***************************************************************************
# *                                                                         *                                                                
# *   CSV Data Transposition and Evolution                                  *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU General Public License for more details.                          *
# *                                                                         *
# *   You should have received a copy of the GNU General Public License     *
# *   along with this program. If not, see <http://www.gnu.org/licenses/>.  *
# *                                                                         *
# ***************************************************************************

import csv
import argparse
from collections import OrderedDict, Counter
import os

def detect_delimiter(file_path):
    """Detect CSV delimiter automatically."""
    try:
        with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
            sample = f.read(8192)
            f.seek(0)
            return csv.Sniffer().sniff(sample, delimiters=[",", ";", "\t", "|"]).delimiter
    except Exception:
        with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
            first_line = f.readline()
        return ";" if first_line.count(";") > first_line.count(",") else ","

def read_records(input_files):
    """
    Read all records and dynamically detect new fields (schema evolution).
    Returns:
        - fields (list of str): all detected column names
        - records (list of OrderedDict): all records aligned to the final schema
        - counts (Counter): occurrences of each field name
    """
    fields = []
    records = []
    counts = Counter()

    for file_path in input_files:
        delim = detect_delimiter(file_path)
        print(f"[INFO] Processing '{file_path}' with detected delimiter '{delim}'")

        current_record = OrderedDict((c, "") for c in fields)

        with open(file_path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f, delimiter=delim)
            for row in reader:
                if not row:
                    continue
                field_name = row[0].strip()
                value = row[1].strip() if len(row) > 1 else ""
                counts[field_name] += 1

                # New record detection
                if fields and field_name == fields[0] and current_record[fields[0]]:
                    records.append(current_record)
                    current_record = OrderedDict((c, "") for c in fields)

                # New field detected mid-processing
                if field_name not in fields:
                    fields.append(field_name)
                    # Add this new field to all previous records
                    for r in records:
                        r[field_name] = ""
                    current_record[field_name] = ""

                current_record[field_name] = value

        if any(v != "" for v in current_record.values()):
            records.append(current_record)

    return fields, records, counts

def write_csv(output_file, fields, records, out_delim):
    """Write transposed CSV with updated schema."""
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter=out_delim)
        writer.writerow(fields)
        for record in records:
            writer.writerow([record.get(c, "") for c in fields])

def write_log(log_file, counts):
    """Write CSV log of field occurrence counts."""
    if not log_file:
        return
    os.makedirs(os.path.dirname(log_file), exist_ok=True) if os.path.dirname(log_file) else None
    with open(log_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["field", "occurrences"])
        for field, count in counts.most_common():
            writer.writerow([field, count])

def process_files(input_files, output_file, out_delim, log_file):
    fields, records, counts = read_records(input_files)
    write_csv(output_file, fields, records, out_delim)
    write_log(log_file, counts)
    print(f"Output file created: {output_file}")
    if log_file:
        print(f"Field occurrence log saved: {log_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSV transposer with schema evolution (dynamic fields).")
    parser.add_argument("inputs", nargs="+", help="One or more input CSV files (key,value format).")
    parser.add_argument("-o", "--out", required=True, help="Output CSV file.")
    parser.add_argument("--out-delim", default=",", help="Output CSV delimiter (default: ',').")
    parser.add_argument("--log", help="Optional CSV file for field occurrence log.")
    args = parser.parse_args()

    process_files(args.inputs, args.out, args.out_delim, args.log)

