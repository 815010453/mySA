# -*- coding:utf-8 -*-
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
    __vertices: list  # 组成该面的点
    # 该面的属性 {'市': '北京市', 'pop': ..., ...}
    __polygonAttribute: dict
    __conGeoPoly: list
    __parts: list

    def __init__(self, p_id: int, parts, vertices: list[GeoEdge], poly_att=None) -> None:
        self.__polygonAttribute = poly_att
        self.__id = p_id
        self.__vertices = vertices
        self.__conGeoPoly = []
        self.__parts = parts

    '''添加相邻的节点'''

    def add_con_polygon(self, polygon: 'GeoPolygon') -> None:
        if polygon != self and polygon not in self.__conGeoPoly:
            # 添加相邻点
            self.__conGeoPoly.append(polygon)
            # 再调用一次相邻点添加
            polygon.add_con_polygon(self)

    '''删除相邻的节点'''

    def remove_con_polygon(self, polygon: 'GeoPolygon') -> None:
        if polygon in self.__conGeoPoly:
            # 删除相邻点
            self.__conGeoPoly.remove(polygon)
            # 再调用一次相邻点删除
            polygon.remove_con_polygon(self)

    def get_id(self) -> int:
        return self.__id

    def get_poly_att(self) -> dict:
        return self.__polygonAttribute

    def get_vertices(self) -> list:
        return self.__vertices

    def get_con_polygon(self) -> list:
        return self.__conGeoPoly

    def get_parts(self) -> list:
        return self.__parts

    def set_id(self, p_id: int) -> None:
        self.__id = p_id

    def set_att(self, att: dict) -> None:
        self.__polygonAttribute = att

    def __str__(self) -> str:
        return str(self.__id)

    def __repr__(self) -> str:
        return str(self.__id)

    def __eq__(self, other):
        if not isinstance(other, GeoPolygon):
            return False
        return other.__id == self.__id
