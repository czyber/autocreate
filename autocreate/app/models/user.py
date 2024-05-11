from pydantic import BaseModel
from autocreate.app.models.codebase import Codebase
from autocreate.database.models.user import UserModel


class User(BaseModel):
    email: str
    github_auth_token: str | None
    id: str | None = None
    codebases: list[Codebase] | None = None

    def to_model(self):
        return UserModel(id=self.id, email=self.email, github_auth_token=self.github_auth_token)

    @staticmethod
    def from_model(model: UserModel):
        return User(id=model.id, email=model.email, github_auth_token=model.github_auth_token)



