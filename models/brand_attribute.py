from pydantic import BaseModel
from typing import List


class Sentiment(BaseModel):
    negative: float
    neutral: float
    positive: float


class BrandAttribute(BaseModel):
    attribute: str
    total_mentions: int
    sentiment: Sentiment


class BrandAttributeData(BaseModel):
    data: List[BrandAttribute]