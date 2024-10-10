from de.thb.content_graph.medium import Medium
from de.thb.content_graph.domain.disease import Disease

class Activity:
    __uid: str
    __name: str
    __medium: Medium
    __disease: Disease
    __required_uid: list[str] = []

    def __init__(self, uid: str, name: str, medium: Medium):
        self.__uid = uid
        self.__name = name
        self.__medium = medium

    @property
    def uid(self) -> str:
        return self.__uid

    @property
    def name(self) -> str:
        return self.__name

    @property
    def medium(self) -> Medium:
        return self.__medium