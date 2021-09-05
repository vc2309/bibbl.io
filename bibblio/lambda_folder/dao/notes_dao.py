from typing import List
import boto3
import os
from boto3.dynamodb.conditions import Key
from lambda_folder.dao import DAOBase

NOTES_TABLE = os.environ.get("TABLE_NAME")
RAW_NOTES_TABLE = os.environ.get("RAW_NOTE_TABLE_NAME") or 'raw-notes'
SMART_NOTES_TABLE = os.environ.get("SMART_NOTE_TABLE_NAME") or 'smart-notes'
DB_ENDPOINT = os.environ.get("DB_ENDPOINT")

class NotesDAO(DAOBase):
    """
    Provide a wrapper around the DynamoDB API to fetch Notes from the given table
    """

    def __init__(self, table_name, key_name) -> None:
        super().__init__(table_name, key_name)

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
        try:
            results = self.table_connector.query(
                IndexName="s3_upload_object",
                KeyConditionExpression=Key('s3_upload_object').eq(s3_object_key),
            )
            return results["Items"] if "Items" in results else []
        except Exception as e:
            print(e)
            return []


class RawNotesDAO(NotesDAO):
    def __init__(self, table_name = RAW_NOTES_TABLE, key_name='note_id') -> None:
        super().__init__(table_name, key_name)

class SmartNotesDAO(NotesDAO):
    def __init__(self, table_name = SMART_NOTES_TABLE, key_name='smart_note_id') -> None:
        super().__init__(table_name, key_name)

