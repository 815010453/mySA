"""
Vertex Class
----------

简单图的节点类 该节点是指两边的交点. 

"""


class Vertex():
    # 定义私有变量
    __conVertex: 'list[Vertex]'  # 相连的边
    __id: int  # 唯一标识符 keyid
    __coord: 'tuple[float]'  # 坐标[x, y] 单位为m
    __att: dict  # 节点属性
    __edges: list

    def __init__(self, id: int, att: dict = {}, coord: 'tuple[float]' = []) -> None:
        self.__conVertex = []
        self.__id = id
        self.__coord = coord
        self.__att = att
        self.__edges = []

    '''添加相邻的节点'''

    def add_conVertex(self, vertex: 'Vertex') -> None:
        if vertex != self:
            if vertex not in self.__conVertex:
                self.__conVertex.append(vertex)
            if self not in vertex.get_conVertex():
                vertex.__conVertex.append(self)
    '''添加节点是它的边'''
    def add_conEdge(self, edge) -> None:
        if edge not in self.__edges:
            self.__edges.append(edge)

    '''删除相邻的节点'''

    def remove_conVertex(self, vertex: 'Vertex') -> None:
        if vertex in self.__conVertex:
            self.__conVertex.remove(vertex)
        if self in vertex.get_conVertex():
            vertex.__conVertex.remove(self)
    
    '''删除相邻的边'''
    def remove_conEdge(self, edge)-> None:
        if edge in self.get_edge():
            self.__conVertex.remove(edge)

    '''
    这些都是私有变量的设置方法 set与get
    '''

    def get_conVertex(self) -> 'list[Vertex]':
        return self.__conVertex

    def get_id(self) -> int:
        return self.__id

    def get_coord(self) -> 'tuple[float]':
        return self.__coord

    def get_att(self) -> dict:
        return self.__att

    def get_edge(self) -> list:
        return self.__edges

    def set_id(self, id: int) -> None:
        self.__id = id

    def set_coord(self, coord: tuple) -> None:
        self.__coord = coord

    def set_att(self, att: dict) -> None:
        self.__att = att

    def __str__(self) -> str:
        return str(self.__id)

    def __repr__(self) -> str:
        return str(self.__id)
