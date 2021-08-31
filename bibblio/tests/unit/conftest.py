import boto3
import pytest

import os

os.environ["RAW_NOTES_TABLE"] = "raw-notes"
db_client = boto3.client("dynamodb", endpoint_url="http://localhost:8000")


@pytest.fixture(autouse=True, scope="session")
def create_raw_notes_tables():
    table = {
        "TableName": os.environ.get("RAW_NOTES_TABLE"),
        "AttributeDefinitions": [
            {"AttributeName": "note_id", "AttributeType": "S"},
            {"AttributeName": "s3_upload_bucket", "AttributeType": "S"},
        ],
        "KeySchema": [{"AttributeName": "note_id", "KeyType": "HASH"}],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "s3_upload_bucket",
                "KeySchema": [{"AttributeName": "s3_upload_bucket", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 1,
                    "WriteCapacityUnits": 1,
                },
            }
        ],
        "ProvisionedThroughput": {"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    }
    db_client.create_table(**table)
    yield
    db_client.delete_table(**{"TableName": os.environ["RAW_NOTES_TABLE"]})


@pytest.fixture()
def insert_items():
    request = {
        "Item": {
            'note_id': {"S": "example-note-01"},
            's3_upload_bucket': {"S": "test_bucket"},
            's3_upload_object': {"S": "test_object"},
            'book_title': {"S":"test_title"},
            'book_author': {"S":"test_author"},
            'note_chapter': {"S":"test_chapter"},
            'note_type_and_location': {"S":"test_location"},
            'note_text': {"S":"test_text"},
        },
        "TableName": os.environ["RAW_NOTES_TABLE"],
    }
    db_client.put_item(**request)
    yield db_client
    db_client.delete_item(
        **{
        "TableName": os.environ["RAW_NOTES_TABLE"],
        "Key": {"note_id": {"S": "example-note-01"}}}
    )
