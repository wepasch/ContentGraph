from de.thb.constants import KEY_NAME, KEY_UID
from de.thb.content_graph.graph.node.node_type import NodeType


class ContentNode:
    __uid: str
    __name: str

    def __init__(self, uid: str, name: str):
        self.__uid = uid
        self.__name = name

    @property
    def uid(self) -> str:
        return self.__uid

    @property
    def name(self) -> str:
        return self.__name

    @property
    def json(self) -> dict:
        return {
            KEY_UID: self.uid,
            KEY_NAME: self.name
        }

    def __repr__(self) -> str:
        return f'[{self.__uid}] {self.name}'

    @property
    def type(self) -> NodeType:
        raise NotImplementedError('self.type not implemented for super class. Implementation only in derived class.')
