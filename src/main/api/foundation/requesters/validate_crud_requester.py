from src.main.api.configs.config import Config
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.models.base_model import BaseModel
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from typing import Optional
import allure

class ValidateCrudRequester(HttpRequester):
    def __init__(self, request_spec, endpoint, response_spec):
        super().__init__(request_spec, endpoint, response_spec)
        self.crud_requester = CrudRequester(
            request_spec=request_spec,
            endpoint=endpoint,
            response_spec=response_spec
        )
    def post(self, model: Optional[BaseModel] = None) -> BaseModel:
        response = self.crud_requester.post(model)
        with allure.step(f'Post {Config.fetch("backendUrl")}{self.endpoint.value.url} and Validated Model'):
            allure.attach(f'Validated Model response: {self.endpoint.value.response_model.__name__}')

        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())


    def delete(self, model: BaseModel) -> BaseModel:
        response = self.crud_requester.delete(model)
        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())

    def get(self, id_account: int) -> BaseModel:
        response = self.crud_requester.get(id_account)
        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())