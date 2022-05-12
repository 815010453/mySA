from GeoVertex import GeoVertex
from GeoEdge import GeoEdge
import numpy as np
import shapefile  # 使用pyshp
from osgeo import osr
import os
import copy

# gdal对应的proj.db在这个文件夹下
os.environ['PROJ_LIB'] = 'D:\\anaconda3\\Lib\\site-packages\\osgeo\\data\\proj'
"""
GeoGraph Class
----------

由GeoVertex组成的简单地理图. 

"""


class GeoGraph:
    # 定义私有变量
    __vertices: 'dict[int]'  # 节点字典 {id1: vertex1, id2: vertex2, ...}
    __edges: 'dict[int]'  # 边字典 {id1: edge1, id2: edge2}
    __id: str  # 图名

    def __init__(self, id: str = '') -> None:
        self.__vertices = {}
        self.__id = id
        self.__edges = {}

    '''检查该图是否合法（简单图）'''

    def check_graph_simple(self) -> bool:
        """检查点是否合法 无重边，无自环"""
        for id in self.__vertices.keys():
            temp_value = self.__vertices[id]
            if id in temp_value.get_conVertex():
                return False
            judge = {}
            for i in temp_value.get_conVertex():
                if i not in judge.keys() and temp_value in i.get_conVertex():
                    judge[i] = 1
                else:
                    return False
        '''检查边是否合法 无重边 无自边'''
        for id in self.__edges.keys():
            temp_value = self.__edges[id]
            v = list(temp_value.get_conEdge().keys())
            con_edge = list(temp_value.get_conEdge().values())
            for item in con_edge:
                if id in item:
                    return False
            for item in v:
                judge = {}
                con_edge = temp_value.get_conEdge()[item]
                for i in con_edge:
                    if i not in judge.keys() and temp_value in i.get_conEdge()[item]:
                        judge[i] = 1
                    else:
                        return False

        return True

    '''
    这些都是私有变量的设置方法 set与get
    '''

    def get_vertices(self) -> dict:
        return self.__vertices

    def get_edges(self) -> dict:
        return self.__edges

    def get_id(self) -> str:
        return self.__id

    def set_id(self, id: str) -> None:
        self.__id = id

    '''添加节点'''

    def add_vertex(self, id: int, geoVertex: GeoVertex) -> None:
        self.__vertices[id] = geoVertex

    '''删除节点'''

    def remove_vertex_v(self, geoVertex: GeoVertex) -> None:
        id = geoVertex.get_id()
        del self.__vertices[id]

    '''图中边的添加与删除'''

    def add_edge(self, vertex_A: GeoVertex, vertex_B: GeoVertex, edge: GeoEdge) -> None:
        # 添加相邻关系
        vertex_A.add_conVertex(vertex_B, edge)
        self.__edges[edge.get_id()] = edge

    def remove_edge(self, vertex_A: GeoVertex, vertex_B: GeoVertex, edge: GeoEdge) -> None:
        vertex_A.remove_conVertex(vertex_B, edge)
        del self.__edges[edge.get_id()]

    '''通过节点id查找节点'''

    def find_vertex(self, id: int) -> GeoVertex:
        return self.__vertices[id]

    '''通过两节点找边'''

    @staticmethod
    def find_edge_v(vertex_1: GeoVertex, vertex_2: GeoVertex) -> GeoEdge:
        con_v = vertex_1.get_conVertex()
        index = con_v.index(vertex_2)
        return vertex_1.get_conEdge()[index]

    '''通过边号找边'''

    def find_edge_id(self, id: int) -> GeoEdge:
        return self.__edges[id]

    '''利用BFS遍历从s到t的最短路径(无权图)'''

    def findpath_BFS(self, s: 'GeoVertex', t: 'GeoVertex') -> 'list[GeoVertex]':
        if s == t:
            return []
        res_path = []  # result
        '''use BFS to find the path'''
        open_list = []  # Queue FIFO
        visited_vertex = {}  # is visited?
        search_vertex = {}  # key is the son node, value is the father node
        for key in self.__vertices.keys():
            visited_vertex[self.__vertices[key]] = False
            search_vertex[self.__vertices[key]] = None
        next_vertex = s
        open_list.append(next_vertex)
        visited_vertex[next_vertex] = True
        while True:
            open_list.remove(next_vertex)
            for v in next_vertex.get_conVertex():
                if not visited_vertex[v]:
                    open_list.append(v)
                    visited_vertex[v] = True
                    # next_vertex is the father geoVertex
                    search_vertex[v] = next_vertex
                if v == t:
                    # find the path
                    res_path.append(t)
                    next_vertex = t
                    while search_vertex[next_vertex] is not None:
                        res_path.append(search_vertex[next_vertex])
                        next_vertex = search_vertex[next_vertex]
                    return res_path[::-1]
            if len(open_list) == 0:
                # failure
                return None
            # get first geoVertex
            next_vertex = open_list[0]

    '''非递归方法查找从s到t的所有路径'''

    @staticmethod
    def findAllPath(s: GeoVertex, t: GeoVertex) -> dict:
        """build stack in order to get all path form s to t"""
        '''initialize'''
        main_stack = []  # main stack
        sub_stack = []  # second stack
        main_stack.append(s)
        next_node_list = []
        for v in s.get_conVertex():
            next_node_list.append(v)
        sub_stack.append(next_node_list)
        temp = sub_stack.pop()
        if len(temp) == 0:
            return {}
        next_node = temp[0]
        main_stack.append(temp.pop(0))
        sub_stack.append(temp)
        count = 0
        all_path = {}  # key is the number of road, value is the path
        next_node_list = []
        for v in next_node.get_conVertex():
            if v not in main_stack:
                next_node_list.append(v)
        sub_stack.append(next_node_list)
        while len(main_stack) != 0:
            if main_stack[-1] == t:
                # find one path and save
                count += 1
                all_path[count] = []
                for v in main_stack:
                    all_path[count].append(v)
                main_stack.pop()
                sub_stack.pop()
            next_node_list = sub_stack.pop()
            if len(next_node_list) != 0:
                next_node = next_node_list[0]
                main_stack.append(next_node_list.pop(0))
                sub_stack.append(next_node_list)
                next_node_list = []
                for v in next_node.get_conVertex():
                    if v not in main_stack:
                        next_node_list.append(v)
                sub_stack.append(next_node_list)
            else:
                main_stack.pop()
        return all_path

    '''利用pyshp画图'''

    def draw_geograph(self, out_path: str = '') -> None:
        # 字段
        for id in self.__vertices.keys():
            if len(self.__vertices[id].get_conVertex()) == 0:
                continue
            fields = list(self.__vertices[id].get_edgeAtt().values())[0].keys()
            break
        print(fields)
        '''
        w = shapefile.Writer(out_path, shapeType=3, encoding='utf-8')
        for i in list(fields):
            if i == 'coord':
                continue
            elif i == 'length':
                w.field(i, 'N', decimal=5)
            else:
                w.field(i, 'C')
        '''
        return None

    def __str__(self) -> str:
        return str(self.__id)

    def __repr__(self) -> str:
        return str(self.__id)

    '''最小变化角构建新的相邻边关系'''

    def construct_Edge_minDeltaAngle(self) -> None:
        key_id = self.get_edges().keys()
        for id in key_id:
            temp_edge = self.get_edges()[id]
            temp_con_edge = temp_edge.get_conEdge()
            print(temp_edge.get_conEdge())
            # 这种环路比较特殊 需要特殊处理
            # if len(temp_con_edge.keys()) == 1:
            [vertex1, vertex2] = temp_con_edge.keys()

            delta_angle = temp_edge.get_deltaAngle()
            # ==0的情况是端点，不做处理
            if len(temp_con_edge[vertex1]) != 0:
                delta_angle_vertex1 = delta_angle[vertex1]
                # 查找变化角最小,且<pi/6的边
                min_angle = min(delta_angle_vertex1)
                if min_angle < np.pi / 6:
                    min_edge = delta_angle_vertex1.index(min_angle)
                    temp_con_edge_vertex1 = [x for x in temp_con_edge[vertex1] if x != min_edge]
                    for i in temp_con_edge_vertex1:
                        temp_edge.remove_conEdge(i, vertex1)
            if len(temp_con_edge[vertex2]) != 0:
                delta_angle_vertex2 = delta_angle[vertex2]
                # 查找变化角最小,且<pi/6的边
                min_angle = min(delta_angle_vertex2)
                if min_angle < np.pi / 6:
                    min_edge = delta_angle_vertex2.index(min_angle)
                    temp_con_edge_vertex2 = [x for x in temp_con_edge[vertex2] if x != min_edge]
                    for i in temp_con_edge_vertex2:
                        temp_edge.remove_conEdge(i, vertex2)

    '''求和'''

    @staticmethod
    def getSumValue(valueStr):
        my_sum = 0.0
        for item in valueStr:
            my_sum = my_sum + item
        return my_sum

    '''求出现次数最多的字符串'''

    @staticmethod
    def getMostTimesValue(valueStr):
        my_hash = dict()
        for item in valueStr:
            if item in my_hash:
                my_hash[item] += 1
            else:
                my_hash[item] = 1

        return max(my_hash, key=my_hash.get)
