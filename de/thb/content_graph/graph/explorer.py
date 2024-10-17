import copy

from de.thb.content_graph.graph.node.type import RelationType, NodeType
from de.thb.content_graph.neo4j.neo4j_access import Neo4jAccess
from de.thb.content_graph.graph.app.init_graph import START_NODE_UID, END_NODE_UID


class Explorer:
    __disease_uid: str
    __access: Neo4jAccess
    __paths: list[list[str]] = [[START_NODE_UID]]

    def __init__(self, disease_uid: str, access: Neo4jAccess):
        self.__disease_uid = disease_uid
        self.__access = access

    @property
    def paths(self) -> list[list[str]]:
        return self.__paths

    def naiv_move(self) -> list[list[str]]:
        """
        Collects all paths from start uid to end uid using only activities suitable for own disease.
        Does not use activity twice.
        """
        if not next(filter(lambda p: p[-1] != END_NODE_UID, self.__paths), None):
            return self.__paths
        extended_paths: list[list[str]] = []
        path: list[str]
        for path in self.__paths:
            curr_uid: str = path[-1]
            if curr_uid == END_NODE_UID:
                extended_paths.append(copy.deepcopy(path))
                continue
            next_stops: list[str] = self.__access.get_related_without(NodeType.ACTIVITY, RelationType.SUITABLE,
                                                                      NodeType.DISEASE, self.__disease_uid, path)
            next_stop: str
            for next_stop in next_stops:
                extended_path: list[str] = copy.deepcopy(path + [next_stop])
                extended_paths.append(extended_path)
        self.__paths = extended_paths
        self.naiv_move()


