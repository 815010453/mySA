# -*- coding:utf-8 -*-
"""
GeoVertex Class
----------

简单图的地理节点类 该节点是指两边的交点.

"""


class GeoVertex:
    # 定义私有变量
    __conVertex: 'list[GeoVertex]'  # 相邻点[vertex1, vertex2, ...]
    __id: int  # 唯一标识符 keyid
    __coord: tuple[float]  # 点坐标[x, y] 单位为m
    __nodeAttributes: dict  # 节点属性{'x':12315,'y':21546,...}

    def __init__(self, v_id: int, att: dict = {}, coord: tuple = ()) -> None:
        self.__conVertex = []
        self.__id = v_id
        self.__coord = coord
        self.__nodeAttributes = att

    '''添加相邻的节点'''

    def add_con_vertex(self, vertex: 'GeoVertex') -> None:
        if vertex != self and vertex not in self.__conVertex:
            # 添加相邻点
            self.__conVertex.append(vertex)
            # 再调用一次相邻点添加
            vertex.add_con_vertex(self)

    '''删除相邻的节点'''

    def remove_con_vertex(self, vertex: 'GeoVertex') -> None:
        if vertex in self.__conVertex:
            # 删除相邻点
            self.__conVertex.remove(vertex)
            # 再调用一次相邻点删除
            vertex.remove_con_vertex(self)

    '''
    这些都是私有变量的设置方法 set与get
    '''

    def get_con_vertex(self) -> 'list[GeoVertex]':
        return self.__conVertex

    def get_id(self) -> int:
        return self.__id

    def get_coord(self) -> tuple[float]:
        return self.__coord

    def get_node_att(self) -> dict:
        return self.__nodeAttributes

    def set_con_vertex(self, vertices: 'list[GeoVertex]') -> None:
        self.__conVertex = vertices

    def set_id(self, v_id: int) -> None:
        self.__id = v_id

    def set_coord(self, coord: tuple[float]) -> None:
        self.__coord = coord

    def set_node_att(self, att: dict) -> None:
        self.__nodeAttributes = att

    def __str__(self) -> str:
        return str(self.__id)

    def __repr__(self) -> str:
        return str(self.__id)

    def __eq__(self, other):
        if not isinstance(other, GeoVertex):
            return False
        return other.__id == self.__id
