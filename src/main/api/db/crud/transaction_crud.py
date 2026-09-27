from src.main.api.db.models.transaction_table import Transaction
from sqlalchemy.orm import Session


class TransactionCrudDb:
    @staticmethod
    def get_transaction(db: Session, from_account_id: int, to_account_id: int, amount: float) -> Transaction | None:
        return db.query(Transaction).filter_by(from_account_id=from_account_id, to_account_id=to_account_id, amount=amount).first()
