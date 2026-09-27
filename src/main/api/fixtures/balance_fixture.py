import pytest
from src.main.api.models.deposit_account_request import DepositAccountRequest


@pytest.fixture
def account_with_balance_request(api_manager, create_user_request, login_user_request):
    response = api_manager.user_steps.create_account(create_user_request)
    id_account = response.id
    deposit_data = DepositAccountRequest(accountId=id_account, amount=9000)
    api_manager.account_steps.deposit_account(login_user_request, deposit_data)
    api_manager.account_steps.deposit_account(login_user_request, deposit_data)
    return id_account
