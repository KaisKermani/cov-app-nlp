from chalicelib.daos.PostDao import PostDao
from chalicelib.entities.Post import Post
from chalicelib.entities.Raw import Raw
from chalicelib.entities.Structured import Structured


class PostRepository:
    def __init__(self, post_dao: PostDao):
        self.post_dao = post_dao

    def get_one(self, post_id) -> Post:
        dao_res = self.post_dao.get_by_id(post_id)
        raw = Raw(**dao_res)
        structured = Structured(**dao_res)
        return Post(**dao_res, raw=raw, structured=structured)