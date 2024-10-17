from de.thb.content_graph.graph.edge.type import PathType


class Path:
    __uid: str
    __type: PathType
    __src_uid: str
    __dst_uid: str

    def __init__(self, uid: str, path_type: PathType, src_uid: str, dst_uid: str):
        self.__uid = uid
        self.__type = path_type
        self.__src_uid = src_uid
        self.__dst_uid = dst_uid

    @property
    def uid(self) -> str:
        return self.__uid

    @property
    def type(self) -> PathType:
        return self.__type

    @property
    def src_uid(self) -> str:
        return self.__src_uid

    @property
    def dst_uid(self) -> str:
        return self.__dst_uid

