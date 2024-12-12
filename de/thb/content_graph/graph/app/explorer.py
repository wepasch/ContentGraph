import copy

from de.thb.content_graph.graph.node.disease import Disease
from de.thb.content_graph.graph.node.node_type import NodeType
from de.thb.content_graph.graph.edge.relation_type import RelationType
from de.thb.content_graph.neo4j.neo4j_access import Neo4jAccess
from de.thb.content_graph.graph.app.init_graph import START_NODE_UID, END_NODE_UID
from de.thb.misc.queryobjects import QueryNode, QueryRelation


class Explorer:
    __disease: Disease
    __access: Neo4jAccess
    __paths: list[list[str]] = [[START_NODE_UID]]

    def __init__(self, disease: Disease, access: Neo4jAccess):
        self.__disease = disease
        self.__access = access

    @property
    def paths(self) -> list[list[str]]:
        return self.__paths

    def run(self, suitable: bool = False, require: bool = False) -> list[list[str]]:
        """
        END_UID terminates a path. It must always be available, else each recursive call must track weather at least
        one path is expanded (mby by flag var).
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

            next_stops: list[str] = self.__get_next_nodes(path, suitable, require)
            next_stop: str
            for next_stop in next_stops:
                extended_path: list[str] = copy.deepcopy(path + [next_stop])
                extended_paths.append(extended_path)
        self.__paths = extended_paths
        self.run(suitable=suitable, require=require)

    def __get_next_nodes(self, path: list[str], suitable: bool, require: bool) -> list[str]:
        if require:
            next_stops: list[str] = self.__access.get_related_exclude_require(
                QueryNode('', NodeType.ACTIVITY), QueryRelation('', RelationType.SUITABLE),
                self.__disease.query_node, path, path)
        elif suitable:
            next_stops: list[str] = self.__access.get_related_exclude(
                QueryNode('', NodeType.ACTIVITY), QueryRelation('', RelationType.SUITABLE),
                self.__disease.query_node, path)
        else:
            next_stops: list[str] = self.__access.get_related_exclude(
                QueryNode('', NodeType.ACTIVITY), QueryRelation('', RelationType.SUITABLE), None, path)

        return next_stops
