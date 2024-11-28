from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from services.ReceiptService import ReceiptService
from services.DTO.ReceiptInput import ReceiptCreate

router = APIRouter()

@router.post("/receipts/process")
def create_receipt(receipt: ReceiptCreate):
    try:
        receipt_id = ReceiptService.create_receipt(receipt)
        return {"id": receipt_id}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())

@router.get("/receipts/{id}/points")
def get_receipt_points(id: str):
    points = ReceiptService.get_receipt_points(id)
    return {"points": points}
