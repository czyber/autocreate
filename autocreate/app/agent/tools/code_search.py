from typing import Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic.v1 import BaseModel, Field


class CodeSearchInput(BaseModel):
    query: str = Field(description="should be a search query")


class CustomCalculatorTool(BaseTool):
    name = "Code Search"
    description = "Search for code snippets in an indexed codebase"
    args_schema: type[BaseModel] = CodeSearchInput
    return_direct: bool = True

    def _run(
        self, a: int, b: int, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        # TODO: Add context about available codebases

    async def _arun(
        self,
        a: int,
        b: int,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Async not implemented yet")
