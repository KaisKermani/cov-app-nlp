from pydantic import BaseModel, Field

from entities.Raw import Raw
from entities.Structured import Structured


class Post(BaseModel):
    id: str
    raw: Raw = Field(...)
    structured: Structured = Field(...)

