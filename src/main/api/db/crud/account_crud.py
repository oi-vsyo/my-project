from src.main.api.db.models.account_table import Account
from sqlalchemy.orm import Session


class AccountCrudDb:
    @staticmethod
    def get_account_by_id(db: Session, account_id: int) -> Account | None:
        return db.query(Account).filter_by(id=account_id).first()

    @staticmethod
    def get_accounts_by_user_id(db: Session, user_id: int):
        return db.query(Account).filter_by(user_id=user_id).all()
