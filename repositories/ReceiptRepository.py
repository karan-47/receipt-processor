from db.db import receipts_db
from entities.Receipt import Receipt
from typing import Optional


class ReceiptRepository:
    @staticmethod
    def save(receipt: Receipt) -> None:
        receipts_db[receipt.id] = receipt

    @staticmethod
    def get_by_id(receipt_id: str) -> Optional[Receipt]:
        return receipts_db.get(receipt_id)
