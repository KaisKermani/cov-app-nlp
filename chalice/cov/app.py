import logging
import os

import boto3
from chalice import Chalice, CORSConfig, IAMAuthorizer, BadRequestError

from chalicelib.factories.HandlerFactory import HandlerFactory, HandlerType
from chalicelib.responses import Responder

app = Chalice(app_name='cov')

cors_config = CORSConfig(
    allow_origin=os.environ['FRONT_URL'],
    allow_headers=['X-Special-Header', 'Access-Control-Allow-Origin'],
    max_age=600,
    expose_headers=['X-Special-Header', 'Access-Control-Allow-Origin'],
    allow_credentials=True
)

app.debug = True

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TURN_OFF_AUTHENTICATION = os.environ.get("TURN_OFF_AUTHENTICATION", "false")

if TURN_OFF_AUTHENTICATION == "true":
    iam_authorizer = None
else:
    iam_authorizer = IAMAuthorizer()

dynamo_resource = boto3.resource("dynamodb")
dynamo_table_name = os.environ.get("TABLE_NAME")

handler_factory = HandlerFactory(dynamo_resource, dynamo_table_name)

@app.route('/raw', methods=['GET'], cors=cors_config, authorizer=iam_authorizer)
def get_all_post_raw():
    post_raw_handler = handler_factory.create_handler(HandlerType.PostRawHandler)

    return post_raw_handler.get_all_raw()


@app.route('/raw/{post_id}', methods=['GET'], cors=cors_config, authorizer=iam_authorizer)
def get_post_raw(post_id):
    post_raw_handler = handler_factory.create_handler(HandlerType.PostRawHandler)

    return post_raw_handler.get_raw(post_id)


@app.route('/structured', methods=['GET'], cors=cors_config, authorizer=iam_authorizer)
def get_all_post_structured():
    post_structured_handler = handler_factory.create_handler(HandlerType.PostStructuredHandler)

    return post_structured_handler.get_all_structured()


@app.route('/structured/{post_id}', methods=['GET'], cors=cors_config, authorizer=iam_authorizer)
def get_post_structured(post_id):
    post_structured_handler = handler_factory.create_handler(HandlerType.PostStructuredHandler)

    return post_structured_handler.get_structured(post_id)


@app.route('/post/{post_id}', methods=['GET'], cors=cors_config, authorizer=iam_authorizer)
def get_post(post_id):
    post_handler = handler_factory.create_handler(HandlerType.PostHandler)

    return post_handler.get_post(post_id)


@app.route('/raw', methods=['POST'], cors=cors_config, authorizer=iam_authorizer)
def put_raw_post():
    post_raw_handler = handler_factory.create_handler(HandlerType.PostRawHandler)

    try:
        json_body = app.current_request.json_body
    except BadRequestError:
        return Responder.error(
            status_code=400,
            error_message="Request body isn't valid json. (%s)" % app.current_request.raw_body
        )
    return post_raw_handler.put_raw(json_body=json_body)


@app.route('/structured', methods=['POST'], cors=cors_config, authorizer=iam_authorizer)
def put_structured_post():
    post_structured_handler = handler_factory.create_handler(HandlerType.PostStructuredHandler)

    try:
        json_body = app.current_request.json_body
    except BadRequestError:
        return Responder.error(
            status_code=400,
            error_message="Request body isn't valid json. (%s)" % app.current_request.raw_body
        )
    return post_structured_handler.put_structured(json_body=json_body)
