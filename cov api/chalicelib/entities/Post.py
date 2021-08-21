from pydantic import BaseModel, Field

from chalicelib.entities.Raw import Raw
from chalicelib.entities.Structured import Structured


class Post(BaseModel):
    id: str
    raw: Raw = Field(...)
    structured: Structured = Field(...)

