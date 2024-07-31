from typing import List, Optional

from pydantic import BaseModel

class Sentiment(BaseModel):
    label: str
    value: int

class ChartValue(BaseModel):
    datetime: str
    total_mention: int
    sentiment: List[Sentiment]

class MentionRange(BaseModel):
    range_new: Optional[str] = None
    range_old: Optional[str] = None
    value: int

class Analysis(BaseModel):
    mentions: List[MentionRange]
    chart_values: List[ChartValue]

class InputData(BaseModel):
    data: List[dict]
    analysis: Analysis