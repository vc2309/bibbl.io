from boto3.dynamodb.conditions import Key
from . import DAOBase
import os

SNAP_SHOTS_TABLE = os.environ.get("SNAPSHOTS_TABLE_NAME") or "snap-shots"


class SnapShotsDAO(DAOBase):
    def __init__(self, table_name=SNAP_SHOTS_TABLE, key_name="snap_shot_id") -> None:
        super().__init__(table_name, key_name)

    def get_snapshots_by_user_id(self, user_id: str) -> list:
        """
        Return all Note objects corresponding to the given 'user_id'
        """
        results = self.table_connector.query(
            IndexName="user_id",
            KeyConditionExpression=Key("user_id").eq(user_id),
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
            KeyConditionExpression=Key("delivery_date").eq(date),
        )
        if "Items" in results:
            return results["Items"]
        return []

    def save_snapshot(self, notes):
        """
        Save notes to dynamodb
        # TODO: handle errors
        params - notes - list - list of notes to save
        returns - boolean - success or not
        """
        for item in notes:
            response = self.table_connector.put_item(Item=item)
        return True
