from de.thb.content_graph.graph.app.wanderer import Wanderer
from de.thb.content_graph.graph.node.disease import Disease
from de.thb.content_graph.graph.node.type import NodeType
from de.thb.content_graph.neo4j.neo4j_access import Neo4jAccess
from de.thb.misc.queryobjects import QueryNode
from de.thb.misc.util import setup_logging


def main():
    access: Neo4jAccess = Neo4jAccess.get_access()
    diseases: list[Disease] = access.get_nodes_like(QueryNode('', NodeType.DISEASE))
    wander: Wanderer = Wanderer(diseases[0], access)
    wander.run()


if __name__ == '__main__':
    setup_logging()
    main()
