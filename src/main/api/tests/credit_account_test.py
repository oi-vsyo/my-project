import pytest
from requests import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.api_fixture import api_manager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.receipt_credit_request import ReceiptCreditRequest
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit




@pytest.mark.api
class TestCreditAccount:
    def test_account_credit_pass(self, db_session: Session, api_manager: ApiManager, create_credit_user_request: CreateUserRequest, login_credit_user_request: LoginUserRequest):

        response = api_manager.user_steps.create_account(create_credit_user_request)

        assert response.balance == 0
        id_account = response.id

        credit_data = ReceiptCreditRequest(accountId=id_account, amount=5000, termMonths=12)
        response_credit = api_manager.credit_steps.receipt_credit(login_credit_user_request, credit_data)

        credit_from_db = Credit.get_credit_by_id(db_session, response_credit.creditId)

        assert credit_from_db.id == response_credit.creditId, 'Кредит клиенту не выдан'
        assert credit_from_db.amount == 5000, 'Сумма выданного кредита не соответствует ожидаемой'



    @pytest.mark.parametrize(
        "username, password, role, amount, response_specs, account_offset",
        [
            ("Masha1", "Pas!sw0rd", "ROLE_USER", 5000, ResponseSpecs.request_forbidden(), 0),
            ("Masha2", "Pas!sw0rd", "ROLE_CREDIT_SECRET", 5000, ResponseSpecs.request_not_found(), 1),
            ("Masha3", "Pas!sw0rd", "ROLE_CREDIT_SECRET", 15001, ResponseSpecs.request_bad(), 0),
        ]
    )
    def test_account_credit_failed(self, username, password, role, amount, response_specs, account_offset, api_manager: ApiManager, db_session: Session):

        create_user_request = CreateUserRequest(username=username, password=password, role=role)
        api_manager.admin_steps.create_user(create_user_request)

        response = api_manager.user_steps.create_account(create_user_request)
        assert response.balance == 0
        id_account = response.id + account_offset

        login_user_request = LoginUserRequest(username=username, password=password)
        credit_data = ReceiptCreditRequest(accountId=id_account, amount=amount, termMonths=12)
        api_manager.credit_steps.receipt_credit_failed(login_user_request, credit_data, response_specs)

        credit_from_db = Credit.get_credit_by_id_account(db_session, id_account)

        assert credit_from_db is None, 'Кредит выдан клиенту'


