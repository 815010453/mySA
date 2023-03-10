from GeoVertex import GeoVertex

"""
GeoVertex Class
----------

简单图的地理边类 该边是指两地理点的连线.
记录其坐标 字段等信息 

"""


class GeoEdge:
    __id: int  # 唯一标识符 v_id
    __vertices: tuple  # 组成该边的点
    # 该边的属性 {'fclass': 'highway', 'name': '公路', ...}
    __edgeAttribute: dict

    def __init__(self, e_id: int, vertex_a: GeoVertex, vertex_b: GeoVertex,
                 edge_att: dict = {}) -> None:
        self.__edgeAttribute = edge_att
        self.__id = e_id
        self.__vertices = (vertex_a, vertex_b)

    def get_id(self) -> int:
        return self.__id

    def get_edge_att(self) -> 'dict[str]':
        return self.__edgeAttribute

    def get_vertices(self) -> tuple[GeoVertex]:
        return self.__vertices

    def set_id(self, e_id: int) -> None:
        self.__id = e_id

    def set_att(self, att: 'dict[str]') -> None:
        self.__edgeAttribute = att

    def set_vertices(self, vertices: tuple) -> None:
        self.__vertices = vertices

    def __str__(self) -> str:
        return str(self.__id)

    def __repr__(self) -> str:
        return str(self.__id)
