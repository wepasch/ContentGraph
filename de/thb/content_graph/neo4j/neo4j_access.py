import config
import logging

from neo4j import GraphDatabase, Driver

from de.thb.content_graph.graph.constants import KEY_UID
from de.thb.content_graph.graph.node.activity import Activity
from de.thb.content_graph.graph.node.content_node import ContentNode
from de.thb.content_graph.graph.node.disease import Disease
from de.thb.content_graph.graph.node.type import NodeType, RelationType
from de.thb.misc.cypher_util import N4Query
from de.thb.misc.queryobjects import QueryNode, QueryRelation

logger = logging.getLogger(__name__)


def _node_from_dict(data: dict, node_type: NodeType) -> ContentNode:
    match node_type:
        case NodeType.ACTIVITY:
            return Activity.from_dict(data)
        case NodeType.DISEASE:
            return Disease.from_dict(data)
        case _:
            raise ValueError(f'unknown node type {node_type} to create ContentNode from')


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

    def get_nodes_like(self, node: QueryNode) -> list[ContentNode | Activity | Disease]:
        query = N4Query.get_node_like(node, 'n')
        with self.__driver.session() as session:
            results = session.run(query)
            return [_node_from_dict(r.data()['n'], node.node_type) for r in results]

    def get_related_exclude(self, src: QueryNode, rel: QueryRelation | None, dst: QueryNode | None,
                            exclude_uids: list[str], reverse: bool = False) -> list[str]:
        query = N4Query.get_related_exclude(src, rel, dst, exclude_uids, 'n', reverse)
        with self.__driver.session() as session:
            results = session.run(query)
            return [result['n'][KEY_UID] for result in results]

    def get_related_exclude_require(self, src: QueryNode, rel: QueryRelation | None, dst: QueryNode | None,
                                    exclude_uids: list[str], available_uids: list[str],
                                    reverse: bool = False) -> list[str]:
        query = N4Query.get_related_exclude_require(src, rel, dst, exclude_uids, available_uids, 'n', reverse)
        with self.__driver.session() as session:
            results = session.run(query)
            return [result['n'][KEY_UID] for result in results]

    def get_connected_by(self, src: QueryNode, rel: QueryRelation) -> list[str]:
        query = N4Query.get_connected_by(src, rel, 'nn')
        with self.__driver.session() as session:
            result = [r for r in session.run(query)]
            try:
                return [n[KEY_UID] for n in result[-1]['nn']]
            except IndexError:
                return []


    def create_node(self, node: QueryNode) -> None:
        node.add_data({KEY_UID: node.uid})
        query = N4Query.create_node(node)
        self.__post_query(query)

    def create_relation(self, src: QueryNode, rel: QueryRelation, dst: QueryNode) -> None:
        query = N4Query.create_relation(src.uid, rel, dst.uid)
        self.__post_query(query)

    def delete_all(self) -> None:
        self.__post_queries([N4Query.delete_all_relations(), N4Query.delete_all_nodes()])
        logger.info('Deleted full graph.')

    def __post_query(self, query) -> None:
        with self.__driver.session() as session:
            session.run(query)

    def __post_queries(self, query_params: list) -> None:
        """
        can be used if no return is expected
        :param query_params: list of query-params tuple
        """
        with self.__driver.session() as session:
            for query_param in query_params:
                session.run(query_param)

    @classmethod
    def get_access(cls) -> 'Neo4jAccess':
        return Neo4jAccess(config.NEO4J_URI, config.NEO4J_PORT, config.NEO4J_USER, config.NEO4J_PWD)
