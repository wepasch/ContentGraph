import logging
from pathlib import Path

from de.thb.content_graph.graph.constants import KEY_NAME, KEY_TYPE, KEY_PATH, KEY_UID
from de.thb.content_graph.graph.node.content_node import ContentNode
from de.thb.content_graph.graph.node.type import MediumType, NodeType

logger = logging.getLogger(__name__)


class Medium(ContentNode):
    __medium_type: MediumType
    __file_path: Path

    def __init__(self, uid: str, name: str, medium_type: MediumType, file_path: Path):
        super().__init__(uid, name)
        self.__medium_type = medium_type
        self.__file_path = file_path

    @property
    def medium_type(self) -> MediumType:
        return self.__medium_type

    @property
    def file_path(self) -> Path:
        return self.__file_path

    @property
    def type(self) -> NodeType:
        return NodeType.MEDIUM

    @property
    def json(self) -> dict:
        return super().json | {KEY_PATH: str(self.__file_path),
                               KEY_TYPE: self.__medium_type.name}

    def __repr__(self) -> str:
        return f'{super().__repr__()}  ({self.__medium_type.name}) -> {self.file_path}'
    
    @staticmethod
    def from_dict(data: dict[str: str]) -> 'Medium':
        media_type: MediumType = MediumType.get(data[KEY_TYPE])
        file_path: Path = Path(data[KEY_PATH])
        return Medium(data[KEY_UID], data[KEY_NAME], media_type, file_path)

    @staticmethod
    def from_dicts(data: list[dict]) -> list['Medium']:
        media: list[Medium] = []
        for d in data:
            media.append(Medium.from_dict(d))
        return media
