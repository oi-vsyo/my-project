from dataclasses import dataclass
from typing import Optional, Type
from src.main.api.models.base_model import BaseModel
from enum import Enum

from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.receipt_credit_request import ReceiptCreditRequest
from src.main.api.models.receipt_credit_response import ReceiptCreditResponse
from src.main.api.models.transactions_account_response import TransactionsAccountResponse
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.models.transfer_account_response import TransferAccountResponse
from src.main.api.requests.create_account_requester import CreateAccountRequester


@dataclass
class EndpointCongiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]

class Endpoint(Enum):
    CREATE_ACCOUNT = EndpointCongiguration(
        request_model= CreateAccountRequester,
        url = "api/account/create",
        response_model= CreateAccountResponse,
    )

    ADMIN_CREATE_USER = EndpointCongiguration(
        request_model= CreateUserRequest,
        url = "api/admin/create",
        response_model= CreateUserResponse,
    )

    LOGIN_USER = EndpointCongiguration(
        request_model=LoginUserRequest,
        url="/auth/token/login",
        response_model=LoginUserResponse
    )

    DEPOSIT_ACCOUNT = EndpointCongiguration(
        request_model= DepositAccountRequest,
        url = "api/account/deposit",
        response_model= DepositAccountResponse,
    )

    RECEIPT_CREDIT = EndpointCongiguration(
        request_model= ReceiptCreditRequest,
        url = "api/credit/request",
        response_model= ReceiptCreditResponse,
    )

    TRANSACTIONS_ACCOUNT = EndpointCongiguration(
        request_model= None,
        url = "api/account/transactions",
        response_model= TransactionsAccountResponse,
    )

    ADMIN_DELETE_USER = EndpointCongiguration(
        request_model=None,
        url="api/admin/users",
        response_model=None
    )

    TRANSFER_ACCOUNT = EndpointCongiguration(
        request_model=TransferAccountRequest,
        url="api/account/transfer",
        response_model=TransferAccountResponse,
    )
