from de.thb.content_graph.graph.activity_sequence import ActivitySequence
from de.thb.content_graph.graph.app.sequence_validator import ValidatorConfig, SequenceValidator
from de.thb.content_graph.graph.node.activity import Activity
from de.thb.content_graph.graph.node.activity_type import ActivityTypeManager, ActivityType


def test_variation() -> None:
    activities: list[Activity] = [
        Activity('a_1', 'Do_Physical_Exercise', ['d'], 'medium', [], 1),
        Activity('a_2', 'Do_Physical_Exercise', ['d'], 'medium', [], 1),
        Activity('a_3', 'Watch_Video', ['d'], 'medium', [], 1)
    ]
    validator_config: ValidatorConfig = ValidatorConfig((2, 2), (10, 30), (3, 3), 2)
    sequence_validator: SequenceValidator = SequenceValidator(activities, validator_config)
    manager: ActivityTypeManager = sequence_validator.manager
    sequence: ActivitySequence = ActivitySequence('s', manager.size)
    [sequence.add_activity(a, manager.get_arr(a.type)) for a in activities]
    assert sequence_validator.has_variation(sequence) == False


def test_repetition() -> None:
    activities: list[Activity] = [
        Activity('a_1', 'Do_Physical_Exercise', ['d'], 'medium', [], 1),
        Activity('a_2', 'Do_Physical_Exercise', ['d'], 'medium', [], 1),
        Activity('a_3', 'Do_Physical_Exercise', ['d'], 'medium', [], 1)
    ]
    validator_config: ValidatorConfig = ValidatorConfig((2, 2), (10, 30), (3, 3), 2)
    sequence_validator: SequenceValidator = SequenceValidator(activities, validator_config)
    manager: ActivityTypeManager = sequence_validator.manager
    sequence: ActivitySequence = ActivitySequence('s', manager.size)
    [sequence.add_activity(a, manager.get_arr(a.type)) for a in activities]
    assert sequence_validator.has_repetition(sequence)