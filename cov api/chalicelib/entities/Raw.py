from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Raw(BaseModel):
    id: str
    post_text: Optional[str]
    author: Optional[str]
    author_profile: Optional[str]
    post_time: Optional[datetime]
    extract_time: Optional[datetime]
    post_link: Optional[str]
    post_group: Optional[str]


