import boto3
import os


class S3Dao(object):
    """
    Provide a wrapper around the DynamoDB API to fetch Notes from the given table
    """

    def __init__(self) -> None:
        self.client = boto3.resource('s3')

    def get_kindle_file(self, bucket_name: str, object_key:str):
        """
        Return all Note objects corresponding to the given 'upload_uri'
        """
        obj = self.client.Object(bucket_name,object_key)
        print("obj ", obj)
        body = obj.get()['Body'].read().decode("utf-8")
        print("Decoded Body")
        return body
