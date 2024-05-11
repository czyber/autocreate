from typing import TypeVar, Any
from autocreate.database.db import Session

T = TypeVar("T")
V = TypeVar("V")


class SqlStorage:
    def __init__(self, domain_entity: T, db_entity: V):
        self.domain_entity = domain_entity
        self.db_entity = db_entity

    def save(self, entity: T) -> T:
        with Session() as session:
            session.add(entity.to_model())
            session.commit()
            return entity

    def get_by_id(self, entity_id: str) -> T:
        with Session() as session:
            return self.domain_entity.from_model(session.query(self.db_entity).filter_by(id=entity_id).first())

    def get_by_field(self, field: str, value: Any) -> T:
        with Session() as session:
            return session.query(self.db_entity).filter(getattr(self.db_entity, field) == value).first()

    def get_all(self) -> T:
        with Session() as session:
            return session.query(self.db_entity).all()

    def update(self, entity: T) -> T:
        with Session() as session:
            session.merge(entity.to_model())
            session.commit()
            return entity

    def delete(self, entity: T) -> T:
        with Session() as session:
            session.delete(entity.to_model())
            session.commit()
            return entity

    def delete_by_id(self, entity_id: str) -> T:
        with Session() as session:
            entity = session.query(self.db_entity).filter_by(id=entity_id).first()
            session.delete(entity)
            session.commit()
            return entity

    def delete_by_field(self, field: str, value: Any) -> T:
        with Session() as session:
            entity = session.query(self.db_entity).filter_by(field=value).first()
            session.delete(entity)
            session.commit()
            return entity

    def delete_all(self) -> T:
        with Session() as session:
            entities = session.query(self.db_entity).all()
            for entity in entities:
                session.delete(entity)
            session.commit()
            return entities

    def get_domain_entity(self, db_entity: V) -> T:
        return self.domain_entity.from_model(db_entity)

    def get_db_entity(self, domain_entity: T) -> V:
        return domain_entity.to_model()


