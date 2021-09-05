from typing import List
import boto3
import os
from boto3.dynamodb.conditions import Key

DB_ENDPOINT = os.environ.get("DB_ENDPOINT")

class DAOBase(object):
    """
    Basic functionality of dynamoDB DAO
    """

    def __init__(self, table_name, key_name) -> None:
        """
        params - table_name - string - dynamodb table name
        params - key_name - string - dynamodb table primary key
        """
        if not DB_ENDPOINT: 
            self.client = boto3.resource("dynamodb")
        else: 
            self.client = boto3.resource("dynamodb", endpoint_url=DB_ENDPOINT)
        self.table_name = table_name
        self.table_connector = self.client.Table(self.table_name)
        self.primary_key = key_name
    
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
