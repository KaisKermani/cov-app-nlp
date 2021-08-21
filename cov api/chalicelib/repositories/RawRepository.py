from datetime import datetime
from typing import List

from chalicelib.daos.RawDao import RawDao
from chalicelib.entities.Raw import Raw


class RawRepository:
    def __init__(self, raw_dao: RawDao):
        self.raw_dao = raw_dao

    def get_all(self) -> List[Raw]:
        return [Raw(**item) for item in self.raw_dao.get_all()]

    def get_one(self, post_id) -> Raw:
        return Raw(**self.raw_dao.get_by_id(post_id))

    def put(self, raw: Raw):
        item = raw.dict()
        item["post_time"] = int(datetime.timestamp(item["post_time"]))
        item["extract_time"] = int(datetime.timestamp(item["extract_time"]))
        item["PK"] = raw.id
        item["SK"] = "raw"
        return self.raw_dao.upsert(item)
