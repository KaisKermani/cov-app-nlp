from pydantic import ValidationError

from chalicelib.entities.Structured import Structured
from chalicelib.repositories.StructuredRepository import StructuredRepository
from chalicelib.responses import Responder


class PostStructuredHandler:
    def __init__(self, structured_repo: StructuredRepository):
        self.structured_repo = structured_repo

    def get_structured(self, post_id):
        return Responder.success(self.structured_repo.get_one(post_id))

    def get_all_structured(self):
        return Responder.success(self.structured_repo.get_all())

    def put_structured(self, json_body):
        try:
            structured = Structured(**json_body)
        except ValidationError as e:
            return Responder.error(
                status_code=400,
                error_message=f"Check structured body format: {str(e)}"
            )
        res = self.structured_repo.put(structured=structured)
        return Responder.success(res)
