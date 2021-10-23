from typing import List
import boto3
import os
from boto3.dynamodb.conditions import Key

USER_TABLE = os.environ.get("USER_TABLE_NAME") or "user-table"
USER_POOL_ID = os.environ.get("USER_POOL_ID")


class UserDAO:
    def __init__(self, table_name=USER_TABLE) -> None:
        DB_ENDPOINT = os.environ.get("DB_ENDPOINT")
        if not DB_ENDPOINT:
            self.client = boto3.resource("dynamodb")
        else:
            self.client = boto3.resource("dynamodb", endpoint_url=DB_ENDPOINT)
        self.table_name = table_name
        self.table_connector = self.client.Table(self.table_name)
        self.cognito = boto3.client("cognito-idp")

    def get_email_by_userid(self, user_id):
        try:
            response = self.cognito.admin_get_user(
                UserPoolId=USER_POOL_ID, Username=user_id
            )
            for attribute in response["UserAttributes"]:
                if attribute["Name"] == "email":
                    return attribute["Value"]
        except Exception as e:
            print("Caught erro while fetching user details : ", e)

    def create_user(self, user_id, email_id):
        response = self.table_connector.put_item(
            Item={"user_id": "test_user", "email_id": "yashvardhannevatia@gmail.com"}
        )
