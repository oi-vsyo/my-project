from http import HTTPStatus
import requests
from src.main.api.models.transactions_account_response import TransactionsAccountResponse
from src.main.api.requests.requester import Requester


class TransactionsAccountRequester(Requester):
    def get(self, user_id: int):
        url=f'{self.base_url}api/account/transactions/{user_id}'
        response=requests.get(
            url=url,
            headers=self.headers,
        )

        self.response_spec(response)
        if response.status_code in [HTTPStatus.OK]:
            return TransactionsAccountResponse(**response.json())
        return response