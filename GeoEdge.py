import math
from GeoVertex import GeoVertex

"""
GeoVertex Class
----------

简单图的地理边类 该边是指两地理点的连线.
记录其坐标 字段等信息 

"""


class GeoEdge():
    # 相邻的边 {v1: [edge1, edge2, ...], v2: [edge3, edge4, ...]}
    __conEdge: 'dict[GeoVertex]'
    __id: int  # 唯一标识符 id
    # 该边的属性 {'fclass': 'highway', 'name': '公路', ...}
    __edgeAttribute: 'dict[str]'
    # 相邻边的变化角 与相邻边对应 {v1: [0.12314, 0.112, ...], v2: [...]}
    __deltaAngle: 'dict[GeoVertex]'
    __coord: 'list[tuple[float]]'  # 该边坐标 [(x1, y1), (x2, y2), ...]

    def __init__(self, id: int, vertex_A: GeoVertex, vertex_B: GeoVertex, coord: 'list[tuple[float]]' = [], edgeAtt: 'dict[str]' = {}) -> None:
        self.__conEdge = {vertex_A:[], vertex_B:[]}
        self.__edgeAttribute = edgeAtt
        self.__deltaAngle = {vertex_A:[], vertex_B:[]}
        self.__coord = coord
        self.__id = id

    '''添加相邻的边'''

    def add_conEdge(self, geoEdge: 'GeoEdge', vertex: GeoVertex) -> None:
        if geoEdge != self:
            if geoEdge not in self.__conEdge[vertex]:
                self.__conEdge[vertex].append(geoEdge)
                # 增加相邻变化角
                self.__deltaAngle[vertex].append(GeoEdge.calculate_angle(
                    self.__coord, geoEdge.get_coord()))
                # 再调用一次
                geoEdge.add_conEdge(self, vertex)
    '''删除相邻的边'''

    def remove_conEdge(self, geoEdge: 'GeoEdge', vertex: GeoVertex) -> None:
        if geoEdge in self.__conEdge[vertex]:
            del self.__deltaAngle[vertex][self.__conEdge[vertex].index(geoEdge)]
            self.__conEdge[vertex].remove(geoEdge)
            # 再调用一次
            geoEdge.remove_conEdge(self, vertex)

    '''这些都是私有变量的设置方法 set与get'''

    def get_conEdge(self) -> 'dict[GeoVertex]':
        return self.__conEdge

    def get_id(self) -> int:
        return self.__id

    def get_edgeAtt(self) -> 'dict[str]':
        return self.__edgeAttribute

    def get_deltaAngle(self) -> 'list[float]':
        return self.__deltaAngle

    def get_coord(self) -> 'list[tuple[float]]':
        return self.__coord

    def set_id(self, id: int) -> None:
        self.__id = id

    def set_coord(self, coord: 'list[tuple[float]]') -> None:
        self.__coord = coord

    def set_att(self, att: 'dict[str]') -> None:
        self.__edgeAttribute = att

    def __str__(self) -> str:
        return str(self.__id)

    def __repr__(self) -> str:
        return str(self.__id)
    
    '''
    静态方法 计算距离
    '''
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
            b = GeoEdge.calculate_distance(coord1[1], coord1[0])
            c = GeoEdge.calculate_distance(coord2[1], coord2[0])
            a = GeoEdge.calculate_distance(coord1[1], coord2[1])
            return (math.pi - math.acos(round((b*b+c*c-a*a) / (2.0*b*c), 10)))

        # 第二种情况 nodecoord在第一条线的头，第二条线的尾巴
        elif abs(coord2[length2-1][0] - coord1[0][0]) < 1e-4 and abs(coord2[length2-1][1] - coord1[0][1]) < 1e-4:
            b = GeoEdge.calculate_distance(coord1[1], coord1[0])
            c = GeoEdge.calculate_distance(
                coord2[length2-2], coord2[length2-1])
            a = GeoEdge.calculate_distance(coord1[1], coord2[length2-2])
            return (math.pi - math.acos(round((b*b+c*c-a*a) / (2.0*b*c), 10)))

        # 第三种情况 nodecoord在第一条线的尾巴，第二条线的头
        elif abs(coord2[0][0] - coord1[length1-1][0]) < 1e-4 and abs(coord2[0][1] - coord1[length1-1][1]) < 1e-4:
            b = GeoEdge.calculate_distance(
                coord1[length1-2], coord1[length1-1])
            c = GeoEdge.calculate_distance(coord2[1], coord2[0])
            a = GeoEdge.calculate_distance(coord1[length1-2], coord2[1])
            return (math.pi - math.acos(round((b*b+c*c-a*a) / (2.0*b*c), 10)))

        # 第四种情况 nodecoord在第一条线的尾巴，第二条线的尾巴
        elif abs(coord2[length2-1][0] - coord1[length1-1][0]) < 1e-4 and abs(coord2[length2-1][1] - coord1[length1-1][1]) < 1e-4:
            b = GeoEdge.calculate_distance(
                coord1[length1-2], coord1[length1-1])
            c = GeoEdge.calculate_distance(
                coord2[length2-2], coord2[length2-1])
            a = GeoEdge.calculate_distance(
                coord1[length1-2], coord2[length2-2])
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


    