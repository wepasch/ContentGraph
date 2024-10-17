from cymple.builder import QueryBuilder
from pypher import Pypher

from de.thb.content_graph.graph.constants import KEY_UID
from de.thb.content_graph.graph.node.type import NodeType, RelationType

EQUALS: str = '='


def to_cypher_attrs(data: dict[str: str | list[str] | int]) -> str:
    if not data:
        return ''
    data_str: str = ''
    k: str
    v: str
    for k, v in data.items():
        if not isinstance(k, str):
            raise TypeError(f'Unexpected type for string key: {type(v)}')
        if isinstance(v, str) or isinstance(v, int):
            v_str = f'\'{str(v)}\''
        elif isinstance(v, list) and (len(v) == 0 or isinstance(v[0], str)):
            v_str = str(v)
        else:
            raise TypeError(f'Unexpected type for value, must be str, list[str], int but was {type(v)}')
        data_str += f'{k}: {v_str}, '
    return '{' + data_str[:-2] + '}'


class Query:
    @classmethod
    def get_match_node(cls, node_type: NodeType | None, data: dict, ref_name: str) -> (str, dict):
        if not node_type:
            return 'MATCH(n)RETURN n', {}
        q: Pypher = Pypher()
        q.Match.node(ref_name, labels=node_type.label)
        where_clauses: list[str] = []
        for k, v in data.items():
            where_clauses.append(f'{ref_name}.{k} = ${k}')
        if where_clauses:
            q.WHERE(' AND '.join(where_clauses))
        q.RETURN(ref_name)
        params = {k: v for k, v in data.items()}
        return str(q), params

    @classmethod
    def get_create_node(cls, node_type: NodeType, data: dict, ref_name: str) -> (str, dict):
        query = Pypher()
        query.CREATE.node(ref_name, labels=node_type.label)
        for k, v in data.items():
            query.SET(f'{ref_name}.{k} = ${k}')
        query.RETURN(ref_name)
        params = {k: v for k, v in data.items()}
        return str(query), params

    @classmethod
    def create_relation(cls, src_uid: str, relation_type: RelationType, dst_uid: str):
        req = f'MATCH(s)WHERE(s.uid=\'{src_uid}\') MATCH(d)WHERE(d.uid=\'{dst_uid}\')CREATE(s)-[r:{relation_type.label}]->(d)'
        return req
        query = Pypher()
        query.MATCH.node('s', uid='$src_uid')
        query.MATCH.node('d', uid='$dst_uid')
        query.CREATE(f'(s)-[r:{relation_type.label}]->(d)')
        params = {'src_uid': src_uid, 'dst_uid': dst_uid}
        return str(query), params

    @classmethod
    def get_related_without(cls, src_type: NodeType, rel_type: RelationType, dst_node_type: NodeType, dst_uid: str,
                            exclude_uids: list[str], ref_name: str, reverse: bool) -> (str, dict):
        if reverse:
            return (f'MATCH ({ref_name}:{src_type.label})<-[:{rel_type.label}]-(:{dst_node_type.label} {{{KEY_UID}:'
                    f'\'{dst_uid}\'}}) WHERE NOT {ref_name}.{KEY_UID} IN {exclude_uids} RETURN {ref_name}'), {}
        else:
            return (f'MATCH ({ref_name}:{src_type.label})-[:{rel_type.label}]->(:{dst_node_type.label} {{{KEY_UID}:'
                    f'\'{dst_uid}\'}}) WHERE NOT {ref_name}.{KEY_UID} IN {exclude_uids} RETURN {ref_name}'), {}


    @classmethod
    def get_from_by(cls, ):
        pass