from src.main.api.models.base_model import BaseModel
from typing import Annotated
from src.main.api.generators.creation_rule import CreationRule


class CreateUserRequest(BaseModel):
    username: Annotated[str, CreationRule(regex="^[a-zA-Z0-9]{3,15}$")]
    password: Annotated[str, CreationRule(regex="^[A-Z]{3}[a-z]{3}[0-9]{2}[!$_]{4}$")]
    role: str