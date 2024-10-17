from pathlib import Path
from typing import Any

from de.thb.content_graph.graph.node.medium import Medium
from de.thb.content_graph.graph.node.disease import Disease
from de.thb.content_graph.graph.node.content_node import ContentNode
from de.thb.content_graph.graph.node.type import MediumType, NodeType
from de.thb.content_graph.graph.constants import KEY_NAME, KEY_MEDIUM, KEY_UID, FLAG_NONE


class Activity(ContentNode):
    __medium: Medium | None
    __disease: Disease
    __required_uid: list[str] = []

    def __init__(self, uid: str, name: str, medium: Medium):
        super().__init__(uid, name)
        self.__medium = medium

    @property
    def medium(self) -> Medium:
        return self.__medium

    @property
    def type(self) -> NodeType:
        return NodeType.ACTIVITY

    @property
    def json(self) -> dict:
        return super().json | self.__medium.json

    @staticmethod
    def from_dict(data: dict[str: Any]) -> 'Activity':
        medium_data: dict = data.get(KEY_MEDIUM)
        if medium_data:
            medium: Medium | None = Medium.from_dict(data[KEY_MEDIUM])
        else:
            medium = None
        return Activity(data[KEY_UID], data[KEY_NAME], medium)

    @staticmethod
    def from_dicts(data: list[dict]) -> list['Activity']:
        activities: list[Activity] = []
        for d in data:
            activities.append(Activity.from_dict(d))
        return activities

    def has_medium(self) -> bool:
        return self.__medium is not None

    def __repr__(self) -> str:
        return f'{super().__repr__()}  ({self.__medium.name})'
