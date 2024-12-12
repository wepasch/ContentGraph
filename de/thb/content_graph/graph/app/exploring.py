import json
import logging

from de.thb.content_graph.graph.app.explorer import Explorer
from de.thb.content_graph.graph.contentpath import ContentPath
from de.thb.content_graph.graph.node.content_node import ContentNode
from de.thb.content_graph.graph.node.disease import Disease
from de.thb.content_graph.graph.node.node_type import NodeType
from de.thb.content_graph.neo4j.neo4j_access import Neo4jAccess
from de.thb.misc.queryobjects import QueryNode
from de.thb.misc.util import setup_logging, get_resource

EXPORT_PATHS_DIR: str = 'export/paths'

FILTER_TIME: int = 10
FILTER_LENGTH: int = 3

logger = logging.getLogger(__name__)


def main():
    logger.info(f'Finding paths with filter dur >= {FILTER_TIME}, len >= {FILTER_LENGTH}.')
    access: Neo4jAccess = Neo4jAccess.get_access()
    diseases: list[ContentNode] = access.get_nodes_like(QueryNode('', NodeType.DISEASE))
    disease: Disease
    for disease in diseases:
        if disease.uid == 'd_01':
            pass
        explorer: Explorer = Explorer(disease, access)
        explorer.run(require=True)
        content_paths: list[ContentPath] = list(map(lambda p: ContentPath.with_path(disease, p), explorer.paths))
        file_name: str = f'literal_{disease.uid}_content_paths.txt'
        with open(f'{get_resource(EXPORT_PATHS_DIR)}/{file_name}', 'w') as file:
            file.write('\n'.join(map(lambda p: str(p), content_paths)))

        content_paths_data: list[dict] = [c.json for c in content_paths]
        file_name: str = f'{disease.uid}_content_paths.json'
        with open(f'{get_resource(EXPORT_PATHS_DIR)}/{file_name}', 'w') as file:
            json.dump(content_paths_data, file)

        filtered_content_paths: list[ContentPath] = list(filter(lambda p: p.duration >= FILTER_TIME and
                                                                          p.activities_length >= FILTER_LENGTH,
                                                                content_paths))
        filtered_content_paths_data: list[dict] = [c.json for c in filtered_content_paths]
        file_name: str = f'filtered_{disease.uid}_content_paths.json'
        with open(f'{get_resource(EXPORT_PATHS_DIR)}/{file_name}', 'w') as file:
            json.dump(filtered_content_paths_data, file)
        logger.info(f'Found {len(filtered_content_paths)}/{len(content_paths)} paths for disease {disease.uid}.')


if __name__ == '__main__':
    setup_logging()
    main()
