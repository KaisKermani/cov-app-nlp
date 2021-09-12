import logging
import os

import requests
from urllib.parse import urlparse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# from urlparse import urlparse  # Python 2
parsed_uri = urlparse(os.environ.get("COV_API_URL"))
host = '{uri.netloc}'.format(uri=parsed_uri)

class CovApiError(Exception):
    pass

class CovApi:
    #TODO: Insert into database and get from database
    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint
    def get_facebook_groups(self):
        return ["1493465070746580"]

    def insert_posts(self, posts, fb_group):

        # Inserting new posts in database:
        for row in posts:
            logger.info((
                row['id'], row['text'], row['Author'], row['Author_profile'], row['Post_time'], row['Extract_time'],
                row['Post_link'], fb_group))
            raw = {
                'id': row['id']
            }
            try:
                self.insert_raw(raw)
            except CovApiError:


    def insert_raw(self, raw):

        from aws_requests_auth.boto_utils import BotoAWSRequestsAuth
        auth = BotoAWSRequestsAuth(aws_host=host,
                                   aws_region='eu-west-1',
                                   aws_service='execute-api')
        structured_endpoint = f"{self.api_endpoint}/raw"
        # Inserting new structured entry in db
        logger.info(f"Inserting {raw} to {structured_endpoint}")
        res = requests.post(structured_endpoint, json=raw, auth=auth)
        if res.status_code == 200:
            logger.info("Successfully inserted row to Cov API")
            logger.info(res.text)
        else:
            logger.info(f"Couldn't insert row to Cov API, {res.text}")
            raise CovApiError(res.text)