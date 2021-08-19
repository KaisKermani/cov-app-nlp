from typing import List

from chalicelib.daos.StructuredDao import StructuredDao
from chalicelib.entities.Structured import Structured


class StructuredRepository:
    def __init__(self, structured_dao: StructuredDao):
        self.structured_dao = structured_dao

    def get_all(self) -> List[Structured]:
        return [Structured(**item) for item in self.structured_dao.get_all()]

    def get_one(self, post_id) -> Structured:
        return Structured(**self.structured_dao.get_by_id(post_id))

    def put(self, structured: Structured):
        item = structured.dict()
        item["PK"] = structured.id
        item["SK"] = "structured"
        return self.structured_dao.upsert(item)

