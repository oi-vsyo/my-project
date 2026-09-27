import pytest

from src.main.api.fixtures.user_fixture import create_user_request
from src.main.api.fixtures.user_fixture import create_credit_user_request
from src.main.api.models.login_user_request import LoginUserRequest


@pytest.fixture
def login_user_request(create_user_request):
    login_user_request = LoginUserRequest(username=create_user_request.username, password=create_user_request.password)
    return login_user_request

@pytest.fixture
def login_credit_user_request(create_credit_user_request):
    login_user_request = LoginUserRequest(username=create_credit_user_request.username, password=create_credit_user_request.password)
    return login_user_request