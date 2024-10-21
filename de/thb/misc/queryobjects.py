from de.thb.content_graph.graph.node.type import NodeType, RelationType


class QueryObject:
    __uid: str
    __data: dict = {}

    def __init__(self, uid: str, data=None):
        self.__uid = uid
        if data:
            self.__data = data

    @property
    def uid(self) -> str:
        return self.__uid

    @property
    def data(self) -> dict:
        return self.__data

    @property
    def label(self) -> str:
        raise NotImplementedError("no label property for 'abstract' QueryObject")

    def add_data(self, add_data: dict) -> None:
        self.__data.update(add_data)


class QueryNode(QueryObject):
    """
    record class to transfer node information in one object
    """
    __node_type: NodeType | None

    def __init__(self, uid: str, node_type: NodeType | None, data=None):
        super().__init__(uid, data=data)
        self.__node_type = node_type

    @property
    def node_type(self) -> NodeType | None:
        if self.__node_type:
            return self.__node_type
        else:
            return None

    @property
    def label(self) -> str | None:
        if self.__node_type:
            return self.__node_type.label
        else:
            return None

class QueryRelation(QueryObject):
    """
    record class to transfer relation information in one object
    """
    __rel_type: RelationType

    def __init__(self, uid: str, rel_type: RelationType | None, data=None):
        super().__init__(uid, data)
        self.__rel_type = rel_type

    @property
    def rel_type(self) -> RelationType:
        return self.__rel_type

    @property
    def label(self) -> str:
        return self.__rel_type.label
