from datetime import date, time
from typing import List
from entities.Item import Item
from pydantic import BaseModel

class ReceiptCreate(BaseModel):
    retailer: str
    purchaseDate: date
    purchaseTime: time
    total: float
    items: List[Item]