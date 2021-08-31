from typing import List
import boto3
import os
from boto3.dynamodb.conditions import Key

NOTES_TABLE = os.environ.get("TABLE_NAME")
RAW_NOTES_TABLE = 'raw-notes'
SMART_NOTES_TABLE = 'smart-notes'
SNAP_SHOTS_TABLE = 'snap-shots'
USER_TABLE = 'user-table'
DB_ENDPOINT = os.environ.get("DB_ENDPOINT")

class NotesDAO(object):
    """
    Provide a wrapper around the DynamoDB API to fetch Notes from the given table
    """
    def __init__(self, table_name, key_name) -> None:
        """
        params - table_name - string - dynamodb table name
        params - key_name - string - dynamodb table primary key
        """
        DB_ENDPOINT = os.environ.get("DB_ENDPOINT")
        if not DB_ENDPOINT: self.client = boto3.resource("dynamodb")
        else: self.client = boto3.resource("dynamodb", endpoint_url=DB_ENDPOINT)
        self.table_name = table_name
        self.table_connector = self.client.Table(self.table_name)
        self.primary_key = key_name
    def save_notes(self, notes):
        """
        Save notes to dynamodb
        # TODO: handle errors
        params - notes - list - list of notes to save
        returns - boolean - success or not
        """
        for item in notes: response = self.table_connector.put_item(Item = item)
        return True
    def get_notes_by_s3_objkey(self, s3_object_key: str) -> list:
        """
        Return all Note objects corresponding to the given  index = id
        params - s3_object_key - string - s3 object key
        returns - list - items from table
        """
        results = self.table_connector.query(
            IndexName="s3_upload_object",
            KeyConditionExpression=Key('s3_upload_object').eq(s3_object_key),
        )
        return results["Items"] if "Items" in results else []
    def get_item_by_id(self, id):
        """
        Return all Note objects corresponding to the given id
        params - id - string - primary key id
        returns - dict - item from table
        """
        results = self.table_connector.query(
            KeyConditionExpression=Key(self.primary_key).eq(id)
            )
        return results["Items"][0] if "Items" in results else []
    def delete_item_by_id(self, id):
        """
        Delete Note object corresponding to the given id
        params - id - string - primary key id
        returns - None
        """
        response = self.table_connector.delete_item(
            Key={self.primary_key: id}
        )
        print(response)
    def get_item_by_index(self, index_name, id):
        """
        Return all objects corresponding to index = id
        """
        results = self.table_connector.query(
            IndexName=index_name,
            KeyConditionExpression=Key(index_name).eq(id),
        )
        return results["Items"] if "Items" in results else []

class RawNotesDAO(NotesDAO):
    def __init__(self, table_name = RAW_NOTES_TABLE, key_name='note_id') -> None:
        super().__init__(table_name, key_name)

class SmartNotesDAO(NotesDAO):
    def __init__(self, table_name = SMART_NOTES_TABLE, key_name='smart_note_id') -> None:
        super().__init__(table_name, key_name)

class SnapShotsDAO(NotesDAO):
    def __init__(self, table_name = SNAP_SHOTS_TABLE, key_name='snap_shot_id') -> None:
        super().__init__(table_name, key_name)

    def get_snaps_by_userid(self, user_id: str) -> list:
        """
        Return all Note objects corresponding to the given 'user_id'
        """
        results = self.table_connector.query(
            IndexName="user_id",
            KeyConditionExpression=Key('user_id').eq(user_id),
        )
        if "Items" in results:
            return results["Items"]
        return []
    def get_snaps_by_date(self, date: str) -> list:
        """
        Return all Note objects corresponding to the given 'user_id'
        """
        results = self.table_connector.query(
            IndexName="delivery_date",
            KeyConditionExpression=Key('delivery_date').eq(date),
        )
        if "Items" in results:
            return results["Items"]
        return []

class UserDAO():
    def __init__(self, table_name = USER_TABLE) -> None:
        DB_ENDPOINT = os.environ.get("DB_ENDPOINT")
        if not DB_ENDPOINT: self.client = boto3.resource("dynamodb")
        else: self.client = boto3.resource("dynamodb", endpoint_url=DB_ENDPOINT)
        self.table_name = table_name
        self.table_connector = self.client.Table(self.table_name)
    def get_user_by_userid(self, user_id):
        response = self.table_connector.query(
            KeyConditionExpression=Key('user_id').eq(user_id)
            )
        return response['Items'][0]
    def create_user(self, user_id, email_id):
        response = self.table_connector.put_item(
            Item = {
                'user_id' : "test_user",
                'email_id': "yashvardhannevatia@gmail.com"
            }
        )
