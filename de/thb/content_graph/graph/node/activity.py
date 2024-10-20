from de.thb.content_graph.graph.node.content_node import ContentNode
from de.thb.content_graph.graph.node.type import NodeType
from de.thb.content_graph.graph.constants import KEY_NAME, KEY_MEDIUM, KEY_REQUIRED
from de.thb.misc.queryobjects import QueryNode


class Activity(ContentNode):
    __medium_info: str
    __disease_uids: list[str]
    __requires: list[str] = []

    def __init__(self, uid: str, name: str, disease_uids: list[str], medium_info: str, requires: list[str]):
        super().__init__(uid, name)
        self.__disease_uids = disease_uids
        self.__medium_info = medium_info
        self.__requires = requires

    @property
    def medium(self) -> str:
        return self.__medium_info

    @property
    def type(self) -> NodeType:
        return NodeType.ACTIVITY

    @property
    def requires(self) -> list[str]:
        return self.__requires

    @property
    def query_node(self) -> QueryNode:
        return QueryNode(super().uid, NodeType.ACTIVITY, {
            KEY_NAME: super().name,
            KEY_MEDIUM: self.__medium_info,
            KEY_REQUIRED: self.__requires
        })

    @property
    def diseases(self) -> list[str]:
        return self.__disease_uids

    def __repr__(self) -> str:
        return f'{super().__repr__()} with {self.__medium_info}'
