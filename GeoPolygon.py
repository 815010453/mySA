from GeoVertex import GeoVertex
from GeoEdge import GeoEdge

"""
GeoVertex Class
----------

简单图的地理面类 该面是指面的边界.
记录其坐标 字段等信息 

"""


class GeoPolygon:
    __id: int
    __edges:list  # 组成该面的边
    # 该面的属性 {'市': '北京市', 'pop': ..., ...}
    __polygonAttribute: dict

    def __init__(self, p_id: int, edges, poly_att=None) -> None:
        if poly_att is None:
            __polygonAttribute = {}
        self.__polygonAttribute = poly_att
        self.__id = p_id
        self.__edges = edges

    def get_id(self) -> int:
        return self.__id

    def get_edge_att(self) -> dict:
        return self.__polygonAttribute

    def get_edges(self) -> list:
        return self.__edges

    def set_id(self, p_id: int) -> None:
        self.__id = p_id

    def set_att(self, att: dict) -> None:
        self.__polygonAttribute = att

    def set_edges(self, edges: list) -> None:
        self.__edges = edges
