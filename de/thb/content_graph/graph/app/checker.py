import logging
from functools import reduce

from de.thb.content_graph.graph.node.activity import Activity
from de.thb.content_graph.graph.node.type import NodeType
from de.thb.content_graph.neo4j.neo4j_access import Neo4jAccess
from de.thb.misc.queryobjects import QueryNode
from de.thb.misc.util import setup_logging

logger = logging.getLogger(__name__)


def check_for_hidden(required_uids: list[str], available_uids: list[str], available_for_required: dict[str, list[str]]) \
        -> None | tuple[str, str,]:
    required_uid: str
    for required_uid in required_uids:
        available_uid: str
        for available_uid in available_uids:
            if available_uid not in available_for_required.get(required_uid, []):
                return required_uid, available_uid
    return None


def require(access: Neo4jAccess) -> bool:
    activities: list[Activity] = access.get_nodes_like(QueryNode('', NodeType.ACTIVITY))
    error_count: int = 0
    m: dict[str, list[str]] = {}
    activity: Activity
    for activity in activities:
        m[activity.uid] = sorted(activity.diseases)
    for activity in activities:
        error: None | tuple[str, str,] = check_for_hidden(activity.required, activity.diseases, m)
        if error:
            error_count += 1
            logger.error(f'{activity.uid} requires {error[0]} but it is not suitable for disease {error[1]}')
    return error_count == 0


def main() -> None:
    access: Neo4jAccess = Neo4jAccess.get_access()
    require(access)


if __name__ == '__main__':
    setup_logging()
    main()
