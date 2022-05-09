import math
"""
Vertex Class
----------

简单图的节点类 该节点是指两边的交点. 

"""


class Vertex():
    # 定义私有变量
    __conVertex: 'list[Vertex]'  # 相邻点
    __id: int  # 唯一标识符 keyid
    __coord: 'tuple[float]'  # 点坐标[x, y] 单位为m
    __nodeAttributes: dict  # 节点属性
    # 边属性 {(self, vertex1):{'name':'南京路','fclass':'road',...},(self, vertex2):{'name':'北京路','fclass':'highway',...},...}
    __edgeAttributes: dict
    

    def __init__(self, id: int, att: dict = {}, coord: 'tuple[float]' = []) -> None:
        self.__conVertex = []
        self.__id = id
        self.__coord = coord
        self.__nodeAttributes = att
        self.__edgeAttributes = {}

    '''添加相邻的节点'''

    def add_conVertex(self, vertex: 'Vertex', edgeDict: dict = {}) -> None:
        if vertex != self:
            if vertex not in self.__conVertex:
                self.__conVertex.append(vertex)
            if (self, vertex) not in self.__edgeAttributes.keys() and (vertex, self) not in self.__edgeAttributes.keys():
                self.__edgeAttributes[(self, vertex)] = edgeDict
            if self not in vertex.get_conVertex():
                vertex.__conVertex.append(self)
            if (self, vertex) not in vertex.get_edgeAtt().keys() and (vertex, self) not in vertex.get_edgeAtt().keys():
                vertex.__edgeAttributes[(self, vertex)] = edgeDict

    '''删除相邻的节点'''

    def remove_conVertex(self, vertex: 'Vertex') -> None:
        if vertex in self.__conVertex:
            self.__conVertex.remove(vertex)
        if (self, vertex) in self.__edgeAttributes.keys():
            del self.__edgeAttributes[(self, vertex)]
        if (vertex, self) in self.__edgeAttributes.keys():
            del self.__edgeAttributes[(vertex, self)]
        if self in vertex.get_conVertex():
            vertex.__conVertex.remove(self)
        if (self, vertex) in vertex.get_edgeAtt().keys():
            del vertex.__edgeAttributes[(self, vertex)]
        if (vertex, self) in vertex.get_edgeAtt().keys():
            del vertex.__edgeAttributes[(vertex, self)]

    '''
    这些都是私有变量的设置方法 set与get
    '''

    def get_conVertex(self) -> 'list[Vertex]':
        return self.__conVertex

    def get_id(self) -> int:
        return self.__id

    def get_coord(self) -> 'tuple[float]':
        return self.__coord

    def get_nodeAtt(self) -> dict:
        return self.__nodeAttributes

    def get_edgeAtt(self) -> dict:
        return self.__edgeAttributes

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

    @staticmethod
    def calculate_distance(coord1: 'tuple[float]', coord2: 'tuple[float]') -> float:
        return ((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)**0.5
    '''
    静态方法 计算角度变化
    '''
    @staticmethod
    def calculate_angle(coord1: 'list[tuple[float]]', coord2: 'list[tuple[float]]') -> float:
        length1 = len(coord1)
        length2 = len(coord2)
        # 第一种情况 nodecoord在第一条线的头，第二条线的头
        if abs(coord2[0][0] - coord1[0][0]) < 1e-4 and abs(coord2[0][1] - coord1[0][1]) < 1e-4:
            b = Vertex.calculate_distance(coord1[1], coord1[0])
            c = Vertex.calculate_distance(coord2[1], coord2[0])
            a = Vertex.calculate_distance(coord1[1], coord2[1])
            return (math.pi - math.acos(round((b*b+c*c-a*a) / (2.0*b*c), 10)))

        # 第二种情况 nodecoord在第一条线的头，第二条线的尾巴
        elif abs(coord2[length2-1][0] - coord1[0][0]) < 1e-4 and abs(coord2[length2-1][1] - coord1[0][1]) < 1e-4:
            b = Vertex.calculate_distance(coord1[1], coord1[0])
            c = Vertex.calculate_distance(coord2[length2-2], coord2[length2-1])
            a = Vertex.calculate_distance(coord1[1], coord2[length2-2])
            return (math.pi - math.acos(round((b*b+c*c-a*a) / (2.0*b*c), 10)))

        # 第三种情况 nodecoord在第一条线的尾巴，第二条线的头
        elif abs(coord2[0][0] - coord1[length1-1][0]) < 1e-4 and abs(coord2[0][1] - coord1[length1-1][1]) < 1e-4:
            b = Vertex.calculate_distance(coord1[length1-2], coord1[length1-1])
            c = Vertex.calculate_distance(coord2[1], coord2[0])
            a = Vertex.calculate_distance(coord1[length1-2], coord2[1])
            return (math.pi - math.acos(round((b*b+c*c-a*a) / (2.0*b*c), 10)))

        # 第四种情况 nodecoord在第一条线的尾巴，第二条线的尾巴
        elif abs(coord2[length2-1][0] - coord1[length1-1][0]) < 1e-4 and abs(coord2[length2-1][1] - coord1[length1-1][1]) < 1e-4:
            b = Vertex.calculate_distance(coord1[length1-2], coord1[length1-1])
            c = Vertex.calculate_distance(coord2[length2-2], coord2[length2-1])
            a = Vertex.calculate_distance(coord1[length1-2], coord2[length2-2])
            return (math.pi - math.acos(round((b*b+c*c-a*a) / (2.0*b*c), 10)))

    '''
    静态方法 坐标系3857转4326 (x, y)m->(longitude, latitude)°
    '''
    @staticmethod
    def mercatorTolonlat(coord_merca: 'list[tuple[float]]') -> 'list[tuple[float]]':
        out = []
        for item in coord_merca:
            x = item[0]/20037508.34*180
            y = item[1]/20037508.34*180
            y = 180.0/math.pi * \
                (2*math.atan(math.exp(y*math.pi/180.0))-math.pi/2)
            out.append((x, y))
        return out
