from de.thb.content_graph.graph.constants import KEY_NAME, KEY_ABBRV, KEY_PREF, KEY_UID
from de.thb.content_graph.graph.node.content_node import ContentNode
from de.thb.content_graph.graph.node.type import NodeType
from de.thb.misc.queryobjects import QueryNode


class Disease(ContentNode):
    __abbreviation: str
    __preferred: list[str]

    def __init__(self, uid: str, name: str, abbreviation: str, preferred: list[str]):
        super().__init__(uid, name)
        self.__abbreviation = abbreviation
        self.__preferred = preferred

    @classmethod
    def from_dict(cls, data: dict) -> 'Disease':
        return Disease(data[KEY_UID], data[KEY_NAME], data[KEY_ABBRV], data[KEY_PREF])

    @property
    def type(self) -> NodeType:
        return NodeType.DISEASE

    @property
    def abbreviation(self) -> str:
        return self.__abbreviation

    @property
    def preferred(self) -> list[str]:
        return self.__preferred

    @property
    def query_node(self) -> QueryNode:
        return QueryNode(super().uid, NodeType.DISEASE, {
            KEY_NAME: super().name,
            KEY_ABBRV: self.__abbreviation,
            KEY_PREF: self.__preferred
        })

    def __repr__(self) -> str:
        return f'{super().__repr__()} ({self.__abbreviation})'
