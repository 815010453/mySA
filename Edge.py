from Vertex import Vertex
import math
"""
Edge Class
----------

由vertex组成的边. 

"""


class Edge():
    # 定义私有变量
    __vertices: 'tuple[Vertex]'  # 节点数组 一个Edge由两个vertex组成
    __id: int  # 边号 keyid
    __coord: 'list[tuple[float]]'  # 坐标[[x1, y1],[x2, y2],...] 单位为m
    __att: dict  # 边属性
    __length: float  # 边长
    __conEdges: 'list[Edge]'  # 相连的边
    __conAngle: 'list[float]'  # 它到相连边的变化角

    def __init__(self, id: int, vertex_A: Vertex, vertex_B: Vertex, coord: 'list[list[float]]' = [], att: dict = {}) -> None:
        self.__vertices = (vertex_A, vertex_B)
        self.__id = id
        self.__coord = coord
        self.__att = att
        self.__length = 0
        self.__conEdges = []
        self.__conAngle = []
        vertex_A.add_conEdge(self)
        vertex_B.add_conEdge(self)
    '''
    为该边添加相邻的边
    '''

    def add_edge(self, edge: 'Edge') -> None:
        if edge != self:
            if edge not in self.__conEdges:
                self.__conEdges.append(edge)
                '''更新角度变化'''
                angle = Edge.calculate_angle(self.__coord, edge.get_coord())
                self.__conAngle.append(angle)
                edge.add_edge(self)

    '''
    这些都是私有变量的设置方法 set(为了安全,只提供部分set方法)与get
    '''

    def get_vertices(self) -> 'list[Vertex]':
        return self.__vertices

    def get_id(self) -> str:
        return self.__id

    def get_coord(self) -> 'list[list[float]]':
        return self.__coord

    def get_att(self) -> dict:
        return self.__att

    def get_conEdge(self) -> 'list[Edge]':
        return self.__conEdges

    def get_conAngle(self) -> 'list[float]':
        return self.__conAngle

    def get_length(self) -> float:
        return self.__length

    def set_id(self, id: str) -> None:
        self.__id = id


    def set_att(self, att: dict = {}) -> None:
        self.__att = att

    def __str__(self) -> str:
        return str(self.__id)

    def __repr__(self) -> str:
        return str(self.__id)

    '''
    静态方法 计算距离
    '''
    @staticmethod
    def calculate_distance(coord1: 'list[float]', coord2: 'list[float]') -> float:
        return ((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)**0.5

    '''
    静态方法 计算角度变化
    '''
    @staticmethod
    def calculate_angle(coord1: 'list[list[float]]', coord2: 'list[list[float]]') -> float:
        length1 = len(coord1)
        length2 = len(coord2)
        # 第一种情况 nodecoord在第一条线的头，第二条线的头
        if abs(coord2[0][0] - coord1[0][0]) < 1e-4 and abs(coord2[0][1] - coord1[0][1]) < 1e-4:
            b = Edge.calculate_distance(coord1[1], coord1[0])
            c = Edge.calculate_distance(coord2[1], coord2[0])
            a = Edge.calculate_distance(coord1[1], coord2[1])
            return (math.pi - math.acos(round((b*b+c*c-a*a) / (2.0*b*c), 10)))

        # 第二种情况 nodecoord在第一条线的头，第二条线的尾巴
        elif abs(coord2[length2-1][0] - coord1[0][0]) < 1e-4 and abs(coord2[length2-1][1] - coord1[0][1]) < 1e-4:
            b = Edge.calculate_distance(coord1[1], coord1[0])
            c = Edge.calculate_distance(coord2[length2-2], coord2[length2-1])
            a = Edge.calculate_distance(coord1[1], coord2[length2-2])
            return (math.pi - math.acos(round((b*b+c*c-a*a) / (2.0*b*c), 10)))

        # 第三种情况 nodecoord在第一条线的尾巴，第二条线的头
        elif abs(coord2[0][0] - coord1[length1-1][0]) < 1e-4 and abs(coord2[0][1] - coord1[length1-1][1]) < 1e-4:
            b = Edge.calculate_distance(coord1[length1-2], coord1[length1-1])
            c = Edge.calculate_distance(coord2[1], coord2[0])
            a = Edge.calculate_distance(coord1[length1-2], coord2[1])
            return (math.pi - math.acos(round((b*b+c*c-a*a) / (2.0*b*c), 10)))

        # 第四种情况 nodecoord在第一条线的尾巴，第二条线的尾巴
        elif abs(coord2[length2-1][0] - coord1[length1-1][0]) < 1e-4 and abs(coord2[length2-1][1] - coord1[length1-1][1]) < 1e-4:
            b = Edge.calculate_distance(coord1[length1-2], coord1[length1-1])
            c = Edge.calculate_distance(coord2[length2-2], coord2[length2-1])
            a = Edge.calculate_distance(coord1[length1-2], coord2[length2-2])
            return (math.pi - math.acos(round((b*b+c*c-a*a) / (2.0*b*c), 10)))

    '''
    静态方法 坐标系3857转4326
    '''
    @staticmethod
    def mercatorTolonlat(coord_merca: 'list[list[float]]') -> 'list[tuple[float]]':
        out = []
        for item in coord_merca:
            x = item[0]/20037508.34*180
            y = item[1]/20037508.34*180
            y = 180.0/math.pi * \
                (2*math.atan(math.exp(y*math.pi/180.0))-math.pi/2)
            out.append((x, y))
        return out
