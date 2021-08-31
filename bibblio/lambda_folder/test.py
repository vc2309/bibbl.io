
from dao.raw_notes_dao import RawNotesDAO, SmartNotesDAO, SnapShotsDAO, UserDAO
from dao.s3_dao import S3Dao
from engine.raw_note_engine import RawNoteEngine, SmartNoteEngine, SnapShotEngine
from engine.email_engine import EmailEngine
import boto3
import pytest
import os
import json
import app

bucket_name = "bibbl-notefilebucket-1v8xy57fre02p"
bucket_arn = "arn:aws:s3:::bibbl-notefilebucket-1v8xy57fre02p"
object_key = "test_user/Extreme Economies-Notebook.html"
RAW_NOTES_TABLE = 'raw-notes'
SMART_NOTES_TABLE = 'smart-notes'
SNAP_SHOTS_TABLE = 'snap-shots'
USER_TABLE = 'user-table'
db_client = boto3.client("dynamodb", endpoint_url="http://localhost:8000")
test_note_number = 21
s3_dao = S3Dao()
raw_notes_dao = RawNotesDAO(RAW_NOTES_TABLE)
smart_notes_dao = SmartNotesDAO(SMART_NOTES_TABLE)
snap_shot_dao = SnapShotsDAO(SNAP_SHOTS_TABLE)

# print(len(raw_notes_dao.get_notes_by_objkey(object_key)))
# print("Testing smart notes engine")
# smart_notes_engine = SmartNoteEngine()
# print(len(smart_notes_engine.parse_raw_notes(object_key,raw_notes_dao)))
# print("-----Testing smart notes dao-----")
# smart_notes_dao = SmartNotesDAO(RAW_NOTES_TABLE)
# print(len(smart_notes_dao.get_notes_by_objkey(object_key)))


@pytest.fixture()
def apigw_event():
    """Generates API GW Event"""
    os.environ["AWS_SAM_STACK_NAME"] = "bibbl"

    return {
        "body": '{ "test": "body"}',
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": "",
            },
            "stage": "prod",
        },
        "queryStringParameters": {"foo": "bar"},
        "headers": {
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country": "US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Port": "443",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "Accept-Encoding": "gzip, deflate, sdch",
        },
        "pathParameters": {"proxy": "/examplepath"},
        "httpMethod": "POST",
        "stageVariables": {"baz": "qux"},
        "path": "/examplepath",
    }

@pytest.fixture()
def s3_event():
    """Generates API GW Event"""
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

@pytest.fixture(autouse=True, scope="session")
def create_raw_notes_tables():
    table = {
        "TableName": RAW_NOTES_TABLE,
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
                    "ReadCapacityUnits": 1,
                    "WriteCapacityUnits": 1,
                },
            }
        ],
        "ProvisionedThroughput": {"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    }
    db_client.create_table(**table)
    yield
    db_client.delete_table(**{"TableName": RAW_NOTES_TABLE})

@pytest.fixture(autouse=True, scope="session")
def create_smart_notes_tables():
    table = {
        "TableName": SMART_NOTES_TABLE,
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
                    "ReadCapacityUnits": 1,
                    "WriteCapacityUnits": 1,
                },
            }
        ],
        "ProvisionedThroughput": {"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    }
    db_client.create_table(**table)
    yield
    db_client.delete_table(**{"TableName": SMART_NOTES_TABLE})

@pytest.fixture(autouse=True, scope="session")
def create_snap_shots_tables():
    table = {
        "TableName": SNAP_SHOTS_TABLE,
        "AttributeDefinitions": [
            {"AttributeName": "snap_shot_id", "AttributeType": "S"},
            {"AttributeName": "user_id", "AttributeType": "S"},
            {"AttributeName": "delivery_date", "AttributeType": "S"},
        ],
        "KeySchema": [{"AttributeName": "snap_shot_id", "KeyType": "HASH"}],
        "GlobalSecondaryIndexes": [
            {
                "IndexName": "user_id",
                "KeySchema": [{"AttributeName": "user_id", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 1,
                    "WriteCapacityUnits": 1,
                },
            },
            {
                "IndexName": "delivery_date",
                "KeySchema": [{"AttributeName": "delivery_date", "KeyType": "HASH"}],
                "Projection": {"ProjectionType": "ALL"},
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 1,
                    "WriteCapacityUnits": 1,
                },
            },
        ],
        "ProvisionedThroughput": {"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    }
    db_client.create_table(**table)
    yield
    db_client.delete_table(**{"TableName": SNAP_SHOTS_TABLE})

@pytest.fixture(autouse=True, scope="session")
def create_user_tables():
    table = {
        "TableName": USER_TABLE,
        "AttributeDefinitions": [
            {"AttributeName": "user_id", "AttributeType": "S"},
        ],
        "KeySchema": [{"AttributeName": "user_id", "KeyType": "HASH"}],
        "ProvisionedThroughput": {"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
    }
    db_client.create_table(**table)
    yield
    db_client.delete_table(**{"TableName": USER_TABLE})

def test_note_file_handler(s3_event):
    app.note_file_handler(s3_event, "")
    assert test_note_number == len(smart_notes_dao.get_item_by_index('s3_upload_object', object_key))
    assert 0 <  len(snap_shot_dao.get_item_by_index('user_id', 'test_user'))

def test_email():
    items = snap_shot_dao.get_item_by_index('delivery_date', '2021-09-01')
    snap_engine = SnapShotEngine()
    user_dao = UserDAO()
    user_dao.create_user('test_user', 'yashvardhannevatia@gmail.com')
    email_id = user_dao.get_user_by_userid('test_user')['email_id']
    email_engine = EmailEngine()
    for item in items:
        content = snap_engine.get_snap_content_by_snap_id(item['snap_shot_id'], snap_shot_dao, smart_notes_dao)
        email_engine.send_email(email_id, content)

# def test_send_snap():
#     user_dao = UserDAO()
#     user_dao.create_user('test_user', 'yashvardhannevatia@gmail.com')
#     email_id = user_dao.get_user_by_userid('test_user')['email_id']
#     print(email_id)
#     content = SnapShotEngine().get_snap_content('test_user', snap_shot_dao, smart_notes_dao)
#     print(content)
    # send email here

# def test_snap_content():
#     snap_engine = SnapShotEngine()
#     content = snap_engine.get_snap_content('test_user', snap_shot_dao, smart_notes_dao)
#     print(content)

# def test_raw_notes_dao():
#
#     obj = {
#             'note_id' : 'test_note_id',
#             'user_id' : 'test_user',
#             's3_upload_bucket' : 'test_bucket',
#             's3_upload_object' : 'test_object',
#             'book_title' : 'test_title',
#             'book_author': 'test_author',
#             'note_chapter': 'test_chapter',
#             'note_type_and_location': 'test_location',
#             'note_text': 'note_text'
#         }
#     raw_notes_dao.save_notes([obj])
#     assert 1 == len(raw_notes_dao.get_notes_by_objkey('test_object'))
#
# def test_test_handler(apigw_event):
#     ret = app.test_handler(apigw_event, "")
#     data = json.loads(ret["body"])
#     assert ret["statusCode"] == 200
#     assert "message" in ret["body"]
#     assert data["message"] == "hello world"
#
# def test_kindle_parser():
#     parser = RawNoteEngine()
#     ret = parser.parse_kindle_file(bucket_name, object_key, 'test_user', s3_dao)
#     assert len(ret) == test_note_number
#     assert ret[0]['book_title'] == 'Extreme Economies\n'
#
# def test_s3_dao():
#     body = s3_dao.get_kindle_file(bucket_name, object_key)
#     assert isinstance(body, str)



# def test_snap_creation():
#     snap_engine = SnapShotEngine()
#     snaps = snap_engine.create_snaps(object_key,smart_notes_dao)
#     snap_shot_dao.save
#     assert len(snaps) > 0


# @pytest.fixture()
# def insert_items():
#     request = {
#         "Item": {
#             'note_id': {"S": "example-note-01"},
#             's3_upload_bucket': {"S": "test_bucket"},
#             's3_upload_object': {"S": "test_object"},
#             'book_title': {"S":"test_title"},
#             'book_author': {"S":"test_author"},
#             'note_chapter': {"S":"test_chapter"},
#             'note_type_and_location': {"S":"test_location"},
#             'note_text': {"S":"test_text"},
#         },
#         "TableName": RAW_NOTES_TABLE,
#     }
#     db_client.put_item(**request)
#     yield db_client
#     db_client.delete_item(
#         **{
#         "TableName": RAW_NOTES_TABLE,
#         "Key": {"note_id": {"S": "example-note-01"}}}
#     )
# def test_fetch_notes(insert_items):
#     raw_notes_dao = RawNotesDao()
#     request = {
#         "TableName": RAW_NOTES_TABLE,
#         "IndexName" : 's3_upload_object',
#         "KeyConditionExpression": "s3_upload_object = :v1",
#         "ExpressionAttributeValues": {":v1": {"S": "test_object"}},
#     }
#     print(insert_items.query(**request))

# def get_snap_content_by_user_id(self, user_id, snap_shots_dao = None, smart_notes_dao = None):
#     """
#         Ignore this function
#     """
#     if not snap_shots_dao: snap_shots_dao = SnapShotsDAO()
#     snap = snap_shots_dao.get_snaps_by_userid(user_id)[0]
#     if not smart_notes_dao: smart_notes_dao  = SmartNotesDAO()
#     content = {'notes':[], 'book_title': ''}
#     for smart_note_id in snap['smart_note_list']:
#         smart_note = smart_notes_dao.get_item_by_id('smart_note_id', smart_note_id)
#         if not content['book_title']: content['book_title'] = smart_note['book_title']
#         content['notes'].append(smart_note['note_text'])
#     return content
