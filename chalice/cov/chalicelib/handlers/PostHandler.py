from chalicelib.entities.Raw import Raw
from chalicelib.repositories.PostRespository import PostRepository
from chalicelib.repositories.RawRepository import RawRepository
from chalicelib.responses import Responder


class PostHandler:
    def __init__(self, post_repo: PostRepository):
        self.post_repo = post_repo

    def get_post(self, post_id: str):
        return Responder.success(self.post_repo.get_one(post_id))
