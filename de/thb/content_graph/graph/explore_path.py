from de.thb.content_graph.graph.app.init_graph import END_NODE_UID
from de.thb.constants import KEY_DISEASE, KEY_ACTIVITIES, KEY_FINISHED, KEY_DURATION_MIN, \
    KEY_TOTAL_LENGTH, KEY_ACT_LENGTH
from de.thb.content_graph.graph.node.activity import Activity
from de.thb.content_graph.graph.node.disease import Disease
from de.thb.content_graph.graph.node.node_type import NodeType
from de.thb.content_graph.neo_4_j.neo4j_access import Neo4jAccess
from de.thb.misc.queryobjects import QueryNode


class ExplorePath:
    __disease: Disease
    __activities: list[Activity]

    def __init__(self, disease: Disease) -> None:
        self.__disease = disease
        self.__activities = []

    @classmethod
    def with_path(cls, disease: Disease, activitiy_uids: list[str]) -> 'ExplorePath':
        content_path: ExplorePath = ExplorePath(disease)
        access: Neo4jAccess = Neo4jAccess.get_access()
        u: str
        for u in activitiy_uids:
            found_activities: list[Activity] = access.get_nodes_like(QueryNode(u, NodeType.ACTIVITY))
            nof_found_activities: int = len(found_activities)
            match nof_found_activities:
                case 0:
                    raise ValueError(f'Found no activitiy for uid {u}.')
                case 1:
                    content_path.add_activity(found_activities[0])
                case _:
                    raise ValueError(f'Found more than 1 activity ({nof_found_activities}) for uid {u}.')
        return content_path

    @property
    def disease(self) -> Disease:
        return self.__disease

    @property
    def activities(self) -> list[Activity]:
        return self.__activities

    @property
    def length(self) -> int:
        return len(self.__activities)

    @property
    def activities_length(self) -> int:
        return len(list(filter(lambda a: a.uid.startswith('a'), self.activities)))

    @property
    def duration(self) -> int:
        duration: int = 0
        a: Activity
        for a in self.activities:
            duration += a.duration if a.duration is not None else 0
        return duration

    @property
    def finished(self) -> bool:
        return len(self.__activities) > 0 and self.activities[-1].uid == END_NODE_UID

    @property
    def json(self) -> dict:
        return {
            KEY_ACTIVITIES: [a.uid for a in self.activities],
            KEY_DISEASE: self.disease.uid,
            KEY_DURATION_MIN: self.duration,
            KEY_ACT_LENGTH: self.activities_length,
            KEY_TOTAL_LENGTH: self.length,
            KEY_FINISHED: self.finished,
        }

    def add_activity(self, activity: Activity) -> None:
        self.activities.append(activity)

    def add_activities(self, activities: list[Activity]) -> None:
        self.activities.extend(activities)

    def __str__(self) -> str:
        return (f'{self.duration} min with {self.activities_length} activities for \'{self.disease.name}\''
                f'{' -> '.join(map(lambda a: f'\'{a.name}\'', self.activities))}')

    def __repr__(self) -> str:
        return (f'{self.duration} min, {self.activities_length} activities: {self.disease.uid} '
                f'{' > '.join(map(lambda a: a.uid, self.activities))}')

