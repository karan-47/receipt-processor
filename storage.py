from typing import Dict
from models.Receipt import Receipt

# This will act as our in-memory database
receipts_db: Dict[str, Receipt] = {}
