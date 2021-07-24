import boto3
import pytest

import os

os.environ["TABLE_NAME"] = "my-table"
db_client = boto3.client("dynamodb", endpoint_url="http://localhost:8000")


@pytest.fixture(autouse=True, scope="session")
def create_tables():
    table = {
        "TableName": os.environ.get("TABLE_NAME"),
        "AttributeDefinitions": [
            {"AttributeName": "note-id", "AttributeType": "S"},
            {"AttributeName": "upload_uri", "AttributeType": "S"},
        ],
        "KeySchema": [{"AttributeName": "note-id", "KeyType": "HASH"}],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "upload_uri",
                "KeySchema": [{"AttributeName": "upload_uri", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5,
                },
            }
        ],
        "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    }
    db_client.create_table(**table)
    yield
    db_client.delete_table(**{"TableName": os.environ.get("TABLE_NAME")})


@pytest.fixture()
def insert_items():
    request = {
        "Item": {
            "note-id": {"S": "example-note-01"},
            "text": {"S": "abcd"},
            "upload_uri": {"S": "vishnu.com"},
        },
        "TableName": os.environ["TABLE_NAME"],
    }
    db_client.put_item(**request)
    yield db_client
    db_client.delete_item(
        **{"TableName": "my-table", "Key": {"note-id": {"S": "example-note-01"}}}
    )
