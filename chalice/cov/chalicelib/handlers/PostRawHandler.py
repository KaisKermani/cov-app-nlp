from pydantic import ValidationError

from entities.Raw import Raw
from repositories.RawRepository import RawRepository
from responses import Responder


class PostRawHandler:
    def __init__(self, raw_repo: RawRepository):
        self.raw_repo = raw_repo

    def get_all_raw(self):
        return Responder.success(self.raw_repo.get_all())

    def get_raw(self, post_id: str):
        return Responder.success(self.raw_repo.get_one(post_id))

    def put_raw(self, json_body):
        try:
            raw = Raw(**json_body)
        except ValidationError as e:
            return Responder.error(
                status_code=400,
                error_message=f"Check raw body format: {str(e)}"
            )
        res = self.raw_repo.put(raw=raw)
        return Responder.success(res)
