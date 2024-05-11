from langchain_community.vectorstores import DeepLake
from langchain_openai import OpenAIEmbeddings


class IndexStorageService:
    username = "czyber"

    def get_retriever(self, identifier: str):
        db = self._get_retriever_db(identifier)
        retriever = db.as_retriever()
        retriever.search_kwargs['distance_metric'] = 'cos'
        retriever.search_kwargs['fetch_k'] = 100
        retriever.search_kwargs['k'] = 10
        return retriever

    def get_db(self, identifier: str):
        db = self._get_db(identifier)
        return db

    def add_documents(self, identifier: str, documents: list) -> list[str]:
        db = self._get_db(identifier)
        return db.add_documents(documents)

    @classmethod
    def _get_retriever_db(cls, identifier: str):
        return DeepLake(dataset_path=f"hub://{cls.username}/{identifier}", overwrite=False)

    @classmethod
    def _get_db(cls, identifier: str):
        embeddings = OpenAIEmbeddings(disallowed_special=())
        return DeepLake(dataset_path=f"hub://{cls.username}/{identifier}", overwrite=True, embedding=embeddings, runtime={"tensor_db": True})

