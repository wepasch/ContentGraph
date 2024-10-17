from typing import Any

from de.thb.content_graph.graph.constants import KEY_UID, KEY_NAME, KEY_ABRV
from de.thb.content_graph.graph.node.content_node import ContentNode
from de.thb.content_graph.graph.node.type import NodeType


class Therapy(ContentNode):
    def __init__(self, uid: str, name: str):
        super().__init__(uid, name)

    @property
    def type(self) -> NodeType:
        return NodeType.THERAPY

    @property
    def json(self) -> dict:
        return super().json

    @staticmethod
    def from_dict(data: dict[str: Any]) -> 'Therapy':
        return Therapy(data[KEY_UID], data[KEY_NAME])

    @staticmethod
    def from_dicts(data: list[dict]) -> list['Therapy']:
        therapies: list[Therapy] = []
        for d in data:
            therapies.append(Therapy.from_dict(d))
        return therapies

    def __repr__(self) -> str:
        return f'{super().__repr__()}'
