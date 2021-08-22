import logging
import os

import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

from urllib.parse import urlparse

# from urlparse import urlparse  # Python 2
parsed_uri = urlparse(os.environ.get("COV_API_URL"))
host = '{uri.netloc}'.format(uri=parsed_uri)


class CovApiError(Exception):
    pass


class CovApi:
    def __init__(self, api_endpoint: str):
        self.api_endpoint = api_endpoint

    def insert_structured(self, structured):

        from aws_requests_auth.boto_utils import BotoAWSRequestsAuth
        auth = BotoAWSRequestsAuth(aws_host=host,
                                   aws_region='eu-west-1',
                                   aws_service='execute-api')
        structured_endpoint = f"{self.api_endpoint}/structured"
        # Inserting new structured entry in db
        logger.info(f"Inserting {structured} to {structured_endpoint}")
        res = requests.post(structured_endpoint, json=structured, auth=auth)
        if res.status_code == 200:
            logger.info("Successfully inserted row to Cov API")
            logger.info(res.text)
        else:
            logger.info(f"Couldn't insert row to Cov API, {res.text}")
            raise CovApiError(res.text)
