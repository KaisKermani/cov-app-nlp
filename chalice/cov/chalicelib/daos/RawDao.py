import logging

from typing import List, Dict

from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class RawDao:
    def __init__(self, dynamo_resource, table_name: str):
        self.dynamo_resource = dynamo_resource
        self.table_name = table_name

    def get_all(self) -> List[Dict[str, str]]:
        """Gets all raw items from DynamoDB by ID and returns them"""
        table = self.dynamo_resource.Table(self.table_name)
        try:
            response = table.query(
                IndexName="SK-index",
                KeyConditionExpression=Key('SK').eq('raw')
            )
        except ClientError as e:
            logger.exception(
                "Unable to access table %s in dynamo. %s" % (
                    self.table_name, e.response.get('Error', {}).get('Message')
                )
            )
            raise ValueError("Unable to access table %s in dynamo" % self.table_name)
        else:
            items = response.get('Items', [])
            logger.info(f"Fetched {len(items)} 'raw' items from database")

            while response.get("LastEvaluatedKey") is not None:
                response = table.query(
                    IndexName="SK-index",
                    KeyConditionExpression=Key('SK').eq('raw'),
                    ExclusiveStartKey=response.get("LastEvaluatedKey")
                )
                items += response.get('Items', [])
            return items

    def get_by_id(self, raw_id: str) -> Dict[str, str]:
        """Gets a raw item from DynamoDB by ID and returns it"""
        table = self.dynamo_resource.Table(self.table_name)
        try:
            response = table.query(
                KeyConditionExpression=Key('PK').eq(raw_id) & Key("SK").eq("raw")
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

    def upsert(self, item: Dict[str, str]):
        """Puts a raw item into the database"""
        table = self.dynamo_resource.Table(self.table_name)
        try:
            return table.put_item(
                Item=item
            )
        except ClientError as e:
            logger.exception(
                "Unable to access table %s in dynamo. %s" % (
                    self.table_name, e.response.get('Error', {}).get('Message')
                )
            )
            raise ValueError("Unable to access table %s in dynamo" % self.table_name)
