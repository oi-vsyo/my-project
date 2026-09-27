from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.receipt_credit_request import ReceiptCreditRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class CreditSteps(BaseSteps):
    def receipt_credit(self, login_credit_user_request: LoginUserRequest, receipt_credit_request: ReceiptCreditRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=login_credit_user_request.username, password=login_credit_user_request.password),
            Endpoint.RECEIPT_CREDIT,
            ResponseSpecs.request_created()
        ).post(receipt_credit_request)
        return response

    def receipt_credit_failed(self, login_credit_user_request: LoginUserRequest, receipt_credit_request: ReceiptCreditRequest, response_specs):
        response = CrudRequester(
            RequestSpecs.auth_headers(username=login_credit_user_request.username, password=login_credit_user_request.password),
            Endpoint.RECEIPT_CREDIT,
            response_specs
        ).post(receipt_credit_request)
        return response