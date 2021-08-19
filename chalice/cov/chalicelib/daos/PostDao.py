import logging

from typing import List, Dict

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class PostDao:
    def __init__(self, dynamo_resource, table_name: str):
        self.dynamo_resource = dynamo_resource
        self.table_name = table_name

    def get_by_id(self, post_id: str) -> Dict[str, str]:
        """Gets a post item from DynamoDB by ID and returns it"""
        table = self.dynamo_resource.Table(self.table_name)
        try:
            response = table.query(
                KeyConditionExpression=Key('PK').eq(post_id)
            )
            items = response.get('Items', [])
            if not len(items):
                return {}
            return items[0]
        except ClientError as e:
            logger.exception(
                "Unable to access table %s in dynamo. %s" % (
                    self.table_name, e.response.get('Error', {}).get('Message')
                )
            )
            raise ValueError("Unable to access table %s in dynamo" % self.table_name)
