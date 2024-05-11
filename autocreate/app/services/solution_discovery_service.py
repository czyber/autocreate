from autocreate.app.models.codebase import Codebase
from autocreate.database.models.codebase import CodebaseModel
from autocreate.infrastructure.sql_storage import SqlStorage


class SolutionDiscoveryService:
    def __init__(self):
        self._codebase_repository = SqlStorage(domain_entity=Codebase, db_entity=CodebaseModel)

    def get_solution(self, codebase_id: str, problem_prompt):
        codebase = self._codebase_repository.get_by_id(codebase_id)
        if not codebase:
            raise Exception("Codebase not found")

        return self._get_solution(codebase, problem_prompt)
