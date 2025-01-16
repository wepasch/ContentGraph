import json
import random

from de.thb.content_graph.graph.app.init_graph import add_types
from de.thb.constants import KEY_DURATION, KEY_UID, KEY_NAME, KEY_DISEASES, KEY_MEDIUM, KEY_REQUIRED
from de.thb.content_graph.graph.edge.relation_type import RelationType
from de.thb.content_graph.graph.node.activity import Activity
from de.thb.content_graph.graph.node.activity_type import ActivityType
from de.thb.content_graph.neo_4_j.neo4j_access import Neo4jAccess
from de.thb.misc.queryobjects import QueryNode, QueryRelation

BLANK_ACTIVITIES_PATH: str = '/resources/graphs/blank_activities_v005.json'


def get_activities_from(path: str = None) -> list[Activity]:
    if path is None:
        path: str = BLANK_ACTIVITIES_PATH
    activity_data: list[dict] = create_activity(path)
    return [activity_from_json(a) for a in activity_data]

def activity_from_json(data: dict) -> Activity:
    return Activity(data[KEY_UID], data[KEY_NAME], data[KEY_DISEASES], data[KEY_MEDIUM],
                    data[KEY_REQUIRED], data[KEY_DURATION])

def create_activity(path: str = None) -> list[dict]:
    types: list[ActivityType] = [ActivityType.AUDIO, ActivityType.VIDEO, ActivityType.PHYSICAL, ActivityType.USER_INPUT,
                                 ActivityType.OTHER]
    data: list[dict] = []
    for i in range(1, 121):
        data.append({
            KEY_NAME: f'Activity {i}',
            KEY_MEDIUM: types[i%len(types)].label,
            KEY_DURATION: random.randint(3,10),
            KEY_UID: f'a_{i}',
            KEY_REQUIRED: [],
            KEY_DISEASES: []
        })
    if path is not None:
        with open(path, 'w') as file:
            json.dump(data, file)
    return data

def fill_db(activities_data: list[dict]) -> None:
    access: Neo4jAccess = Neo4jAccess.get_access()
    access.delete_all()
    type_nodes: dict[str, QueryNode] = add_types(access, activities_data)
    activities: list[Activity] = [Activity(a[KEY_UID], a[KEY_NAME], a[KEY_DISEASES], a[KEY_MEDIUM], a[KEY_REQUIRED],
                                           duration_min=a[KEY_DURATION]) for a in activities_data]
    is_a: QueryRelation = QueryRelation('', RelationType.IS_A)
    for a in activities:
        query_node: QueryNode = a.query_node
        access.create_node(query_node)
        access.create_relation(query_node, is_a, type_nodes[a.type.label])
