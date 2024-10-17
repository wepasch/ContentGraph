import config
import logging

from typing import Any
from neo4j import GraphDatabase, Driver

from de.thb.content_graph.graph.node.activity import Activity
from de.thb.content_graph.graph.constants import KEY_UID, KEY_MEDIUM, KEY_DISEASE, KEY_REQUIRED
from de.thb.content_graph.graph.node.disease import Disease
from de.thb.content_graph.graph.node.type import NodeType, RelationType
from de.thb.misc.cypher_util import Query
from de.thb.misc.util import copy_without

logger = logging.getLogger(__name__)


class Neo4jAccess:
    def __init__(self, host: str, port: int, user: str, password: str):
        uri: str = f"bolt://{host}:{port}"
        self.__driver: Driver = GraphDatabase.driver(uri, auth=(user, password))
        if not self.__is_connected():
            raise Exception("Neo4j connection failed")

    def __is_connected(self) -> bool:
        try:
            with self.__driver.session() as session:
                session.run("RETURN 1")
            return True
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False

    def get_node_uids_of(self, node_type: NodeType | None) -> list:
        """
        :param node_type: for all nodes of type or all node in graph if type == None
        :return: list of UIDs
        """
        query, params = Query.get_match_node(node_type, {}, 'n')
        with self.__driver.session() as session:
            results = session.run(query, params)
            return [r['n'][KEY_UID] for r in results]

    def get_related_without(self, src_node_type: NodeType, rel_type: RelationType, dst_node_type: NodeType,
                            dst_uid: str, exclude_uids: list[str]) -> list[str]:
        query, params = Query.get_related_without(src_node_type, rel_type, dst_node_type, dst_uid,
                                                  exclude_uids, 'n')
        with self.__driver.session() as session:
            results = session.run(query, params)
            return [result['n'][KEY_UID] for result in results]

    def create_activity(self, activity_data: dict) -> dict[str, list[str]]:
        self.create_node_from_dict(copy_without(activity_data, {KEY_MEDIUM, KEY_DISEASE}), NodeType.ACTIVITY)
        activity_uid: str = activity_data[KEY_UID]
        required_activities: list[str] = []
        try:
            required_activities = activity_data.pop(KEY_REQUIRED)
        except KeyError:
            pass
        try:
            medium_uid: str = activity_data.pop(KEY_MEDIUM)
            self.create_relation(activity_uid, RelationType.USES, medium_uid)
        except KeyError:
            pass
        try:
            disease_uid: str = activity_data.pop(KEY_DISEASE)
            self.create_relation(activity_uid, RelationType.SUITABLE, disease_uid)
        except KeyError:
            pass
        if required_activities:
            return {activity_uid: required_activities}
        else:
            return {}

    def create_disease(self, disease_data: dict) -> None:
        self.create_node_from_dict(disease_data, NodeType.DISEASE)

    def create_node_from_dict(self, node_data: dict[str, Any], node_type: NodeType) -> None:
        query, params = Query.get_create_node(node_type, node_data, 'n')
        with self.__driver.session() as session:
            session.run(query, params)

    def create_relation(self, src_uid: str, relation_type: RelationType, dst_uid: str) -> None:
        query, params = Query.create_relation(src_uid, relation_type, dst_uid)
        with self.__driver.session() as session:
            session.run(query, params)

    def delete_all(self) -> None:
        with self.__driver.session() as session:
            session.run("MATCH ()-[r]->() DELETE r")
            session.run("MATCH (n) DELETE n")

    @classmethod
    def get_access(cls) -> 'Neo4jAccess':
        return Neo4jAccess(config.NEO4J_URI, config.NEO4J_PORT, config.NEO4J_USER, config.NEO4J_PWD)

    @staticmethod
    def __get_constr(node_type: NodeType):
        match node_type:
            case NodeType.ACTIVITY:
                return Activity.from_dict
            case NodeType.DISEASE:
                return Disease.from_dict
            case _:
                raise Exception(f'No constructor from dictionary for node type: {node_type}')
