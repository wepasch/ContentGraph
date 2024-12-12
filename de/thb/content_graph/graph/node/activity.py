import logging
from de.thb.content_graph.graph.node.content_node import ContentNode
from de.thb.content_graph.graph.node.type import NodeType
from de.thb.content_graph.graph.constants import KEY_NAME, KEY_MEDIUM, KEY_REQUIRED, KEY_DISEASES, KEY_UID, \
    KEY_DURATION_MIN
from de.thb.misc.queryobjects import QueryNode

NOT_SET_TIME: int = -1
logger = logging.getLogger(__name__)


class Activity(ContentNode):
    __medium_info: str
    __disease_uids: list[str]
    __required: list[str] = []
    __duration: int | None

    def __init__(self, uid: str, name: str, disease_uids: list[str], medium_info: str, required: list[str],
                 duration_min: int | None = None):
        super().__init__(uid, name)
        self.__disease_uids = disease_uids
        self.__medium_info = medium_info
        self.__required = required
        if duration_min < 0:
            logger.warning(f'Invalid time {duration_min} for activity {uid}.')
            duration_min = None
        self.__duration = duration_min

    @classmethod
    def from_dict(cls, data: dict) -> 'Activity':
        duration_min: int | None = None
        try:
            duration_min = int(data[KEY_DURATION_MIN])
        except Exception as e:
            logger.warning(f'Can not set activity duration from {data[KEY_DURATION_MIN]}: {e}')
        return Activity(data[KEY_UID], data[KEY_NAME], data[KEY_DISEASES], data[KEY_MEDIUM], data[KEY_REQUIRED],
                        duration_min=duration_min)

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
            KEY_REQUIRED: self.__required,
            KEY_DURATION_MIN: self.__duration
        })

    @property
    def diseases(self) -> list[str]:
        return self.__disease_uids

    @property
    def duration_min(self) -> int | None:
        return self.__duration

    def __repr__(self) -> str:
        return (f'{super().__repr__()} {self.duration_min if self.duration_min else '?'} min. with '
                f'{self.__medium_info if self.__medium_info else '?'}')
