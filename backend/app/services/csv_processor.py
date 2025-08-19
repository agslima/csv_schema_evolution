import csv
from app.services.sanitize import sanitize_value
from app.db.mongo import db, fs_bucket
from bson import ObjectId
import io

async def process_csv(file_id: str, id_field: str = None):
    doc = await db.files.find_one({"_id": ObjectId(file_id)})
    if not doc:
        raise ValueError("File not found")

    # read file from GridFS
    grid_out = fs_bucket.find({"filename": doc["filename"]})[0]
    content = grid_out.read()
    text_io = io.StringIO(content.decode("utf-8-sig"))
    
    records = []
    fields_set = set()
    current_record = {}

    reader = csv.reader(text_io)
    for row in reader:
        if not row:
            continue
        field = row[0].strip()
        value = sanitize_value(row[1].strip() if len(row) > 1 else "")
        fields_set.add(field)

        if id_field and field == id_field and current_record:
            records.append(current_record)
            current_record = {}
        elif not id_field and field in current_record:
            records.append(current_record)
            current_record = {}

        current_record[field] = value

    if current_record:
        records.append(current_record)

    # update metadata in Mongo
    await db.files.update_one(
        {"_id": ObjectId(file_id)},
        {"$set": {
            "status": "processed",
            "fields": list(fields_set),
            "records_count": len(records)
        }}
    )
    return records
