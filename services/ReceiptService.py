from hashlib import sha256
from math import ceil
from datetime import time
from fastapi import HTTPException
from entities.Receipt import Receipt
from repositories.ReceiptRepository import ReceiptRepository
from services.DTO import ReceiptInput


class ReceiptService:
    @staticmethod
    def hash_receipt(receipt: ReceiptInput) -> str:
        """
        Generates a unique hash for the receipt based on its content.
        """
        hash_input = f"{receipt.retailer}{receipt.purchaseDate}{receipt.purchaseTime}{receipt.total}{[item.dict() for item in receipt.items]}"
        return sha256(hash_input.encode()).hexdigest()

    @staticmethod
    def create_receipt(receipt_data: ReceiptInput) -> str:
        """
        Processes a receipt, calculates points, and stores it if new.
        """
        # Generate hash ID for the receipt
        receipt_id = ReceiptService.hash_receipt(receipt_data)

        # Check if receipt already exists
        existing_receipt = ReceiptRepository.get_by_id(receipt_id)
        if existing_receipt:
            return receipt_id

        # Calculate points for the new receipt
        points = ReceiptService.calculate_points(receipt_data)

        # Create a Receipt object
        receipt_obj = Receipt(
            id=receipt_id,
            retailer=receipt_data.retailer,
            purchaseDate=receipt_data.purchaseDate,
            purchaseTime=receipt_data.purchaseTime,
            total=receipt_data.total,
            items=receipt_data.items,
            points=points,
        )

        # Save the receipt to the repository
        ReceiptRepository.save(receipt_obj)

        return receipt_id

    @staticmethod
    def get_receipt_points(receipt_id: str) -> int:
        """
        Retrieves points for a given receipt by ID.
        """
        receipt = ReceiptRepository.get_by_id(receipt_id)
        if not receipt:
            raise HTTPException(status_code=404, detail="Receipt not found")
        return receipt.points

    @staticmethod
    def calculate_points(receipt: ReceiptInput) -> int:
        """
        Calculates points based on receipt rules.
        """
        points = 0

        # Rule 1: One point for every alphanumeric character in the retailer name.
        points += sum(c.isalnum() for c in receipt.retailer)

        # Rule 2: 50 points if the total is a round dollar amount with no cents.
        if receipt.total.is_integer():
            points += 50

        # Rule 3: 25 points if the total is a multiple of 0.25.
        if receipt.total % 0.25 == 0:
            points += 25

        # Rule 4: 5 points for every two items on the receipt.
        points += (len(receipt.items) // 2) * 5

        # Rule 5: Points for items with description length multiple of 3.
        points += sum(
            ceil(item.price * 0.2)
            for item in receipt.items
            if len(item.shortDescription.strip()) % 3 == 0
        )

        # Rule 6: 6 points if the day in the purchase date is odd.
        if receipt.purchaseDate.day % 2 != 0:
            points += 6

        # Rule 7: 10 points if the purchase time is between 2:00 PM and 4:00 PM.
        purchase_time = time(receipt.purchaseTime.hour, receipt.purchaseTime.minute)
        if time(14, 0) < purchase_time < time(16, 0):
            points += 10

        return points
