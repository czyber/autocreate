from fastapi import FastAPI
from pydantic import BaseModel

from autocreate.app.models.codebase import Codebase
from autocreate.app.services.codebase_service import CodebaseService

from autocreate.app.models.user import User
from autocreate.app.services.user_service import UserService
from autocreate.app.utils.helpers import cleanup_dir
from dotenv import load_dotenv

load_dotenv()

codebase_service = CodebaseService()
user_service = UserService()

app = FastAPI()


class CreateCodebaseRequest(BaseModel):
    name: str
    url: str


@app.post("/codebase")
def create_codebase(request: CreateCodebaseRequest):
    codebase = codebase_service.create_codebase(codebase=Codebase(name=request.name, url=request.url))
    return codebase


class CreateUserRequest(BaseModel):
    email: str
    github_auth_token: str | None


@app.post("/users")
def create_user(request: CreateUserRequest):
    return user_service.create_user(user=User(email=request.email, github_auth_token=request.github_auth_token))


class AddAuthTokenRequest(BaseModel):
    github_auth_token: str


@app.patch("/users/{user_id}/auth_token")
def add_auth_token(user_id: str, request: AddAuthTokenRequest):
    return user_service.add_auth_token(user_id, request.github_auth_token)


class IndexCodebaseRequest(BaseModel):
    repo_name: str
    user_id: str
    repo_owner: str


@app.post("/codebase/download")
def download_codebase(request: IndexCodebaseRequest):
    root_dir, repo_dir = codebase_service.index(request.repo_owner, request.repo_name, request.user_id)
    cleanup_dir(root_dir)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
