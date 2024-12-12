import copy
import logging

from de.thb.content_graph.graph.app.init_graph import START_NODE_UID, END_NODE_UID
from de.thb.content_graph.graph.constants import KEY_DISEASE
from de.thb.content_graph.graph.node.disease import Disease
from de.thb.content_graph.graph.node.node_type import NodeType
from de.thb.content_graph.graph.edge.relation_type import RelationType
from de.thb.content_graph.neo4j.neo4j_access import Neo4jAccess
from de.thb.misc.queryobjects import QueryRelation, QueryNode


MAX_TRIES: int = 3
NOT_SET_INT: int = -1

logger = logging.getLogger(__name__)


def _right_align(num: int, s: str, emph: bool, max_pad: int = 3, new_line: bool = False) -> str:
    num_str: str = str(num)
    num_len: int = len(num_str)
    return f'{(max_pad - (num_len + 1)) * ' '}{'*' if emph else ' '}[{num_str}]{s}{'\n' if new_line else ''}'


class Choice:
    __recommended: str | None = None
    __further_selection: list[str]
    __prompt: str | None

    def __init__(self, recommended: str | None, further_selection: list[str], prompt: str | None = None):
        self.__further_selection = further_selection
        if recommended:
            self.__recommended = recommended
        self.__prompt = prompt

    @property
    def recommended(self) -> str | None:
        return self.__recommended

    @property
    def further_selection(self) -> list[str]:
        return self.__further_selection

    @property
    def prompt(self) -> str | None:
        return self.__prompt

    @property
    def selection_listing(self) -> str:
        selection: str = f'{self.prompt}\n' if self.prompt else ''
        choice_counter: int = 1
        if self.recommended:
            selection += _right_align(choice_counter, f': {self.recommended}', True, max_pad=3, new_line=True)
            choice_counter += 1
        _next: str
        for _next in self.further_selection:
            selection += _right_align(choice_counter, f': {_next}', False, max_pad=3, new_line=True)
            choice_counter += 1
        return selection

    @property
    def given(self) -> bool:
        return not (self.recommended is None and len(self.further_selection) == 0)

    def set_prompt(self, prompt: str) -> None:
        self.__prompt = prompt

    def contains(self, uid: str) -> bool:
        if self.recommended == uid:
            return True
        else:
            return uid in self.further_selection

    def __getitem__(self, item: int) -> str | None:
        if item == 1:
            if self.recommended:
                return self.recommended
            else:
                item += 1
        if item in range(2, len(self.further_selection) + 2):
            return self.further_selection[item - 2]
        else:
            return None

    def __repr__(self) -> str:
        return (f'{self.recommended if self.recommended else ''} | {', '.join(self.further_selection)} '
                f'"{self.prompt if self.prompt else ''}"')


class Wanderer:
    __disease: Disease
    __access: Neo4jAccess
    __path: list[str] = [START_NODE_UID]

    def __init__(self, disease: Disease, access: Neo4jAccess):
        self.__disease = disease
        self.__access = access

    @property
    def path(self) -> list[str]:
        return self.__path

    def plan(self) -> Choice:
        position: str = self.__path[-1]
        if position == END_NODE_UID:
            return Choice(None, [])

        # find all preferred, not only next from position
        all_pref: list[str] = self.__access.get_connected_by(QueryNode('', NodeType.ACTIVITY),
                                                             QueryRelation('', RelationType.PREFERRED,
                                                                           data={KEY_DISEASE: self.__disease.uid}))
        all_avail: list[str] = self.__access.get_related_exclude_require(
            QueryNode(position, NodeType.ACTIVITY), QueryRelation('', RelationType.SUITABLE),
            QueryNode(self.__disease.uid, NodeType.DISEASE), self.__path, self.__path)
        a: str
        pref_next: list[str] = [a for a in all_pref if a in all_avail]
        recommendation: str | None = None if len(pref_next) == 0 else pref_next[0]
        if recommendation:
            all_avail.remove(recommendation)
        if END_NODE_UID in all_avail:
            all_avail.remove(END_NODE_UID)
            all_avail.append(END_NODE_UID)
        selection: list[str] = copy.deepcopy(all_avail)
        return Choice(recommendation, selection, None)

    def step(self, next_uid: str) -> None:
        self.path.append(next_uid)

    def run(self) -> None:
        print(f'\nCurrent path: {' -> '.join(self.__path)}')
        position: str = self.__path[-1]
        if position == END_NODE_UID:
            print('End...')
            return

        # find all preferred, not only next from position
        all_pref: list[str] = self.__access.get_connected_by(QueryNode('', NodeType.ACTIVITY),
                                                             QueryRelation('', RelationType.PREFERRED,
                                                                           data={KEY_DISEASE: self.__disease.uid}))
        all_avail: list[str] = self.__access.get_related_exclude_require(
            QueryNode(position, NodeType.ACTIVITY), QueryRelation('', RelationType.SUITABLE),
            QueryNode(self.__disease.uid, NodeType.DISEASE), self.__path, self.__path)
        a: str
        pref_next: list[str] = [a for a in all_pref if a in all_avail]
        recommendation: str | None = None if len(pref_next) == 0 else pref_next[0]
        misc_next: list[str] = list(set(all_avail) - set(pref_next[:1]))
        if END_NODE_UID in misc_next:
            misc_next.remove(END_NODE_UID)
            misc_next.append(END_NODE_UID)
        selection: list[str] = copy.deepcopy(misc_next)

        choice_counter: int = 1
        print('Choose next activity (*...recommended):')
        if recommendation:
            print(_right_align(choice_counter, f': {recommendation}', True))
            selection.insert(0, recommendation)
            choice_counter += 1
        _next: str
        for _next in misc_next:
            print(_right_align(choice_counter, f': {_next}', False))
            choice_counter += 1

        choice: int = -1
        tries: int = 0
        while choice == NOT_SET_INT:
            choice_str: str = input('\n\t?- ')
            if choice_str.casefold() == 'x':
                print('Exit...')
                exit(0)
            try:
                choice: int = int(choice_str)
                print(f'\tchoice: {choice}')
                if choice < 1 or choice >= choice_counter:
                    raise ValueError
            except ValueError:
                choice = NOT_SET_INT
                print(f'Error - possible choices: {', '.join(map(str, range(1, choice_counter)))}')
                tries += 1
                if tries >= MAX_TRIES:
                    print('Exit...')
                    exit(1)
        next_activity: str = selection[choice - 1]
        print(f'Next activity: {next_activity}')
        self.__path.append(next_activity)
        self.run()










