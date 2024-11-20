import logging

from de.thb.content_graph.graph.app.explorer import Explorer
from de.thb.content_graph.graph.node.content_node import ContentNode
from de.thb.content_graph.graph.node.disease import Disease
from de.thb.content_graph.graph.node.type import NodeType
from de.thb.content_graph.neo4j.neo4j_access import Neo4jAccess
from de.thb.misc.queryobjects import QueryNode
from de.thb.misc.util import setup_logging

logger = logging.getLogger(__name__)


def main():
    access: Neo4jAccess = Neo4jAccess.get_access()
    diseases: list[ContentNode] = access.get_nodes_like(QueryNode('', NodeType.DISEASE))
    print('Possible paths for ')
    disease: Disease
    for disease in diseases:
        explorer: Explorer = Explorer(disease, access)
        explorer.run(require=True)
        print(f'\n\t{disease.name}, {disease.uid}')
        p: list[str]
        for p in explorer.paths:
            print('\t\t', ' -> '.join(p))


if __name__ == '__main__':
    setup_logging()
    main()
