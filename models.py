from datetime import datetime
from pydantic import BaseModel  # pydantics for structuring our data.
from typing import List


class Stock(BaseModel):
    symbol: str
    date: datetime
    price_open: float
    price_high: float
    price_low: float
    price_close: float
    price_adj_close: float
    volume: float


class Stocks(BaseModel):
    history: List[Stock]
