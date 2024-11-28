from typing import Dict
from entities.Receipt import Receipt

# This will act as our in-memory database
receipts_db: Dict[str, Receipt] = {}
