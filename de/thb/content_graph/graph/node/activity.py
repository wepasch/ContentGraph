from typing import Any

from de.thb.content_graph.graph.node.disease import Disease
from de.thb.content_graph.graph.node.content_node import ContentNode
from de.thb.content_graph.graph.node.type import NodeType
from de.thb.content_graph.graph.constants import KEY_NAME, KEY_MEDIUM, KEY_UID, NA


class Activity(ContentNode):
    __medium_info: str
    __disease_uid: Disease
    __required_uid: list[str] = []

    def __init__(self, uid: str, name: str, medium_info: str):
        super().__init__(uid, name)
        self.__medium_info = medium_info

    @property
    def medium(self) -> str:
        return self.__medium_info

    @property
    def type(self) -> NodeType:
        return NodeType.ACTIVITY

    @property
    def json(self) -> dict:
        return super().json | {KEY_MEDIUM: self.__medium_info}

    @staticmethod
    def from_dict(data: dict[str: Any]) -> 'Activity':
        return Activity(data[KEY_UID], data[KEY_NAME], data.get(KEY_MEDIUM, NA))

    @staticmethod
    def from_dicts(data: list[dict]) -> list['Activity']:
        activities: list[Activity] = []
        for d in data:
            activities.append(Activity.from_dict(d))
        return activities

    def has_medium(self) -> bool:
        return self.__medium_info not in [None, '', NA]

    def __repr__(self) -> str:
        return f'{super().__repr__()} with {self.__medium_info}'
