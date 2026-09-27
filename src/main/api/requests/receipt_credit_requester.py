from http import HTTPStatus
from requests import Response
from src.main.api.models.receipt_credit_request import ReceiptCreditRequest
from src.main.api.models.receipt_credit_response import ReceiptCreditResponse
from src.main.api.requests.requester import Requester
import requests


class ReceiptCreditRequester(Requester):
    def post(self, receipt_credit_request: ReceiptCreditRequest) -> ReceiptCreditResponse | Response:
        url=f"{self.base_url}api/credit/request"
        response=requests.post(
            url=url,
            json=receipt_credit_request.model_dump(),
            headers=self.headers
        )

        self.response_spec(response)
        if response.status_code in [HTTPStatus.CREATED]:
            return ReceiptCreditResponse(**response.json())
        return response