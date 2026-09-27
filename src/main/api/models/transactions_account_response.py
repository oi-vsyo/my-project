from datetime import datetime
from src.main.api.models.base_model import BaseModel
from typing import List, Optional

class Transaction(BaseModel):
    transactionId: int
    type: str
    amount: float
    fromAccountId: Optional[int] = None
    toAccountId: Optional[int] = None
    createdAt: datetime
    creditId: Optional[int] = None

class TransactionsAccountResponse(BaseModel):
    id: int
    number: str
    balance: float
    transactions: list[Transaction]