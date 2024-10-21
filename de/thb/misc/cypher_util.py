from de.thb.content_graph.graph.constants import KEY_UID, KEY_REQUIRED
from de.thb.content_graph.graph.node.type import NodeType
from de.thb.misc.queryobjects import QueryNode, QueryRelation, QueryObject

REF_N: str = 'n'
REF_S: str = 's'
REF_D: str = 'd'
REF_R: str = 'r'

REL_DIR: tuple[tuple[str, str,], tuple[str, str,],] = (('-', '->'), ('<-', '-'))


def cypherfy_dict(d: dict[str, str | int | list[str | int]]) -> str:
    k: str
    v: str | int | list[str | int]
    return '{' + ', '.join([f'{k}: {__conv_val(v)}' for k, v in d.items()]) + '}'


def _eval_quobject(obj: QueryObject, ref: str = '') -> str:
    s: str = ''
    if not obj:
        return s
    if ref:
        s += ref
    if obj.label:
        s += f':{obj.label}'
    if obj.uid:
        obj.add_data({KEY_UID: obj.uid})
    if obj.data:
        s += f'{cypherfy_dict(obj.data)}'
    return s


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
    def get_node_like(cls, node: QueryNode, ref: str):
        return f'MATCH ({_eval_quobject(node, ref)}) RETURN {ref}'

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
                            exclude_uids: list[str], ref_name: str, reverse: bool):

        return (f'MATCH ({_eval_quobject(src, ref=ref_name)})'
                f'{REL_DIR[reverse][0]}[{_eval_quobject(rel)}]{REL_DIR[reverse][1]}'
                f'({_eval_quobject(dst)})'
                f'WHERE NOT {ref_name}.{KEY_UID} IN {exclude_uids}'
                f'RETURN {ref_name}, collect(DISTINCT {ref_name})')

    @classmethod
    def get_related_exclude_require(cls, src: QueryNode, rel: QueryRelation | None, dst: QueryNode | None,
                                    exclude_uids: list[str], available_uids: list[str], ref_name: str, reverse: bool):
        rel_str: str = f'[:{rel.label}]' if rel else '[]'
        src_str: str = f'(:{dst.label} {{{KEY_UID}:\'{dst.uid}\'}})' if dst else '()'
        return (f'MATCH ({ref_name}:{src.label}){REL_DIR[reverse][0]}{rel_str}{REL_DIR[reverse][1]}{src_str} '
                f'WHERE NOT {ref_name}.{KEY_UID} IN {exclude_uids} '
                f' AND ALL(req IN {ref_name}.{KEY_REQUIRED} WHERE req IN {available_uids})'
                f'RETURN {ref_name}, collect(DISTINCT {ref_name})')
