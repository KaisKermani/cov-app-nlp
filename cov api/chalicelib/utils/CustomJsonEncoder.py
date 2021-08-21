import json
import datetime
from decimal import Decimal

from pydantic import BaseModel


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)

        if isinstance(obj, BaseModel):
            return obj.dict()

        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.strftime("%Y-%m-%d %H:%M:%S")

        return super(CustomJsonEncoder, self).default(obj)
