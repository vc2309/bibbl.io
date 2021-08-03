import boto3
import os
from models import Snapshot, SmartNote
import uuid
DB_ENDPOINT = os.environ.get("DD_ENDPOINT")
SNAPSHOTS_TABLE = os.environ.get("SNAPSHOTS_TABLE_NAME")

class SnapshotsDAO(object):
    """
    Provide a wrapper around the DynamoDB API to fetch Notes from the given table
    """

    def __init__(self, table_name = SNAPSHOTS_TABLE) -> None:
        self.client = db_client = boto3.client("dynamodb", endpoint_url=DB_ENDPOINT)
        self.table_name = table_name

    def get_snapshots_by_upload_uri(self, upload_uri: str) -> list:
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

    def get_snapshots_by_user_id(self, user_id: str) -> list:
        """
        Return all Note objects corresponding to the given 'user_id'
        """
        request = {
            "TableName": self.table_name,
            "IndexName": "user_id",
            "KeyConditionExpression": "user_id = :v1",
            "ExpressionAttributeValues": {":v1": {"S": str(user_id)}},
        }
        results = self.client.query(**request)
        if "Items" in results:
            return results["Items"]
        return [] 

    def write_snapshot(self, snapshot: Snapshot):
        item = {}
        item["snapshot_id"]["S"] = snapshot.snapshot_id
        item["book_id"]["S"] = snapshot.book_id
        item["user_id"]["S"] = snapshot.user_id
        item["smart_note_ids"]["SS"] = [smart_note.smart_note_id for smart_note in snapshot.smart_notes]
        request = {
            "Item" : item,
            "TableName" : self.table_name
        }
        self.client.put_item(**request)