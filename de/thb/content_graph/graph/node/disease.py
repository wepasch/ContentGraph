from de.thb.content_graph.graph.constants import KEY_NAME, KEY_ABRV, KEY_UID
from de.thb.content_graph.graph.node.content_node import ContentNode
from de.thb.content_graph.graph.node.type import NodeType


class Disease(ContentNode):
    __abbreviation: str

    def __init__(self, uid: str, name: str, abbreviation: str):
        super().__init__(uid, name)
        self.__abbreviation = abbreviation

    @property
    def type(self) -> NodeType:
        return NodeType.DISEASE

    @property
    def abbreviation(self) -> str:
        return self.__abbreviation

    @property
    def json(self) -> dict:
        return super().json | {KEY_ABRV: self.__abbreviation}

    @staticmethod
    def from_dict(data: dict[str: str]) -> 'Disease':
        return Disease(data[KEY_UID], data[KEY_NAME], data[KEY_ABRV])

    @staticmethod
    def from_dicts(data: list[dict]) -> list['Disease']:
        diseases: list[Disease] = []
        for d in data:
            diseases.append(Disease.from_dict(d))
        return diseases

    def __repr__(self) -> str:
        return f'{super().__repr__()} ({self.__abbreviation})'
