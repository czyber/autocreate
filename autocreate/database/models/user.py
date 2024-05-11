from autocreate.database.models.base import Base, new_uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship
from autocreate.database.models.codebase import CodebaseModel


class UserModel(Base):
    __tablename__ = 'users'
    id: Mapped[str] = mapped_column(primary_key=True, default=new_uuid)
    email: Mapped[str]
    github_auth_token: Mapped[str | None]
    codebases: Mapped[list['CodebaseModel']] = relationship()

