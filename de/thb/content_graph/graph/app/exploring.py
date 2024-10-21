import logging

from de.thb.content_graph.graph.explorer import Explorer
from de.thb.content_graph.graph.node.disease import Disease
from de.thb.content_graph.graph.node.type import NodeType
from de.thb.content_graph.neo4j.neo4j_access import Neo4jAccess
from de.thb.misc.util import setup_logging

logger = logging.getLogger(__name__)


def main():
    access: Neo4jAccess = Neo4jAccess.get_access()
    diseases: list[Disease] = ['d_01', 'd_02']#access.get_disease({})
    d: str
    for d in diseases:
        explorer: Explorer = Explorer(d, access)
        explorer.run(require=True)
        print('\n', d)
        p: list[str]
        for p in explorer.paths:
            print('\t', ' -> '.join(p))


if __name__ == '__main__':
    setup_logging()
    main()
