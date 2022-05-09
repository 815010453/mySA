import math
"""
GeoVertex Class
----------

简单图的地理节点类 该节点是指两边的交点. 

"""


class GeoVertex():
    # 定义私有变量
    __conVertex: 'list[GeoVertex]'  # 相邻点
    __id: int  # 唯一标识符 keyid
    __coord: 'tuple[float]'  # 点坐标[x, y] 单位为m
    __nodeAttributes: dict  # 节点属性
    # 边属性 {(self, vertex1):{'name':'南京路','fclass':'road',...},(self, vertex2):{'name':'北京路','fclass':'highway',...},...}
    __edgeAttributes: dict
    # 记录相邻边的变化角 {(vertex1, vertex2):float, (vertex2, vertex3): float,...}
    __deltaAngle: dict

    def __init__(self, id: int, att: dict = {}, coord: 'tuple[float]' = []) -> None:
        self.__conVertex = []
        self.__id = id
        self.__coord = coord
        self.__nodeAttributes = att
        self.__edgeAttributes = {}
        self.__deltaAngle = {}

    '''添加相邻的节点'''

    def add_conVertex(self, GeoVertex: 'GeoVertex', edgeDict: dict = {}) -> None:
        if GeoVertex != self:
            if GeoVertex not in self.__conVertex:
                self.__conVertex.append(GeoVertex)
                self.__edgeAttributes[(self, GeoVertex)] = edgeDict
                # 如果当前点相邻的点个数>1 更新相邻变化角字典
                if len(self.__conVertex) > 1:
                    coord2 = edgeDict['coord']
                    for v in self.__conVertex:
                        if v != GeoVertex:
                            tempKey = (v, GeoVertex)
                            edgeKey = self.get_edgeAtt().keys()
                            if (self, v) in edgeKey:
                                coord1 = self.get_edgeAtt()[(self, v)]['coord']
                            else:
                                coord1 = self.get_edgeAtt()[(v, self)]['coord']
                            self.__deltaAngle[tempKey] = GeoVertex.calculate_angle(coord1, coord2)
                GeoVertex.add_conVertex(self, edgeDict)
            
                

    '''删除相邻的节点'''

    def remove_conVertex(self, GeoVertex: 'GeoVertex') -> None:
        if GeoVertex in self.__conVertex:
            self.__conVertex.remove(GeoVertex)
        if (self, GeoVertex) in self.__edgeAttributes.keys():
            del self.__edgeAttributes[(self, GeoVertex)]
        if (GeoVertex, self) in self.__edgeAttributes.keys():
            del self.__edgeAttributes[(GeoVertex, self)]
        if self in GeoVertex.get_conVertex():
            GeoVertex.__conVertex.remove(self)
        if (self, GeoVertex) in GeoVertex.get_edgeAtt().keys():
            del GeoVertex.__edgeAttributes[(self, GeoVertex)]
        if (GeoVertex, self) in GeoVertex.get_edgeAtt().keys():
            del GeoVertex.__edgeAttributes[(GeoVertex, self)]

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

    def get_edgeAtt(self) -> dict:
        return self.__edgeAttributes

    def get_deltaAngle(self) -> dict:
        return self.__deltaAngle

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
            b = GeoVertex.calculate_distance(coord1[1], coord1[0])
            c = GeoVertex.calculate_distance(coord2[1], coord2[0])
            a = GeoVertex.calculate_distance(coord1[1], coord2[1])
            return (math.pi - math.acos(round((b*b+c*c-a*a) / (2.0*b*c), 10)))

        # 第二种情况 nodecoord在第一条线的头，第二条线的尾巴
        elif abs(coord2[length2-1][0] - coord1[0][0]) < 1e-4 and abs(coord2[length2-1][1] - coord1[0][1]) < 1e-4:
            b = GeoVertex.calculate_distance(coord1[1], coord1[0])
            c = GeoVertex.calculate_distance(coord2[length2-2], coord2[length2-1])
            a = GeoVertex.calculate_distance(coord1[1], coord2[length2-2])
            return (math.pi - math.acos(round((b*b+c*c-a*a) / (2.0*b*c), 10)))

        # 第三种情况 nodecoord在第一条线的尾巴，第二条线的头
        elif abs(coord2[0][0] - coord1[length1-1][0]) < 1e-4 and abs(coord2[0][1] - coord1[length1-1][1]) < 1e-4:
            b = GeoVertex.calculate_distance(coord1[length1-2], coord1[length1-1])
            c = GeoVertex.calculate_distance(coord2[1], coord2[0])
            a = GeoVertex.calculate_distance(coord1[length1-2], coord2[1])
            return (math.pi - math.acos(round((b*b+c*c-a*a) / (2.0*b*c), 10)))

        # 第四种情况 nodecoord在第一条线的尾巴，第二条线的尾巴
        elif abs(coord2[length2-1][0] - coord1[length1-1][0]) < 1e-4 and abs(coord2[length2-1][1] - coord1[length1-1][1]) < 1e-4:
            b = GeoVertex.calculate_distance(coord1[length1-2], coord1[length1-1])
            c = GeoVertex.calculate_distance(coord2[length2-2], coord2[length2-1])
            a = GeoVertex.calculate_distance(coord1[length1-2], coord2[length2-2])
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
