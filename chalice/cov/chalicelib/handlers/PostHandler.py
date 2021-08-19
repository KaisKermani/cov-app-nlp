from pydantic import ValidationError

from entities.Raw import Raw
from repositories.PostRespository import PostRepository
from repositories.RawRepository import RawRepository
from responses import Responder


class PostHandler:
    def __init__(self, post_repo: PostRepository):
        self.post_repo = post_repo

    def get_post(self, post_id: str):
        return Responder.success(self.post_repo.get_one(post_id))
