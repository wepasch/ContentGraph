from de.thb.content_graph.graph.node.content_node import ContentNode
from de.thb.content_graph.graph.node.type import NodeType
from de.thb.content_graph.graph.constants import KEY_NAME, KEY_MEDIUM, KEY_REQUIRED, KEY_DISEASES, KEY_UID
from de.thb.misc.queryobjects import QueryNode


class Activity(ContentNode):
    __medium_info: str
    __disease_uids: list[str]
    __required: list[str] = []

    def __init__(self, uid: str, name: str, disease_uids: list[str], medium_info: str, required: list[str]):
        super().__init__(uid, name)
        self.__disease_uids = disease_uids
        self.__medium_info = medium_info
        self.__required = required

    @classmethod
    def from_dict(cls, data: dict) -> 'Activity':
        return Activity(data[KEY_UID], data[KEY_NAME], data[KEY_DISEASES], data[KEY_MEDIUM], data[KEY_REQUIRED])

    @property
    def medium(self) -> str:
        return self.__medium_info

    @property
    def type(self) -> NodeType:
        return NodeType.ACTIVITY

    @property
    def required(self) -> list[str]:
        return self.__required

    @property
    def query_node(self) -> QueryNode:
        return QueryNode(super().uid, NodeType.ACTIVITY, {
            KEY_NAME: super().name,
            KEY_MEDIUM: self.__medium_info,
            KEY_REQUIRED: self.__required
        })

    @property
    def diseases(self) -> list[str]:
        return self.__disease_uids

    def __repr__(self) -> str:
        return f'{super().__repr__()} with {self.__medium_info}'
