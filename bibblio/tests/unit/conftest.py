import boto3
import pytest
import os

os.environ["RAW_NOTE_TABLE_NAME"] = "my-table"
os.environ["SMART_NOTE_TABLE_NAME"] = "smart-notes-table-test"
os.environ["SNAPSHOTS_TABLE_NAME"] = "snapshots-table-test"
os.environ["USER_TABLE_NAME"] = "user-table-test"
os.environ["DB_ENDPOINT"] = "http://localhost:8000"
db_client = boto3.client("dynamodb", endpoint_url="http://localhost:8000")
from lambda_folder.pkg.dao import NotesDAO, SmartNotesDAO, SnapShotsDAO, RawNotesDAO


@pytest.fixture(autouse=True, scope="session")
def create_tables():
    note_table_name, smart_note_table_name, snapshots_table_name, user_table_name = (
        os.environ.get("RAW_NOTE_TABLE_NAME"),
        os.environ.get("SMART_NOTE_TABLE_NAME"),
        os.environ.get("SNAPSHOTS_TABLE_NAME"),
        os.environ.get("USER_TABLE_NAME")
    )
    table = {
        "TableName": note_table_name,
        "AttributeDefinitions": [
            {"AttributeName": "note_id", "AttributeType": "S"},
            {"AttributeName": "s3_upload_object", "AttributeType": "S"},
        ],
        "KeySchema": [{"AttributeName": "note_id", "KeyType": "HASH"}],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "s3_upload_object",
                "KeySchema": [{"AttributeName": "s3_upload_object", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5,
                },
            }
        ],
        "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    }

    smart_note_table = {
        "TableName": smart_note_table_name,
        "AttributeDefinitions": [
            {"AttributeName": "smart_note_id", "AttributeType": "S"},
            {"AttributeName": "s3_upload_object", "AttributeType": "S"},
        ],
        "KeySchema": [{"AttributeName": "smart_note_id", "KeyType": "HASH"}],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "s3_upload_object",
                "KeySchema": [{"AttributeName": "s3_upload_object", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5,
                },
            }
        ],
        "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    }

    snapshots_table = {
        "TableName": snapshots_table_name,
        "AttributeDefinitions": [
            {"AttributeName": "snap_shot_id", "AttributeType": "S"},
            {"AttributeName": "s3_upload_object", "AttributeType": "S"},
            {"AttributeName": "user_id", "AttributeType": "S"},
        ],
        "KeySchema": [{"AttributeName": "snap_shot_id", "KeyType": "HASH"}],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "s3_upload_object",
                "KeySchema": [{"AttributeName": "s3_upload_object", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5,
                },
            },
            {
                "IndexName": "user_id",
                "KeySchema": [{"AttributeName": "user_id", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5,
                },
            },
        ],
        "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    }

    user_table = {
        "TableName": user_table_name,
        "AttributeDefinitions": [
            {"AttributeName": "user_id", "AttributeType": "S"},
        ],
        "KeySchema": [{"AttributeName": "user_id", "KeyType": "HASH"}],
        "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    }
    def delete_tables():
        db_client.delete_table(**{"TableName": note_table_name})
        db_client.delete_table(**{"TableName": smart_note_table_name})
        db_client.delete_table(**{"TableName": snapshots_table_name})
        db_client.delete_table(**{"TableName": user_table_name})
    try:
        db_client.create_table(**table)
        db_client.create_table(**smart_note_table)
        db_client.create_table(**snapshots_table)
        db_client.create_table(**user_table)
    except Exception as e:
        print("Error thrown : ", e)
        delete_tables()
        return
    yield
    delete_tables()

@pytest.fixture()
def insert_user():
    request = {
        "Item": {
            "user_id": {"S": "user01"},
            "email_id": {"S": "yashvardhannevatia@gmail.com"},
            "notes_in_snap": {"N": "3"},
        },
        "TableName": "user-table-test",
    }
    db_client.put_item(**request)

@pytest.fixture()
def insert_smart_notes():
    request = {
        "Item": {
            "smart_note_id": {"S": "example-smart-note-01"},
            "text": {"S": "abcd 1234"},
            "s3_upload_object": {"S": "vishnu.com"},
        },
        "TableName": "smart-notes-table-test",
    }
    db_client.put_item(**request)
    request = {
        "Item": {
            "smart_note_id": {"S": "example-smart-note-02"},
            "text": {"S": "xyz 1234"},
            "s3_upload_object": {"S": "vishnu.com"},
        },
        "TableName": "smart-notes-table-test",
    }
    db_client.put_item(**request)
    yield db_client
    db_client.batch_write_item(
        **{
            "RequestItems": {
                os.environ["SMART_NOTE_TABLE_NAME"]: [
                    {
                        "DeleteRequest": {
                            "Key": {"smart_note_id": {"S": "example-smart-note-01"}}
                        },
                        "DeleteRequest": {
                            "Key": {"smart_note_id": {"S": "example-smart-note-02"}}
                        },
                        "DeleteRequest": {
                            "Key": {"smart_note_id": {"S": "example-smart-note-03"}}
                        },
                    }
                ]
            }
        }
    )


@pytest.fixture()
def insert_snapshots():
    request = {
        "Item": {
            "snap_shot_id": {"S": "example-snapshot-01"},
            "user_id": {"S": "user01"},
            "s3_upload_object": {"S": "vishnu.com"},
            "smart_note_ids": {"SS": ["smart-note01", "smart-note02"]},
            "delivery_status": {"S": "Pending"},
            "delivery_date": {"S": "2021-01-01"},
        },
        "TableName": "snapshots-table-test",
    }
    db_client.put_item(**request)
    request = {
        "Item": {
            "snap_shot_id": {"S": "example-snapshot-02"},
            "user_id": {"S": "user01"},
            "s3_upload_object": {"S": "vishnu.com"},
            "smart_note_ids": {"SS": ["smart-note03", "smart-note02"]},
            "delivery_status": {"S": "Pending"},
            "delivery_date": {"S": "2021-01-02"},
        },
        "TableName": "snapshots-table-test",
    }
    db_client.put_item(**request)
    request = {
        "TableName": "snapshots-table-test",
        "IndexName": "user_id",
        "KeyConditionExpression": "user_id = :v1",
        "ExpressionAttributeValues": {":v1": {"S": "user01"}},
    }
    print(request)
    results = db_client.query(**request)
    print(results)
    yield db_client


@pytest.fixture()
def insert_items():
    request = {
        "Item": {
            "note_id": {"S": "example-note-01"},
            "text": {"S": "abcd"},
            "s3_upload_object": {"S": "vishnu.com"},
        },
        "TableName": os.environ["RAW_NOTE_TABLE_NAME"],
    }
    db_client.put_item(**request)
    yield db_client
    db_client.delete_item(
        **{"TableName": "my-table", "Key": {"note_id": {"S": "example-note-01"}}}
    )


@pytest.fixture()
def notes_dao():
    return RawNotesDAO()


@pytest.fixture()
def smart_notes_dao():
    return SmartNotesDAO()


@pytest.fixture()
def snapshots_dao():
    return SnapShotsDAO()
