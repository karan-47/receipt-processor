from pydantic import BaseModel, validator
from datetime import date, time
from typing import List

from models.Item import Item


class Receipt(BaseModel):
    id: str
    retailer: str
    purchaseDate: date
    purchaseTime: time
    items: List[Item]
    total: float
    

    @validator('total')
    def total_must_be_sum_of_items(cls, v, values):
        items = values.get('items', [])
        calculated_total = sum(item.price for item in items)

       

        # Get the number of decimal places in v
        decimals = 0
        if '.' in str(v):
            decimals = len(str(v).split('.')[1])

        # Round the calculated total to the same number of decimal places as v
        rounded_calculated_total = round(calculated_total, decimals)

        

        if v != rounded_calculated_total:
            raise ValueError('total must be the sum of all item prices')
        return v