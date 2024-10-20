from pypher import Pypher

from de.thb.content_graph.graph.constants import KEY_UID, KEY_REQUIRED
from de.thb.content_graph.graph.node.type import NodeType
from de.thb.misc.queryobjects import QueryNode, QueryRelation

REF_N: str = 'n'
REF_S: str = 's'
REF_D: str = 'd'
REF_R: str = 'r'


def cypherfy_dict(d: dict[str, str | int | list[str | int]]) -> str:
    k: str
    v: str | int | list[str | int]
    return '{' + ', '.join([f'{k}: {__conv_val(v)}' for k, v in d.items()]) + '}'


def __conv_val(v: str | int | list[str | int]) -> str:
    if isinstance(v, str) or isinstance(v, int):
        return f"'{v}'"
    elif isinstance(v, list):
        return '[' + ', '.join([__conv_val(v_i) for v_i in v]) + ']'
    else:
        raise TypeError(f'node attribute value {v} is not a string, int or list of those, but {type(v)}')


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


class N4Query:
    @classmethod
    def delete_all_relations(cls) -> (str, dict):
        return 'MATCH ()-[r]->() DELETE r'

    @classmethod
    def delete_all_nodes(cls) -> (str, dict):
        return 'MATCH (n) DELETE n'

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
    def create_node(cls, node: QueryNode) -> str:
        return f'CREATE (:{node.label} {cypherfy_dict(node.data)})'

    @classmethod
    def create_relation(cls, src_uid: str, rel: QueryRelation, dst_uid: str):
        rel_str: str = f'{REF_R}:{rel.label}'
        if rel.data:
            rel_str += cypherfy_dict(rel.data)
        return (f'MATCH ({REF_S}) WHERE ({REF_S}.{KEY_UID}=\'{src_uid}\') MATCH ({REF_D}) WHERE '
                f'({REF_D}.{KEY_UID}=\'{dst_uid}\') CREATE ({REF_S})-[{rel_str}]->({REF_D})')

    @classmethod
    def get_related_exclude(cls, src: QueryNode, rel: QueryRelation | None, dst: QueryNode | None,
                            exclude_uids: list[str], ref_name: str):
        rel_str: str = f'[:{rel.label}]' if rel else '[]'
        src_str: str = f'(:{dst.label} {{{KEY_UID}:\'{dst.uid}\'}})' if dst else '()'
        return (f'MATCH ({ref_name}:{src.label})-{rel_str}->{src_str} '
                f'WHERE NOT {ref_name}.{KEY_UID} IN {exclude_uids} '
                f'RETURN {ref_name}, collect(DISTINCT {ref_name})')

    @classmethod
    def get_related_exclude_require(cls, src: QueryNode, rel: QueryRelation | None, dst: QueryNode | None,
                                    exclude_uids: list[str], available_uids: list[str], ref_name: str):
        rel_str: str = f'[:{rel.label}]' if rel else '[]'
        src_str: str = f'(:{dst.label} {{{KEY_UID}:\'{dst.uid}\'}})' if dst else '()'
        return (f'MATCH ({ref_name}:{src.label})-{rel_str}->{src_str} '
                f'WHERE NOT {ref_name}.{KEY_UID} IN {exclude_uids} '
                f' AND ALL(req IN {ref_name}.{KEY_REQUIRED} WHERE req IN {available_uids})'
                f'RETURN {ref_name}, collect(DISTINCT {ref_name})')

