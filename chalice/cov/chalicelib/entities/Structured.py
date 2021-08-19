from typing import Optional

from pydantic import BaseModel


class Structured(BaseModel):
    id: str
    loc_from: Optional[str]
    loc_to: Optional[str]
    n_seats: Optional[str]
    cov_day: Optional[str]
    cov_time: Optional[str]
    phone: Optional[str]
    cost: Optional[str]
    category: Optional[str]
