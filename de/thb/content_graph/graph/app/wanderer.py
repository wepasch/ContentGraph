import copy

from de.thb.content_graph.graph.app.init_graph import START_NODE_UID, END_NODE_UID
from de.thb.content_graph.graph.constants import KEY_DISEASE
from de.thb.content_graph.graph.node.disease import Disease
from de.thb.content_graph.graph.node.type import RelationType, NodeType
from de.thb.content_graph.neo4j.neo4j_access import Neo4jAccess
from de.thb.misc.queryobjects import QueryRelation, QueryNode


MAX_TRIES: int = 3
NOT_SET_INT: int = -1


def _meh(num: int, s: str, emph: bool, max_pad: int = 3) -> str:
    num_str: str = str(num)
    num_len: int = len(num_str)
    return f'{(max_pad - (num_len + 1)) * ' '}{'*' if emph else ' '}[{num_str}]{s}'


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

    def run(self) -> None:
        print(f'\nCurrent path: {' -> '.join(self.__path)}' )
        position: str = self.__path[-1]
        if position == END_NODE_UID:
            print('End...')
            return

        all_pref: list[str] = self.__access.get_connected_by(QueryNode(position, NodeType.ACTIVITY),
                                                              QueryRelation('', RelationType.PREFERRED,
                                                                            data={KEY_DISEASE: self.__disease.uid}))
        all_avail: list[str] = self.__access.get_related_exclude_require(
            QueryNode(position, NodeType.ACTIVITY), QueryRelation('', RelationType.SUITABLE),
            QueryNode(self.__disease.uid, NodeType.DISEASE), self.__path, self.__path)
        pref_next: list[str] = list(filter(lambda a: a in all_avail, all_pref))
        recom_next: str | None = None if len(pref_next) == 0 else pref_next[0]
        misc_next: list[str] = list(set(all_avail) - set(pref_next[:1]))
        if END_NODE_UID in misc_next:
            misc_next.remove(END_NODE_UID)
            misc_next.append(END_NODE_UID)
        selection: list[str] = copy.deepcopy(misc_next)

        choice_counter: int = 1
        print('Choose next activity (*...recommended):')
        if recom_next:
            print(_meh(choice_counter, f': {recom_next}', True))
            selection.insert(0, recom_next)
            choice_counter += 1
        _next: str
        for _next in misc_next:
            print(_meh(choice_counter, f': {_next}', False))
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






