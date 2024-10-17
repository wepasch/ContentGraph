from de.thb.content_graph.graph.explorer import Explorer
from de.thb.content_graph.graph.node.type import NodeType
from de.thb.content_graph.neo4j.neo4j_access import Neo4jAccess


def main():
    access: Neo4jAccess = Neo4jAccess.get_access()
    diseases: list = access.get_node_uids_of(NodeType.DISEASE)
    d: str
    for d in diseases:
        explorer: Explorer = Explorer(d, access)
        explorer.move()
        print('\n', d)
        p: list[str]
        for p in explorer.paths:
            print('\t', ' -> '.join(p))



if __name__ == '__main__':
    main()
