import textwrap
from langchain_core.prompts import ChatPromptTemplate
from autocreate.app.prompts.pydantic_xml_prompt import PydanticBaseXmlPrompt


class SolutionDiscoveryPromptXml(PydanticBaseXmlPrompt):
    file_path: str
    snippet: str

    @classmethod
    def get_template(cls):
        return cls(file_path="path/to/file.py", snippet="# Your code snippet here")


class SolutionDiscoveryPrompt:
    @staticmethod
    def get_system_message() -> ChatPromptTemplate:
        template = textwrap.dedent(
            f"""\
            You are an exceptional senior software engineer. 
            
            You are giving tasks to a coding agent that will perform code changes based on your instructions. The tasks must be clear and detailed enough that the coding agent can perform the task without any additional information.
            
            You have access to tools that allow you to search a codebase to find the relevant code snippets and view relevant files. You can use these tools as many times as you want to find the relevant code snippets.
            
            Your output must use the below format and use the types of steps provided:
            {SolutionDiscoveryPromptXml.get_template().to_string()}
            
            Guidelines:
            - Each code change must be a separate step and be explicit and clear.
            - No placeholders are allowed, the steps must be clear and detailed.
            - Make sure you use the tools provided to look through the codebase and at the files you are changing before outputting the steps.
            """)
        return ChatPromptTemplate.from_template(template)

    @staticmethod
    def get_user_message() -> ChatPromptTemplate:
        template = textwrap.dedent(
            """\
            You have to break the below task into steps:
            {task_str}
    
            Solve the task step-by-step then output a concise list of steps to perform in the output format provided in the system message.
            """)
        return ChatPromptTemplate.from_template(template)

