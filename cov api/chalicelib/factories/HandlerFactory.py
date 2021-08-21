from enum import auto, Enum

from chalicelib.daos.PostDao import PostDao
from chalicelib.daos.RawDao import RawDao
from chalicelib.daos.StructuredDao import StructuredDao
from chalicelib.handlers.PostHandler import PostHandler
from chalicelib.handlers.PostRawHandler import PostRawHandler
from chalicelib.handlers.PostStructuredHandler import PostStructuredHandler
from chalicelib.repositories.PostRespository import PostRepository
from chalicelib.repositories.RawRepository import RawRepository
from chalicelib.repositories.StructuredRepository import StructuredRepository


class HandlerType(Enum):
    PostHandler = auto()
    PostRawHandler = auto()
    PostStructuredHandler = auto()

class HandlerFactory:
    def __init__(self, dynamo_resource, dynamo_table_name: str):
        self.dynamo_resource = dynamo_resource
        self.dynamo_table_name = dynamo_table_name

    def create_handler(self, handler):
        if handler == HandlerType.PostRawHandler:
            raw_dao = RawDao(self.dynamo_resource, self.dynamo_table_name)
            raw_repo = RawRepository(raw_dao)
            return PostRawHandler(raw_repo=raw_repo)
        elif handler == HandlerType.PostHandler:
            post_dao = PostDao(self.dynamo_resource, self.dynamo_table_name)
            post_repo = PostRepository(post_dao)
            return PostHandler(post_repo)
        elif handler == HandlerType.PostStructuredHandler:
            structured_dao = StructuredDao(self.dynamo_resource, self.dynamo_table_name)
            structured_repo = StructuredRepository(structured_dao)
            return PostStructuredHandler(structured_repo=structured_repo)
        else:
            raise ValueError(f"Unknown handler type: {handler}")