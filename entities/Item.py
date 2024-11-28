from pydantic import BaseModel, validator

class Item(BaseModel):
    shortDescription: str
    price: float

    @validator('price')
    def price_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError('price must be greater than or equal to 0')
        return v