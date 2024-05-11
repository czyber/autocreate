from pydantic import BaseModel
from autocreate.database.models.codebase import CodebaseModel


class Codebase(BaseModel):
    user_id: str
    name: str
    url: str
    sha: str | None = None
    id: str | None = None

    def to_model(self):
        return CodebaseModel(
            id=self.id,
            user_id=self.user_id,
            name=self.name,
            url=self.url,
            sha=self.sha
        )

    @staticmethod
    def from_model(model: CodebaseModel):
        return Codebase(
            id=model.id,
            user_id=model.user_id,
            sha=model.sha,
            name=model.name,
            url=model.url
        )

    @property
    def identifier(self):
        return f"{self.user_id}-{self.name}-{self.sha}"


