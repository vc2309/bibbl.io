from typing import List
import boto3
import os

NOTES_TABLE = os.environ.get("TABLE_NAME")
SMART_NOTES_TABLE = os.environ.get("SMART_NOTE_TABLE_NAME")
DB_ENDPOINT = os.environ.get("DD_ENDPOINT")


class NotesDAO(object):
    """
    Provide a wrapper around the DynamoDB API to fetch Notes from the given table
    """

    def __init__(self, table_name = NOTES_TABLE) -> None:
        self.client = db_client = boto3.client("dynamodb", endpoint_url=DB_ENDPOINT)
        self.table_name = table_name

    def get_notes_by_upload_uri(self, upload_uri: str) -> List[dict]:
        """
        Return all Note objects corresponding to the given 'upload_uri'
        """
        request = {
            "TableName": self.table_name,
            "IndexName": "upload_uri",
            "KeyConditionExpression": "upload_uri = :v1",
            "ExpressionAttributeValues": {":v1": {"S": str(upload_uri)}},
        }
        results = self.client.query(**request)
        if "Items" in results:
            return results["Items"]
        return []

class SmartNotesDAO(NotesDAO):
    def __init__(self) -> None:
        super().__init__(table_name=SMART_NOTES_TABLE)
    

