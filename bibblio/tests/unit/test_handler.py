import sys
import os

import json
import pytest
from lambda_folder import app
# import os
# import boto3
# from engine.raw_note_engine import RawNoteEngine
# from dao.s3_dao import S3Dao


bucket_name = "bibbl-notefilebucket-1qokiqtl0hkfp"
bucket_arn = "arn:aws:s3:::bibbl-notefilebucket-1qokiqtl0hkfp"
object_key = "test_user/Being Mortal-Notebook.html"


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

def test_test_handler(apigw_event):
    ret = app.test_handler(apigw_event, "")
    data = json.loads(ret["body"])
    assert ret["statusCode"] == 200
    assert "message" in ret["body"]
    assert data["message"] == "hello world"

def test_note_file_handler(s3_event):
    ret =  app.note_file_handler(s3_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "message" in ret["body"]
    assert data["message"] == "hello world"

def test_fetch_notes(insert_items):
    request = {
        "TableName": os.environ["RAW_NOTES_TABLE"],
        "IndexName" : 's3_upload_bucket',
        "KeyConditionExpression": "s3_upload_bucket = :v1",
        "ExpressionAttributeValues": {":v1": {"S": "test_bucket"}},
    }
    # print(insert_items())
    print(insert_items.query(**request))

def test_kindle_parser():
    parser = RawNoteEngine()
    ret = parser.parse_kindle_file(bucket_name, object_key)
    assert len(ret) == 21
    assert ret[0]['book_title'] == 'Extreme Economies\n'

def test_s3_dao():
    s3_dao = S3Dao()
    body = s3_dao.get_kindle_file(bucket_name, object_key)
    # print(type(body))
    assert isinstance(body, str)
