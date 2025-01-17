import logging

from config import MAX_NOF_ACTIVITIES, MAX_DURATION, MIN_NOF_ACTIVITIES, \
    MIN_DURATION, LIMIT_TYPE_REPETITION, ACTIVITY_TYPES_PER_WINDOW, WINDOW_SIZE
from de.thb.content_graph.graph.activity_sequence import ActivitySequence
from de.thb.content_graph.graph.app.sequence_validator import SequenceValidator, ValidatorConfig
from de.thb.content_graph.graph.node.activity import Activity
from de.thb.content_graph.graph.node.node_type import NodeType
from de.thb.content_graph.neo_4_j.neo4j_access import Neo4jAccess
from de.thb.content_graph.experimentation import find_sequences
from de.thb.misc.queryobjects import QueryNode
from de.thb.misc.util import setup_logging

EXPORT_PATHS_DIR: str = 'export/paths'

logger = logging.getLogger(__name__)

def main() -> None:
    logger.info(f'Start generating for duration in [{MIN_DURATION}, {MAX_DURATION}], '
                f'path size in [{MIN_NOF_ACTIVITIES}, {MAX_NOF_ACTIVITIES}], '
                f'variety ratio {ACTIVITY_TYPES_PER_WINDOW} | {WINDOW_SIZE} and repetition limit {LIMIT_TYPE_REPETITION}.')
    validator_config: ValidatorConfig = ValidatorConfig((MIN_NOF_ACTIVITIES, MAX_NOF_ACTIVITIES),
                                                        (MIN_DURATION, MAX_DURATION),
                                                        (ACTIVITY_TYPES_PER_WINDOW, WINDOW_SIZE),
                                                        LIMIT_TYPE_REPETITION)
    access: Neo4jAccess = Neo4jAccess.get_access()
    all_activities: list[Activity] = access.get_nodes_like(QueryNode('', NodeType.ACTIVITY))
    activities: list[Activity] = [a for a in all_activities if not a.type.is_meta]
    logger.info(f'Work with {len(activities)} activities.')
    sequence_validator: SequenceValidator = SequenceValidator(activities, validator_config)

    activity_sequences: list[ActivitySequence] = sequence_validator.get_valid_sequences()

    activity_sequences_rec: list[ActivitySequence] = []
    find_sequences(ActivitySequence('A', sequence_validator.manager.size), activities[:], sequence_validator, 0, activity_sequences_rec)

    raise Exception('End of implementations ¯\_(ツ)_/¯')











if __name__ == '__main__':
    setup_logging()
    main()
