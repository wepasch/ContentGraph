from de.thb.content_graph.graph.node.type import NodeType


class QueryNode:
    __uid: str
    __node_type: NodeType

    def __init__(self, uid: str, node_type: NodeType):
        self.__uid = uid
        self.__node_type = node_type

    @property
    def uid(self) -> str:
        return self.__uid

    @property
    def node_type(self) -> NodeType:
        return self.__node_type
