from math import ceil
import uuid
from datetime import date, time
from fastapi import HTTPException
from typing import List
from entities.Receipt import Receipt
from entities.Item import Item
from db.db import receipts_db
from fastapi import APIRouter
from pydantic import BaseModel, ValidationError

router = APIRouter()


class ReceiptCreate(BaseModel):
    retailer: str
    purchaseDate: date
    purchaseTime: time
    total: float
    items: List[Item]

@router.post("/receipts/process")
def create_receipt(receipt: ReceiptCreate):
    try:
        receipt_obj = Receipt(
            id = str(uuid.uuid4()),
            retailer=receipt.retailer,
            purchaseDate=receipt.purchaseDate,
            purchaseTime=receipt.purchaseTime,
            total=receipt.total,
            items=receipt.items
        )
        receipts_db[receipt_obj.id] = receipt_obj
        return {"id": receipt_obj.id}
    except ValidationError as e:
        errors = [{"loc": err["loc"], "msg": err["msg"], "type": err["type"]} for err in e.errors()]
        raise HTTPException(status_code=422, detail=errors)

@router.get("/receipts/{id}/points")
def get_receipt_points(id: str):
    receipt = receipts_db.get(id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    
    return {"points": calculate_points(receipt)}

def calculate_points(receipt: Receipt):
    points = 0

    # Rule 1: One point for every alphanumeric character in the retailer name.
    rule1 = sum(c.isalnum() for c in receipt.retailer)
    points+=rule1

    # Rule 2: 50 points if the total is a round dollar amount with no cents.
    rule2 = 0
    if receipt.total.is_integer():
        rule2 += 50
    points+=rule2
    
    # Rule 3: 25 points if the total is a multiple of 0.25.
    rule3 = 0
    if receipt.total % 0.25 == 0:
        rule3 += 25
    points+=rule3

    # Rule 4: 5 points for every two items on the receipt.
    rule4 = (len(receipt.items) // 2) * 5
    points+=rule4

    # Rule 5: Points for items with description length multiple of 3.
    rule5 = 0
    for item in receipt.items:
        if len(item.shortDescription.strip()) % 3 == 0:
            rule5 += ceil(item.price * 0.2)

    points+=rule5

    # Rule 6: 6 points if the day in the purchase date is odd.
    rule6 = 0
    if receipt.purchaseDate.day % 2 != 0:
        rule6 = 6
    points+=rule6
    
    # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    rule7 = 0
    purchase_time = time(receipt.purchaseTime.hour, receipt.purchaseTime.minute)
    if time(14, 0) < purchase_time < time(16, 0):
        rule7 = 10

    points+=rule7
    return points