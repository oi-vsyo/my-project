from src.main.api.models.base_model import BaseModel


class ReceiptCreditRequest(BaseModel):
    accountId: int
    amount: float
    termMonths: int