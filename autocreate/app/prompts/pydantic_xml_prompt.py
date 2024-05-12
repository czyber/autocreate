from pydantic_xml import BaseXmlModel
from xml.etree import ElementTree as ET


class PydanticBaseXmlPrompt(BaseXmlModel):
    """Taken from
    https://github.com/getsentry/seer/blob/11827c2237c46c0c7f43c19d9b53074913775105/src/seer/automation/models.py#L213
    """
    def _pad_with_newlines(self, tree: ET.Element) -> None:
        for elem in tree.iter():
            if elem.text:
                stripped = elem.text.strip("\n")
                if stripped:
                    elem.text = "\n" + stripped + "\n"
            if elem.tail:
                stripped = elem.tail.strip("\n")
                if stripped:
                    elem.tail = "\n" + stripped + "\n"

    def to_string(self) -> str:
        tree: ET.Element = self.to_xml_tree()

        ET.indent(tree, space="", level=0)

        self._pad_with_newlines(tree)

        return ET.tostring(tree, encoding="unicode")
