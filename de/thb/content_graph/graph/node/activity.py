import logging

from de.thb.content_graph.graph.node.activity_type import ActivityType
from de.thb.content_graph.graph.node.content_node import ContentNode
from de.thb.content_graph.graph.node.node_type import NodeType
from de.thb.constants import KEY_NAME, KEY_MEDIUM, KEY_REQUIRED, KEY_DISEASES, KEY_UID, \
    KEY_DURATION_MIN
from de.thb.misc.queryobjects import QueryNode

NOT_SET_TIME: int = -1
logger = logging.getLogger(__name__)


class Activity(ContentNode):
    __type: ActivityType
    __medium_info: str
    __disease_uids: list[str]
    __required: list[str] = []
    __duration: int | None

    def __init__(self, uid: str, name: str, disease_uids: list[str], medium_info: str, required: list[str],
                 duration_min: int | None = None):
        super().__init__(uid, name)
        _activity_type: ActivityType | None = next(filter(lambda t: t.label == medium_info, ActivityType.values()), None)
        if _activity_type is None:
            logger.debug(f'Can not parse type for activity {uid} from name {medium_info}. Assign meta type.')
            self.__type = ActivityType.META
        else:
            self.__type = _activity_type
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
    def node_type(self) -> NodeType:
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
    def duration(self) -> int | None:
        return self.__duration

    @property
    def type(self) -> ActivityType:
        return self.__type

    def __repr__(self) -> str:
        return (f'{super().__repr__()} ({self.type.label}) {self.duration if self.duration else '?'} min. with '
                f'{self.__medium_info if self.__medium_info else '?'}')
