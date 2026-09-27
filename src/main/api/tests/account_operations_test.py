import pytest
from requests import Session

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.specs.response_specs import ResponseSpecs


@pytest.mark.api
class TestAccountOperations:
    def test_create_operations(self, api_manager: ApiManager, create_user_request: CreateUserRequest, login_user_request: LoginUserRequest, db_session: Session):

        response = api_manager.user_steps.create_account(create_user_request)

        assert response.balance == 0
        id_account = response.id

        deposit_data = DepositAccountRequest(accountId=id_account, amount=1957.99)
        api_manager.account_steps.deposit_account(login_user_request, deposit_data)

        response_transactions = api_manager.account_steps.transactions_account(login_user_request, id_account)

        assert response_transactions.balance == 1957.99

        account_from_db = Account.get_account_by_id(db_session, id_account)
        assert account_from_db.id == response_transactions.id, 'Аккаунт не создан, id аккаунта нет в БД'
        assert account_from_db.balance == 1957.99, 'Поле баланса для созданного аккаунта не соответствует ожидаемому'


    @pytest.mark.parametrize(
        "username, password, id_account, amount, response_specs",
        [
            ("admin", "123456", 1, 2500, ResponseSpecs.request_forbidden()),
            ("SuperUser", "Pas!sw0rd", 135, 2500, ResponseSpecs.request_not_found()),
        ]
    )
    def test_create_operations_failed(self, api_manager, login_user_request, username, password, id_account, amount, response_specs):

        user_request = LoginUserRequest(username=username, password=password)
        deposit_data = DepositAccountRequest(accountId=id_account, amount=amount)

        api_manager.account_steps.deposit_account_failed(user_request, deposit_data, response_specs)

