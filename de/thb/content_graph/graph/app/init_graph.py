import json
import logging

from de.thb.content_graph.graph.node.activity import Activity
from de.thb.content_graph.graph.node.disease import Disease
from de.thb.content_graph.graph.node.medium import Medium

from de.thb.content_graph.graph.constants import KEY_NODES, KEY_NAME, KEY_MEDIA, KEY_DISEASES, KEY_ACTIVITIES, KEY_UID
from de.thb.content_graph.graph.node.therapy import Therapy
from de.thb.content_graph.graph.node.type import MediumType, NodeType, RelationType
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

    m: dict
    for m in graph_data[KEY_MEDIA]:
        access.create_medium(m)
    d: dict
    for d in graph_data[KEY_DISEASES]:
        access.create_disease(d)
    requirements: dict[str, list[str]] = {}
    a: dict
    for a in graph_data[KEY_ACTIVITIES]:
        requirements = requirements | access.create_activity(a)

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
