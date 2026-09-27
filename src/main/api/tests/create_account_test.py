import pytest
from requests import Session

from src.main.api.db.crud.user_crud import UserCrudDb as User
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


@pytest.mark.api
class TestCreateAccount:
    def test_create_account_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, login_user_request: LoginUserRequest, db_session: Session):

        response = api_manager.user_steps.create_account(create_user_request)
        assert response.balance == 0

        id_account = response.id
        deposit_data = DepositAccountRequest(accountId=id_account, amount=1957.99)
        api_manager.account_steps.deposit_account(login_user_request, deposit_data)

        transfer_data = TransferAccountRequest(fromAccountId=id_account, toAccountId=135, amount=500.90)
        response_transfer = api_manager.account_steps.transfer_account(login_user_request, transfer_data)

        assert round(response_transfer.fromAccountIdBalance, 2) == 1457.09

        account_from_db = Account.get_account_by_id(db_session, id_account)
        assert account_from_db.id == response_transfer.fromAccountId, 'Аккаунт не создан, id аккаунта нет в БД'
        assert account_from_db.balance == 1457.09, 'Поле баланса после проведенных операций не соответствует ожиданию'


    @pytest.mark.parametrize(
        "username,password,response_specs",
        [
            ("Vika", "Pas!sw0rd", ResponseSpecs.request_conflict()),
            ("admin", "123456", ResponseSpecs.request_forbidden())
        ]
    )
    def test_create_account_invalid(self, api_manager: ApiManager, username, password, response_specs, db_session: Session):

        create_user_request = LoginUserRequest(username=username, password=password)
        user = User.get_user_by_username(db_session, username)
        account_before = Account.get_accounts_by_user_id(db_session, user.id)

        api_manager.user_steps.create_account_failed(create_user_request, response_specs)

        account_after = Account.get_accounts_by_user_id(db_session, user.id)

        assert len(account_before) == len(account_after), "У пользователя был создан новый аккаунт"

    @pytest.mark.parametrize(
        "toAccountId,amount,response_specs, transaction_created",
        [
            (7, 500, ResponseSpecs.request_not_found(), False),
            (135, 499.99, ResponseSpecs.request_bad(),False),
            (140, 500, ResponseSpecs.request_ok(), True),
            (128, 9999.99, ResponseSpecs.request_ok(), True),
            (135, 10000, ResponseSpecs.request_ok(), True),
            (141, 10001, ResponseSpecs.request_bad(), False),
            (155, 18000, ResponseSpecs.request_bad(), False),
        ]
        )
    def test_transfer_account_invalid(self, api_manager: ApiManager, login_user_request: LoginUserRequest, account_with_balance_request, toAccountId, amount, response_specs, transaction_created, db_session: Session):

        transfer_data = TransferAccountRequest(fromAccountId=account_with_balance_request, toAccountId=toAccountId, amount=amount)
        api_manager.account_steps.transfer_account_failed(login_user_request, transfer_data, response_specs)

        transfer_from_db = Transaction.get_transaction(db_session, from_account_id=account_with_balance_request, to_account_id=toAccountId, amount=amount)

        if transaction_created:
            assert transfer_from_db is not None, "Транзакция не создана в БД"
        else:
            assert transfer_from_db is None, "Транзакция ошибочно создана в БД"


