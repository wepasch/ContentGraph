import logging

from de.thb.content_graph.graph.app.wanderer import Wanderer, Choice
from de.thb.content_graph.graph.node.disease import Disease
from de.thb.content_graph.graph.node.node_type import NodeType
from de.thb.content_graph.neo4j.neo4j_access import Neo4jAccess
from de.thb.misc.queryobjects import QueryNode
from de.thb.misc.util import setup_logging

logger = logging.getLogger(__name__)


def main():
    access: Neo4jAccess = Neo4jAccess.get_access()
    diseases: list[Disease] = access.get_nodes_like(QueryNode('', NodeType.DISEASE))
    disease: Disease = diseases[0]
    wander: Wanderer = Wanderer(disease, access)
    print(f'Wander for disease: {disease}')
    choice: Choice = wander.plan()
    while choice.given:
        choice.set_prompt('Choose next activity (*...recommended):')
        print(choice.selection_listing)
        choice_str: str = input('\t?- ')
        print(f'\tchoice: {choice_str}')
        if choice_str.casefold() == 'x':
            print('Exit...')
            exit(0)
        try:
            choice_int: int = int(choice_str)
            chosen_uid: str | None = choice[choice_int]
            if not chosen_uid:
                raise ValueError
        except ValueError:
            print('Error, retry...\n')
            continue
        wander.step(chosen_uid)
        print(f'Taken path: {' -> '.join(wander.path)}')
        choice = wander.plan()


if __name__ == '__main__':
    setup_logging()
    main()
