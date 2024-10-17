import config
import logging

from typing import Any
from neo4j import GraphDatabase, Driver, Result

from de.thb.content_graph.graph.node.activity import Activity
from de.thb.content_graph.graph.node.content_node import ContentNode
from de.thb.content_graph.graph.node.disease import Disease
from de.thb.content_graph.graph.node.medium import Medium
from de.thb.content_graph.graph.constants import LABEL_MEDIUM, KEY_UID, KEY_MEDIUM, KEY_DISEASE, KEY_REQUIRED, KEY_TYPE, \
    KEY_NAME
from de.thb.content_graph.graph.node.therapy import Therapy
from de.thb.content_graph.graph.node.type import NodeType, MediumType, RelationType
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
            print(f"Connection failed: {e}")
            return False

    def get_nodes_with(self, node: ContentNode) -> list[ContentNode]:
        nodes: list[ContentNode] = []
        node_type: NodeType = node.type
        query, params = Query.get_match_node(node_type, node.json, 'n')
        with self.__driver.session() as session:
            results = session.run(query, params)
            for result in results:
                nodes.append(Neo4jAccess.__get_constr(node_type)(result['n']))
        return nodes

    def get_node_by_uid(self, uid: str) -> ContentNode:
        pass

    def get_node_uids_of(self, node_type: NodeType | None) -> list:
        query, params = Query.get_match_node(node_type, {}, 'n')
        with self.__driver.session() as session:
            results = session.run(query, params)
            return [r['n'][KEY_UID] for r in results]

    def get_related_without(self, src_node_type: NodeType, rel_type: RelationType, dst_node_type: NodeType,
                            dst_uid: str, exclude_uids: list[str], reverse: bool = False) -> list[str]:
        query, params = Query.get_related_without(src_node_type, rel_type, dst_node_type, dst_uid,
                                                  exclude_uids, 'n', reverse)
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

    def create_medium(self, medium_data: dict) -> None:
        type_desc: str = medium_data.get(KEY_TYPE)
        medium_data[KEY_TYPE] = MediumType.get(type_desc).name
        self.create_node_from_dict(medium_data, NodeType.MEDIUM)

    def create_disease(self, disease_data: dict) -> None:
        self.create_node_from_dict(disease_data, NodeType.DISEASE)

    def create_meta_node(self, meta_data: dict) -> None:
        self.create_node_from_dict(meta_data, NodeType.META)

    def __create_node(self, node: ContentNode) -> str:
        existing_nodes: list[ContentNode] = self.get_nodes_with(node)
        if existing_nodes:
            logger.info(f'Already created {node}.')
            return existing_nodes[0].uid
        else:
            query, params = Query.get_create_node(node.type, node.json, 'n')
            with self.__driver.session() as session:
                result: Result = session.run(query, params)
                return next(result)['n'][KEY_UID]

    def create_node_from_dict(self, node_data: dict[str, Any], node_type: NodeType) -> None:
        query, params = Query.get_create_node(node_type, node_data, 'n')
        with self.__driver.session() as session:
            result: Result = session.run(query, params)
            return next(result)['n'][KEY_UID]

    def create_relation(self, src_uid: str, relation_type: RelationType, dst_uid: str) -> None:
        query = Query.create_relation(src_uid, relation_type, dst_uid)
        with self.__driver.session() as session:
            session.run(query)

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
            case NodeType.MEDIUM:
                return Medium.from_dict
            case NodeType.DISEASE:
                return Disease.from_dict
            case NodeType.THERAPY:
                return Therapy.from_dict
            case _:
                raise Exception(f'No constructor from dictionary for node type: {node_type}')
