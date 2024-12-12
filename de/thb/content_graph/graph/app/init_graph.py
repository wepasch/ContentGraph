import json
import logging

from de.thb.content_graph.graph.constants import KEY_NAME, KEY_DISEASES, KEY_ACTIVITIES, KEY_UID, KEY_REQUIRED, \
    KEY_ABBRV, KEY_PREF, KEY_MEDIUM, KEY_DISEASE, KEY_DURATION_MIN
from de.thb.content_graph.graph.node.activity import Activity
from de.thb.content_graph.graph.node.disease import Disease
from de.thb.content_graph.graph.node.node_type import NodeType
from de.thb.content_graph.graph.edge.relation_type import RelationType
from de.thb.content_graph.neo4j.neo4j_access import Neo4jAccess
from de.thb.misc.queryobjects import QueryNode, QueryRelation
from de.thb.misc.util import setup_logging, get_resource

logger = logging.getLogger(__name__)

# made up data
BASE_GRAPH_PATH: str = 'graphs/base.json'
# test data w/out require, preferred
BASE_GRAPH_PATH: str = 'graphs/template_v003_Psymeon 11112024.json'
# test data w/ require, preferred
BASE_GRAPH_PATH: str = 'graphs/template_v004_Psymeon 21112024.json'
# test data w/ durations for activities
BASE_GRAPH_PATH: str = 'graphs/template_v004_Psymeon 23112024.json'
START_NODE_UID: str = 'm_00'
START_NODE_DATA: dict = {KEY_UID: START_NODE_UID, KEY_NAME: 'START', KEY_REQUIRED: []}
START_NODE: QueryNode = QueryNode(START_NODE_UID, NodeType.ACTIVITY, data=START_NODE_DATA)
END_NODE_UID: str = 'm_01'
END_NODE_DATA: dict = {KEY_UID: END_NODE_UID, KEY_NAME: 'END', KEY_REQUIRED: []}
END_NODE: QueryNode = QueryNode(END_NODE_UID, NodeType.ACTIVITY, data=END_NODE_DATA)


def main() -> None:
    with open(get_resource(BASE_GRAPH_PATH), 'r') as f:
        graph_data: dict = json.load(f)
    access: Neo4jAccess = Neo4jAccess.get_access()
    access.delete_all()

    diseases: list[Disease] = [Disease(d[KEY_UID], d[KEY_NAME], d[KEY_ABBRV], d.get(KEY_PREF, []))
                               for d in graph_data[KEY_DISEASES]]
    [access.create_node(d.query_node) for d in diseases]
    diseases_lu: dict[str, Disease] = {d.uid: d for d in diseases}
    disease_uids: list[str] = [d.uid for d in diseases]

    activities: list[Activity] = ([Activity(a[KEY_UID], a[KEY_NAME], a[KEY_DISEASES], a[KEY_MEDIUM], a[KEY_REQUIRED],
                                            duration_min=a[KEY_DURATION_MIN])
                                  for a in graph_data[KEY_ACTIVITIES]] +
                                  [Activity(START_NODE_UID, 'START', disease_uids,  '', [],
                                            duration_min=0),
                                   Activity(END_NODE_UID, 'END', disease_uids, '', [],
                                            duration_min=0)])
    [access.create_node(a.query_node) for a in activities]

    suitable: QueryRelation = QueryRelation('', RelationType.SUITABLE)
    requires: QueryRelation = QueryRelation('', RelationType.REQUIRES)
    activity: Activity
    for activity in activities:
        activity_query: QueryNode = activity.query_node
        [access.create_relation(activity_query, suitable, diseases_lu[d].query_node) for d in activity.diseases]
        [access.create_relation(activity_query, requires, QueryNode(a, NodeType.ACTIVITY)) for a in activity.required]

    disease: Disease
    for disease in diseases:
        pref_path: list[QueryNode] = [QueryNode(s, NodeType.ACTIVITY) for s in disease.preferred]
        preferred: QueryRelation = QueryRelation('', RelationType.PREFERRED, data={KEY_DISEASE: disease.uid})
        [access.create_relation(pref_path[i], preferred, pref_path[i + 1]) for i in range(len(pref_path) - 1)]


if __name__ == '__main__':
    setup_logging()
    main()
