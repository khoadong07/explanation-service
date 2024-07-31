from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class Sentiment(BaseModel):
    negative: Optional[int]
    positive: Optional[int]
    neutral: Optional[int]


class ChannelDistribution(BaseModel):
    channel: str
    count_mentions: int
    percent: float
    sentiment: Sentiment


class Data(BaseModel):
    range_date: str
    total_mentions: int


class ChannelDistributionData(BaseModel):
    data: Data
    channel_distribution: List[ChannelDistribution]