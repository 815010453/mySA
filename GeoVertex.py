"""
GeoVertex Class
----------

简单图的地理节点类 该节点是指两边的交点. 

"""


class GeoVertex():
    # 定义私有变量
    __conVertex: 'list[GeoVertex]'  # 相邻点[vertex1, vertex2, ...]
    __id: int  # 唯一标识符 keyid
    __coord: 'tuple[float]'  # 点坐标[x, y] 单位为m
    __nodeAttributes: dict  # 节点属性{'x':12315,'y':21546,...}
    __conEdge: list # 经过它的边 与相邻点对应 [edge1, edge2, ...]

    def __init__(self, id: int, att: dict = {}, coord: 'tuple[float]' = []) -> None:
        self.__conVertex = []
        self.__id = id
        self.__coord = coord
        self.__nodeAttributes = att
        self.__conEdge = []

    '''添加相邻的节点'''

    def add_conVertex(self, geoVertex: 'GeoVertex', geoEdge) -> None:
        # 添加相邻点
        self.__conVertex.append(geoVertex)
        # 添加相邻边
        self.__conEdge.append(geoEdge)
        if len(self.__conEdge) > 1:
            # 添加边的相邻关系
            for e in self.__conEdge:
                geoEdge.add_conEdge(e, self)
        # 再调用一次相邻点添加
        geoVertex.__conVertex.append(self)
        geoVertex.__conEdge.append(geoEdge)
        if len(geoVertex.__conEdge) > 1:
            # 添加边的相邻关系
            for e in geoVertex.__conEdge:
                geoEdge.add_conEdge(e, geoVertex)
            

    '''删除相邻的节点'''

    def remove_conVertex(self, geoVertex: 'GeoVertex', geoEdge) -> None:
        if geoVertex in self.__conVertex:
            # 删除相邻点
            self.__conVertex.remove(geoVertex)
            # 删除相邻边
            self.__conEdge.remove(geoEdge)
            # 再调用一次相邻点删除
            geoVertex.remove_conVertex(self, geoEdge)

    '''
    这些都是私有变量的设置方法 set与get
    '''

    def get_conVertex(self) -> 'list[GeoVertex]':
        return self.__conVertex

    def get_id(self) -> int:
        return self.__id

    def get_coord(self) -> 'tuple[float]':
        return self.__coord

    def get_nodeAtt(self) -> dict:
        return self.__nodeAttributes
    
    def get_conEdge(self) -> list:
        return self.__conEdge

    def set_conVertex(self, vertices: 'list[GeoVertex]') -> None:
        self.__conVertex = vertices

    def set_id(self, id: int) -> None:
        self.__id = id

    def set_coord(self, coord: tuple) -> None:
        self.__coord = coord

    def set_nodeAtt(self, att: dict) -> None:
        self.__nodeAttributes = att

    def __str__(self) -> str:
        return str(self.__id)

    def __repr__(self) -> str:
        return str(self.__id)

    