from pydantic import BaseModel
from typing import List


class SentimentBreakdown(BaseModel):
    label: str
    value: int


class DataSummary(BaseModel):
    range_date: str
    total_mentions: int


class AnalysisResult(BaseModel):
    data: DataSummary
    sentiment_breakdown: List[SentimentBreakdown]