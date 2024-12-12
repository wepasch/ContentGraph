import logging

from de.thb.content_graph.graph.node.activity import Activity
from de.thb.content_graph.graph.node.node_type import NodeType
from de.thb.content_graph.neo4j.neo4j_access import Neo4jAccess
from de.thb.misc.queryobjects import QueryNode
from de.thb.misc.util import setup_logging, get_resource

EXPORT_PATHS_DIR: str = 'export/paths'

FILTER_TIME: int = 10
FILTER_LENGTH: int = 3

logger = logging.getLogger(__name__)


def main(max_t: int = 30, max_len: int = 10, max_depth: int = 32) -> None:
    logger.info(f'Start generating for max_t: {max_t}, max_len: {max_len}, max_depth: {max_depth}')
    access: Neo4jAccess = Neo4jAccess.get_access()
    all_activities: list[Activity] = access.get_nodes_like(QueryNode('', NodeType.ACTIVITY))
    for a in all_activities:
        print(a)


if __name__ == '__main__':
    setup_logging()
    main()
