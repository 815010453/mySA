"""
GeoVertex Class
----------

简单图的地理节点类 该节点是指两边的交点. 

"""


class GeoVertex:
    # 定义私有变量
    __conVertex: 'list[GeoVertex]'  # 相邻点[vertex1, vertex2, ...]
    __id: int  # 唯一标识符 keyid
    __coord: 'list[float]'  # 点坐标[x, y] 单位为m
    __nodeAttributes: dict  # 节点属性{'x':12315,'y':21546,...}
    __conEdge: list  # 经过它的边 与相邻点对应 [edge1, edge2, ...]

    def __init__(self, v_id: int, att: dict = {}, coord: 'list[float]'  = []) -> None:
        self.__conVertex = []
        self.__id = v_id
        self.__coord = coord
        self.__nodeAttributes = att
        self.__conEdge = []

    '''添加相邻的节点'''

    def add_con_vertex(self, vertex: 'GeoVertex', geo_edge) -> None:
        if vertex != self and vertex not in self.__conVertex:
            # 添加相邻点
            self.__conVertex.append(vertex)
        if geo_edge not in self.__conEdge:
            # 添加相邻边
            self.__conEdge.append(geo_edge)
        if self.__conEdge:
            # 添加边的相邻关系
            for e in self.__conEdge:
                geo_edge.add_con_edge(e, self)
        # 再调用一次相邻点添加
        if vertex != self and self not in vertex.__conVertex:
            vertex.__conVertex.append(self)
        if geo_edge not in vertex.__conEdge:
            vertex.__conEdge.append(geo_edge)
        if vertex.__conEdge:
            # 添加边的相邻关系
            for e in vertex.__conEdge:
                geo_edge.add_con_edge(e, vertex)

    '''删除相邻的节点'''

    def remove_con_vertex(self, vertex: 'GeoVertex', edge) -> None:
        if vertex in self.__conVertex:
            # 删除相邻点
            self.__conVertex.remove(vertex)
        if edge in self.__conEdge:
            # 删除相邻边
            self.__conEdge.remove(edge)
        if self.__conEdge:
            # 删除边的相邻关系
            for e in self.__conEdge:
                edge.remove_con_edge(e, self)
        # 再调用一次相邻点删除
        if self in vertex.__conVertex:
            vertex.__conVertex.remove(self)
        if edge in vertex.__conEdge:
            vertex.__conEdge.remove(edge)
        if vertex.__conEdge:
            # 删除边的相邻关系
            for e in vertex.__conEdge:
                edge.remove_con_edge(e, vertex)


    '''
    这些都是私有变量的设置方法 set与get
    '''

    def get_con_vertex(self) -> 'list[GeoVertex]':
        return self.__conVertex

    def get_id(self) -> int:
        return self.__id

    def get_coord(self) -> 'list[float]':
        return self.__coord

    def get_node_att(self) -> dict:
        return self.__nodeAttributes

    def get_con_edge(self) -> list:
        return self.__conEdge

    def set_con_vertex(self, vertices: 'list[GeoVertex]') -> None:
        self.__conVertex = vertices

    def set_id(self, id: int) -> None:
        self.__id = id

    def set_coord(self, coord: 'list[float]') -> None:
        self.__coord = coord

    def set_node_att(self, att: dict) -> None:
        self.__nodeAttributes = att

    def __str__(self) -> str:
        return str(self.__id)

    def __repr__(self) -> str:
        return str(self.__id)
