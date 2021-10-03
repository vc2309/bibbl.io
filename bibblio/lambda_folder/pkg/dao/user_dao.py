from typing import List
import boto3
import os
from boto3.dynamodb.conditions import Key

USER_TABLE = os.environ.get("USER_TABLE_NAME") or "user-table"

class UserDAO:
    def __init__(self, table_name=USER_TABLE) -> None:
        DB_ENDPOINT = os.environ.get("DB_ENDPOINT")
        if not DB_ENDPOINT:
            self.client = boto3.resource("dynamodb")
        else:
            self.client = boto3.resource("dynamodb", endpoint_url=DB_ENDPOINT)
        self.table_name = table_name
        self.table_connector = self.client.Table(self.table_name)

    def get_user_by_userid(self, user_id):
        response = self.table_connector.query(
            KeyConditionExpression=Key("user_id").eq(user_id)
        )
        return response["Items"][0]

    def create_user(self, user_id, email_id):
        response = self.table_connector.put_item(
            Item={"user_id": "test_user", "email_id": "yashvardhannevatia@gmail.com"}
        )
