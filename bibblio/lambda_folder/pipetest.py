
import os
import app
import boto3


bucket_name = "bibbl-notefilebucket-3fsrntx5wcnu"
bucket_arn = "arn:aws:s3:::bibbl-notefilebucket-3fsrntx5wcnu"
object_key = "test_user/Extreme Economies-Notebook.html"
os.environ["DB_ENDPOINT"] = "http://localhost:8000"
db_client = boto3.client("dynamodb", endpoint_url="http://localhost:8000")
note_table_name, smart_note_table_name, snapshots_table_name, user_table_name = (
    'raw-notes',
    'smart-notes',
    'snap-shots',
    'user-table'
)

def s3_event():
    """Generates S3 Event"""
    os.environ["AWS_SAM_STACK_NAME"] = "bibbl"
    return {
    "Records": [
    {
      "eventVersion": "2.0",
      "eventSource": "aws:s3",
      "awsRegion": "us-west-2",
      "eventTime": "1970-01-01T00:00:00.000Z",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "EXAMPLE"
      },
      "requestParameters": {
        "sourceIPAddress": "127.0.0.1"
      },
      "responseElements": {
        "x-amz-request-id": "EXAMPLE123456789",
        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
      },
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "testConfigRule",
        "bucket": {
          "name": bucket_name,
          "ownerIdentity": {
            "principalId": "EXAMPLE"
          },
          "arn": bucket_arn
        },
        "object": {
          "key": object_key,
          "size": 1024,
          "eTag": "0123456789abcdef0123456789abcdef",
          "sequencer": "0A1B2C3D4E5F678901"
        }
      }
    }
  ]
}

def create():
    print("Creating tables")
    delete()
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
            {"AttributeName": "delivery_date", "AttributeType": "S"},
            {"AttributeName": "user_id", "AttributeType": "S"},
        ],
        "KeySchema": [{"AttributeName": "snap_shot_id", "KeyType": "HASH"}],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "user_id",
                "KeySchema": [{"AttributeName": "user_id", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5,
                },
            },
            {
                "IndexName": "delivery_date",
                "KeySchema": [{"AttributeName": "delivery_date", "KeyType": "HASH"}],
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
    try:
        db_client.create_table(**table)
        db_client.create_table(**smart_note_table)
        db_client.create_table(**snapshots_table)
        db_client.create_table(**user_table)
        create_user()
    except Exception as e:
        print("Error thrown : ", e)
        delete_tables()
        return

def create_user():
    request = {
        "Item": {
            "user_id": {"S": "test_user"},
            "email_id": {"S": "yashvardhannevatia@gmail.com"},
            "notes_in_snap": {"N": "1"},
        },
        "TableName": user_table_name,
    }
    db_client.put_item(**request)

def delete():
    try:
        db_client.delete_table(**{"TableName": note_table_name})
        db_client.delete_table(**{"TableName": smart_note_table_name})
        db_client.delete_table(**{"TableName": snapshots_table_name})
        db_client.delete_table(**{"TableName": user_table_name})
    except Exception as e:
        print("Error thrown : ", e)

def run():
    ret =  app.note_file_handler(s3_event(), "")
    app.snap_delivery_handler("","")

create()
# delete_tables()
# create_tables()
# test_note_file_handler()
# delete_tables()
