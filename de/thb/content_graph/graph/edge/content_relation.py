from de.thb.content_graph.graph.edge.relation_type import RelationType


class ContentRelation:
    __rel_type: RelationType
    __data: dict = {}

    def __init__(self, rel_type: RelationType, data: dict = None):
        self.__rel_type = rel_type
        if data:
            self.__data = data

    @property
    def rel_type(self) -> RelationType:
        return self.__rel_type

    @property
    def label(self) -> str | None:
        if self.__rel_type:
            return self.__rel_type.label
        else:
            return None

    @property
    def data(self) -> dict:
        return self.__data
