from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI

from autocreate.app.models.codebase import Codebase
from autocreate.app.prompts.solution_discovery_prompt import SolutionDiscoveryPrompt
from autocreate.app.services.index_storage_service import IndexStorageService
from autocreate.database.models.codebase import CodebaseModel
from autocreate.infrastructure.sql_storage import SqlStorage
from dataclasses import dataclass


class DomainEntity:
    attributes: dict


@dataclass
class Solution:
    steps: list[str]


class SolutionDiscoveryService:
    def __init__(self):
        self._codebase_repository = SqlStorage(domain_entity=Codebase, db_entity=CodebaseModel)
        self._index_storage_service = IndexStorageService()

    def add_domain_entity(self, domain_entity: DomainEntity, codebase_id: str):
        codebase = self._codebase_repository.get_by_id(codebase_id)
        if not codebase:
            raise Exception("Codebase not found")

        solution = self._add_domain_entity(codebase, domain_entity)

        self._codebase_repository.update(codebase)

    def _add_domain_entity(self, codebase: Codebase, domain_entity: DomainEntity) -> Solution:
        retriever = self._index_storage_service.get_retriever(codebase.id)
        model = ChatOpenAI(model='gpt-4-turbo-2024-04-09')
        agent = create_react_agent(llm=model, retriever=retriever)
        conversational_chain = ConversationalRetrievalChain.from_llm(model, retriever=retriever)

        conversational_chain.invoke(SolutionDiscoveryPrompt.get_system_message())

        return Solution(steps=retriever.search(domain_entity.attributes))
