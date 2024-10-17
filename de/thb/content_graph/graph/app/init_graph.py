import json
import logging

from de.thb.content_graph.graph.constants import KEY_NAME, KEY_DISEASES, KEY_ACTIVITIES, KEY_UID
from de.thb.content_graph.graph.node.type import NodeType, RelationType
from de.thb.content_graph.neo4j.neo4j_access import Neo4jAccess
from de.thb.misc.util import setup_logging, get_resource

logger = logging.getLogger(__name__)

BASE_GRAPH_PATH: str = 'graphs/base.json'
START_NODE_UID: str = 'm_00'
START_NODE_DATA: dict = {KEY_UID: START_NODE_UID, KEY_NAME: 'START'}
END_NODE_UID: str = 'm_01'
END_NODE_DATA: dict = {KEY_UID: END_NODE_UID, KEY_NAME: 'END'}


def add_start_stop(access: Neo4jAccess) -> None:
    access.create_activity(START_NODE_DATA)
    access.create_activity(END_NODE_DATA)
    disease_uids: list[str] = access.get_node_uids_of(NodeType.DISEASE)
    uid: str
    for uid in disease_uids:
        access.create_relation(START_NODE_UID, RelationType.SUITABLE, uid)
        access.create_relation(END_NODE_UID, RelationType.SUITABLE, uid)


def main() -> None:
    with open(get_resource(BASE_GRAPH_PATH), 'r') as f:
        graph_data: dict = json.load(f)
    access: Neo4jAccess = Neo4jAccess.get_access()
    access.delete_all()

    disease_data: dict
    for disease_data in graph_data[KEY_DISEASES]:
        access.create_disease(disease_data)
    requirements: dict[str, list[str]] = {}
    activity_data: dict
    for activity_data in graph_data[KEY_ACTIVITIES]:
        requirements = requirements | access.create_activity(activity_data)

    src: str
    dsts: list[str]
    for src, dsts in requirements.items():
        dst: str
        for dst in dsts:
            access.create_relation(src, RelationType.REQUIRES, dst)
    add_start_stop(access)


if __name__ == '__main__':
    setup_logging()
    main()
