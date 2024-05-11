from autocreate.infrastructure.sql_storage import SqlStorage
from autocreate.app.models.user import User
from autocreate.database.models.user import UserModel


class UserService:
    def __init__(self):
        self._user_repository = SqlStorage(domain_entity=User, db_entity=UserModel)

    def create_user(self, user: User):
        if self._user_repository.get_by_field("github_auth_token", user.github_auth_token):
            raise Exception("User already exists")
        return self._user_repository.save(user)

    def get_user(self, user_id: str):
        return self._user_repository.get_by_id(UserModel, user_id)

    def get_user_by_github_auth_token(self, github_auth_token: str):
        return self._user_repository.get_by_field("github_auth_token", github_auth_token)

    def get_all_users(self):
        return self._user_repository.get_all()

    def delete_user(self, user_id: str):
        return self._user_repository.delete(user_id)

    def add_auth_token(self, user_id: str, github_auth_token: str):
        user = self._user_repository.get_by_id(user_id)
        user.github_auth_token = github_auth_token
        return self._user_repository.update(user)

