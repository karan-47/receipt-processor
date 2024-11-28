from pydantic import BaseModel, validator, ValidationError
from datetime import date, time
from typing import List
from entities.Item import Item


class Receipt(BaseModel):
    id: str
    retailer: str
    purchaseDate: date
    purchaseTime: time
    items: List[Item]
    total: float
    points: int

    @validator('total')
    def total_must_be_sum_of_items(cls, v, values):
        items = values.get('items', [])
        if not items:
            raise ValueError('Receipt must have at least one item.')

        calculated_total = sum(item.price for item in items)

        # Handle decimal rounding consistency
        decimals = 0
        if isinstance(v, float) and '.' in str(v):
            decimals = len(str(v).split('.')[1])
        rounded_calculated_total = round(calculated_total, decimals)

        if v != rounded_calculated_total:
            raise ValueError(
                f'Total must be the sum of all item prices. Expected: {rounded_calculated_total}, Got: {v}'
            )
        return v
