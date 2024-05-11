from sqlalchemy import ForeignKey

from autocreate.database.models.base import Base, new_uuid

from sqlalchemy.orm import Mapped, mapped_column


class CodebaseModel(Base):
    __tablename__ = 'codebases'
    id: Mapped[str] = mapped_column(primary_key=True, default=new_uuid)
    user_id: Mapped[str | None] = mapped_column(ForeignKey('users.id'))
    name: Mapped[str]
    url: Mapped[str | None]
    sha: Mapped[str | None]


