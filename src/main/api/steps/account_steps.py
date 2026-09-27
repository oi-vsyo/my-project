from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class AccountSteps(BaseSteps):
    def deposit_account(self, login_user_request: LoginUserRequest, deposit_account_request: DepositAccountRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=login_user_request.username, password=login_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(deposit_account_request)
        return response

    def deposit_account_failed(self, login_user_request: LoginUserRequest, deposit_account_request: DepositAccountRequest, response_specs):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=login_user_request.username, password=login_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            response_specs
        ).post(deposit_account_request)
        return response


    def transactions_account(self, login_user_request: LoginUserRequest, id_account: int):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=login_user_request.username, password=login_user_request.password),
            Endpoint.TRANSACTIONS_ACCOUNT,
            ResponseSpecs.request_ok()
        ).get(id_account)
        return response

    def transfer_account(self, login_user_request: LoginUserRequest, transfer_account_request: TransferAccountRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=login_user_request.username, password=login_user_request.password),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_ok()
        ).post(transfer_account_request)
        return response

    def transfer_account_failed(self, login_user_request: LoginUserRequest, transfer_account_request: TransferAccountRequest, response_specs):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=login_user_request.username, password=login_user_request.password),
            Endpoint.TRANSFER_ACCOUNT,
            response_specs
        ).post(transfer_account_request)
        return response