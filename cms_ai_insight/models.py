from typing import Optional

from pydantic import BaseModel

class BuzzRequest(BaseModel):
    indexes: list[str]
    labels: list[str]
    published_from: str
    published_to: str
    refresh_token: Optional[str] = None
    token: Optional[str] = None