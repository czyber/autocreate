import os

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

from autocreate.app.models.user import User
from autocreate.app.services.index_storage_service import IndexStorageService
from autocreate.app.services.repo_service import RepoService
from autocreate.database.models.user import UserModel
from autocreate.infrastructure.sql_storage import SqlStorage
from autocreate.app.models.codebase import Codebase
from autocreate.database.models.codebase import CodebaseModel


class CodebaseService:
    def __init__(self):
        self._codebase_repository = SqlStorage(domain_entity=Codebase, db_entity=CodebaseModel)
        self._user_repository = SqlStorage(domain_entity=User, db_entity=UserModel)
        self._index_storage_service = IndexStorageService()

    def create_codebase(self, codebase: Codebase):
        return self._codebase_repository.save(codebase)

    def get_codebase(self, codebase_id: str):
        return self._codebase_repository.get_by_id(codebase_id)

    def get_codebase_from_github_url(self, user_id: str, github_url: str):
        user = self._user_repository.get_by_id(user_id)
        if not user:
            raise Exception("User not found")
        if not user.github_auth_token:
            raise Exception("User has no GitHub auth token")

        return self._codebase_repository.get_by_field("url", github_url)

    def does_index_exist_for_head_sha(self, head_sha: str):
        return self._codebase_repository.get_by_field("sha", head_sha)

    def index(self, repo_owner: str, repo_name: str, user_id: str):
        user = self._user_repository.get_by_id(user_id)
        if not user:
            raise Exception("User not found")
        if not user.github_auth_token:
            raise Exception("User has no GitHub auth token")

        repo_service = RepoService(repo_owner, repo_name, user.github_auth_token)
        tmp_dir, tmp_repo_dir = repo_service.download()

        if self.does_index_exist_for_head_sha(repo_service.sha):
            return tmp_dir, tmp_repo_dir

        codebase = self._codebase_repository.save(
            Codebase(
                url=f"{repo_owner}/{repo_name}",
                user_id=user_id,
                sha=repo_service.sha,
                name=repo_name,
            )
        )

        self._index(
            codebase=codebase,
            path=tmp_repo_dir
        )

        return tmp_dir, tmp_repo_dir

    def _index(self, codebase: Codebase, path: str) -> list[str]:
        docs = []
        for dirpath, dirnames, filenames in os.walk(path):
            for file in filenames:
                try:
                    loader = TextLoader(os.path.join(dirpath, file), encoding='utf-8')
                    docs.extend(loader.load_and_split())
                except Exception as e:  # noqa
                    pass

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(docs)
        return self._index_storage_service.add_documents(identifier=codebase.identifier, documents=texts)
