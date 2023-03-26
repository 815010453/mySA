# -*- coding:utf-8 -*-
import datetime
import numpy as np
from GeoVertex import GeoVertex
from GeoEdge import GeoEdge
from GeoPolygon import GeoPolygon
import shapefile  # 使用pyshp
from osgeo import osr
import os
import math
import random

"""
GeoGraph Class
----------

由GeoVertex组成的简单地理图. 

"""


class GeoGraph:
    # 定义私有变量
    __vertices_id: dict[int]  # 点号对应的节点字典 {id1: vertex1, id2: vertex2, ...}
    __edges_id: dict[int]  # 边号对应的边字典 {id1: edge1, id2: edge2}
    __vertices_edge: dict[tuple]  # 点号对应的边号字典 {(vertex1, vertex2): edge1, (vertex3, vertex4): edge2,...}
    __name: str  # 图名
    __vertexCoord: dict  # 点的坐标对应的点号
    __polygon_id: dict[int]  # 多边形号对应的多边形
    __vertex_polygon: dict  # 点对应的多边形

    def __init__(self, g_id: str = '') -> None:
        self.__vertices_id = {}
        self.__name = g_id
        self.__edges_id = {}
        self.__vertices_edge = {}
        self.__vertexCoord = {}
        self.__polygon_id = {}
        self.__vertex_polygon = {}

    # 通过边文件路径名以及图名构建该图
    def constructGraph_edge(self, edge_path) -> None:
        """所有的点构成一张图"""
        '''开始构建图'''
        '''读取边的shapefile文件'''
        '''构建点与点之间的相邻关系以及构建边'''
        with shapefile.Reader(edge_path, encoding='utf-8') as edgeFile:
            # 读取属性
            all_records = edgeFile.records()
            key_list = []  # 字段名
            for i in edgeFile.fields:
                key_list.append(i[0])
            print(key_list)
            # 不需要第0个字段名
            del key_list[0]
            count = 1
            count_edge = 1
            # 读取坐标
            all_points = edgeFile.shapes()
            for item, shape in zip(all_records, all_points):
                # 创建边
                # 将key和对应的value打包成一个字典
                temp_dict = dict(zip(key_list, item))
                if count % 100000 == 0:
                    print(temp_dict)
                preVertex = None
                for point in shape.points:
                    # 如果节点已经在图中了，则去找它
                    if point in self.__vertexCoord.keys():
                        # 如果前置节点不存在，则查找前置节点
                        if preVertex is None:
                            preVertex = self.__vertices_id[self.__vertexCoord[point]]
                            continue
                        # 否则查找现在的节点
                        nowVertex = self.__vertices_id[self.__vertexCoord[point]]
                    # 否则节点不在图中
                    else:
                        # 如果前置节点不存在，则创建前置节点
                        if preVertex is None:
                            # 创建节点
                            preVertex = GeoVertex(count, {}, point)
                            count += 1
                            continue
                        # 否则创建现在的节点
                        nowVertex = GeoVertex(count, {}, point)
                        count += 1
                    # 通过前置节点和现在的节点构建该边
                    nowEdge = GeoEdge(e_id=count_edge, edge_att=temp_dict, vertex_a=preVertex, vertex_b=nowVertex)
                    # 在图中添加该边
                    self.add_edge(nowEdge)
                    count_edge += 1
                    preVertex = nowVertex
        '''if self.check_graph_simple():
            print('Constructing graph succeed!')
            print('The count of vertices is ' + str(len(list(self.__vertices_id.keys()))))
            print('The count of edges is ' + str(len(list(self.__edges_id.keys()))))'''

    # 通过面文件路径名以及图面构建该图

    def constructGraph_polygon(self, polygon_path) -> None:
        with shapefile.Reader(polygon_path, encoding='utf-8') as edgeFile:
            # 读取属性
            all_records = edgeFile.records()
            key_list = []  # 字段名
            for i in edgeFile.fields:
                key_list.append(i[0])
            print(key_list)
            # 不需要第0个字段名
            del key_list[0]
            count = 1
            count_edge = 1
            # 读取坐标
            all_points = edgeFile.shapes()
            polygon_id = 0
            for item, shape in zip(all_records, all_points):
                # 创建边
                # 将key和对应的value打包成一个字典
                temp_dict = dict(zip(key_list, item))
                if count % 100000 == 0:
                    print(temp_dict)
                preVertex = None
                polygon_id += 1
                vertices = []
                for point in shape.points:
                    # 如果节点已经在图中了，则去找它
                    if point in self.__vertexCoord.keys():
                        # 如果前置节点不存在，则查找前置节点
                        if preVertex is None:
                            preVertex = self.__vertices_id[self.__vertexCoord[point]]
                            vertices.append(preVertex)
                            continue
                        # 否则查找现在的节点
                        nowVertex = self.__vertices_id[self.__vertexCoord[point]]
                    # 否则节点不在图中
                    else:
                        # 如果前置节点不存在，则创建前置节点
                        if preVertex is None:
                            # 创建节点
                            preVertex = GeoVertex(count, {}, point)
                            vertices.append(preVertex)
                            count += 1
                            continue
                        # 否则创建现在的节点
                        nowVertex = GeoVertex(count, {}, point)
                        count += 1
                    vertices.append(nowVertex)
                    nowEdge_id = self.find_edge_vertices(preVertex, nowVertex)
                    if nowEdge_id is None:
                        # 通过前置节点和现在的节点构建该边
                        nowEdge = GeoEdge(e_id=count_edge, edge_att={}, vertex_a=preVertex, vertex_b=nowVertex)
                        # 在图中添加该边
                        self.add_edge(nowEdge)
                        count_edge += 1
                    preVertex = nowVertex
                geopolygon = GeoPolygon(polygon_id, vertices, temp_dict)
                self.add_polygon(geopolygon)
        for p_id, polygon in self.__polygon_id.items():
            print(polygon.get_poly_att()['市'], [i.get_poly_att()['市'] for i in polygon.get_con_polygon()])
        '''if self.check_graph_simple():
            print('Constructing graph succeed!')
            print('The count of vertices is ' + str(len(list(self.__vertices_id.keys()))))
            print('The count of edges is ' + str(len(list(self.__edges_id.keys()))))'''

    '''检查该图是否合法（简单图）'''

    def check_graph_simple(self) -> bool:
        """检查点是否合法 无重边，无自环"""
        for vertices_id, temp_edge_id in self.__vertices_edge.items():
            vertices = []
            for id in vertices_id:
                vertices.append(self.__vertices_id[id])
            if len(vertices_id) != 2:
                print('edge error 1: The edge ' + str(temp_edge_id) + ' is not constructed by 2 vertices')
                return False
            if vertices[0] not in vertices[1].get_con_vertex() or vertices[1] not in vertices[0].get_con_vertex():
                print('vertex error 1: The vertices ' + str(vertices_id[0]) + ' and ' + str(
                    vertices_id[1]) + ' is non-adjacent')
                print(vertices[0].get_con_vertex())
                print(vertices[1].get_con_vertex())
                return False
        return True

    '''
    这些都是私有变量的设置方法 set与get
    '''

    def get_vertices(self) -> dict:
        return self.__vertices_id

    def get_edges(self) -> dict:
        return self.__edges_id

    def get_id(self) -> str:
        return self.__name

    def set_id(self, g_id: str) -> None:
        self.__name = g_id

    '''添加节点'''

    def add_vertex(self, geo_vertex: GeoVertex) -> None:
        self.__vertices_id[geo_vertex.get_id()] = geo_vertex
        self.__vertexCoord[geo_vertex.get_coord()] = geo_vertex.get_id()

    '''删除节点'''

    def remove_vertex_v(self, geo_vertex: GeoVertex) -> None:
        v_id = geo_vertex.get_id()
        del self.__vertices_id[v_id]
        conVertices = geo_vertex.get_con_vertex()
        for vertex in conVertices:
            edge_id = self.find_edge_vertices(vertex, geo_vertex)
            vertices_id = []
            vertices = self.__edges_id[edge_id].get_vertices()
            for v in vertices:
                vertices_id.append(v.get_id())
            vertices_id = tuple(vertices_id)
            del self.__vertices_edge[vertices_id]
            del self.__vertices_edge[(vertices_id[1], vertices_id[0])]
            del self.__edges_id[edge_id]

    '''添加边'''

    def add_edge(self, edge: GeoEdge) -> None:
        vertices = edge.get_vertices()
        # 先在图中添加点
        for i in vertices:
            self.add_vertex(i)
        vertices_id = tuple([i.get_id() for i in vertices])
        self.__edges_id[edge.get_id()] = edge
        self.__vertices_edge[vertices_id] = edge.get_id()
        self.__vertices_edge[(vertices_id[1], vertices_id[0])] = edge.get_id()
        vertices[0].add_con_vertex(vertices[1])

    '''删除边'''

    def remove_edge(self, edge: GeoEdge) -> None:
        vertices = edge.get_vertices()
        vertices_id = tuple([i.get_id() for i in vertices])
        del self.__edges_id[edge.get_id()]
        # 删除相邻关系
        vertices[0].remove_con_vertex(vertices[1])
        del self.__vertices_edge[vertices_id]
        del self.__vertices_edge[(vertices_id[1], vertices_id[0])]

    '''添加多边形'''

    def add_polygon(self, polygon: GeoPolygon) -> None:
        vertices: list[GeoVertex] = polygon.get_vertices()
        self.__polygon_id[polygon.get_id()] = polygon
        for v in vertices:
            v_id = v.get_id()
            if v_id not in self.__vertex_polygon.keys():
                self.__vertex_polygon[v_id] = [polygon]
            else:
                con_polygon = self.__vertex_polygon[v_id]
                for p in con_polygon:
                    polygon.add_con_polygon(p)
                self.__vertex_polygon[v_id].append(polygon)

    '''通过节点id查找节点'''

    def find_vertex_id(self, v_id: int) -> GeoVertex:
        return self.__vertices_id[v_id]

    '''通过两节点找边'''

    def find_edge_vertices(self, vertex1: GeoVertex, vertex2: GeoVertex) -> int:
        vertices_id1 = (vertex1.get_id(), vertex2.get_id())
        vertices_id2 = (vertex2.get_id(), vertex1.get_id())
        if vertices_id1 in self.__vertices_edge.keys():
            return self.__vertices_edge[vertices_id1]
        if vertices_id2 in self.__vertices_edge.keys():
            return self.__vertices_edge[vertices_id2]

    '''通过边号找边'''

    def find_edge_id(self, e_id: int) -> GeoEdge:
        return self.__edges_id[e_id]

    '''通过多边形号找多边形'''

    def find_polygon_id(self, p_id: int) -> GeoPolygon:
        return self.__polygon_id[p_id]

    '''断开相邻点的连接(新增了点号)'''

    def disconnect_vertex(self, vertex: GeoVertex, vertices: list, new_id: int, subVertex: dict,
                          auxVertex: dict) -> int:
        """subVertex: {v_id1: [new_id1, new_id2, ...], v_id2: [new_id3, ....]} 父节点对应分裂出的点号集合
            auxVertex: {new_id1: v_id1, new_id2: v_id2 } 分裂出的点号对应的父节点
        """
        newVertex = GeoVertex(new_id, vertex.get_node_att(), vertex.get_coord())
        self.__vertices_id[new_id] = newVertex
        if vertex.get_id() not in auxVertex.keys():
            auxVertex[new_id] = vertex.get_id()
            subVertex[vertex.get_id()] = [new_id]
        else:
            auxVertex[new_id] = auxVertex[vertex.get_id()]
            subVertex[auxVertex[new_id]].append(new_id)
        # 删除相邻关系，添加新相邻关系
        for v in vertices:
            vertex.remove_con_vertex(v)
            newVertex.add_con_vertex(v)
        new_id += 1
        return new_id

    '''合并两个点'''

    @staticmethod
    def connect_vertex(vertex1: GeoVertex, vertex2: GeoVertex) -> None:
        conVertex_b = [i for i in vertex2.get_con_vertex()]
        for vertex in conVertex_b:
            vertex1.add_con_vertex(vertex)
            vertex2.remove_con_vertex(vertex)

    '''最小变化角构建新相邻边关系（对节点进行遍历）'''

    def reconstruct_edge_min_delta_angle(self, k=math.pi / 6) -> dict:
        """
        基于最小角度变化重构图，返回一个字典，该字典包含所有被合并的边。

        :param k: 两条边的夹角的最小变化角度的阈值。默认为math.pi/6(30度)
        :type k: float
        :return: 道路字典。key是道路的ID，值是节点集合。
        :rtype: dict
        """
        vertices_id = self.__vertices_id.keys()
        new_id = len(vertices_id) + 1
        judge_id = new_id
        vertex_id = 1
        subVertex = {}
        auxVertex = {}
        while vertex_id in self.__vertices_id.keys():
            vertex: GeoVertex = self.__vertices_id[vertex_id]
            conVertices = [i for i in vertex.get_con_vertex()]
            count = len(conVertices)
            conVertices_id = [i.get_id() for i in conVertices]
            vertex_id += 1
            if count <= 1:
                continue
            elif count == 2 and vertex_id <= judge_id:
                continue
            else:
                calDict = {}
                oldConVertices = [i for i in conVertices]
                # 分别计算不同组合下的夹角值
                while conVertices:
                    vertex1 = conVertices.pop()
                    vertex1_id = conVertices_id.pop()
                    for vertex2, vertex2_id in zip(conVertices, conVertices_id):
                        calDict[(vertex1_id, vertex2_id)] = GeoGraph.calculate_angle(vertex1.get_coord(),
                                                                                     vertex2.get_coord(),
                                                                                     vertex.get_coord())
                # 对value进行升序排列
                angleArray = {k: v for k, v in sorted(calDict.items(), key=lambda item: item[1])}
                judgeArray = list(angleArray.values())
                if judgeArray[0] <= k:
                    # 如果最小的比临界值小，则应该是这两个节点进行连接
                    linkedVertices = list(list(angleArray.keys())[0])
                    oldConVertices.remove(self.__vertices_id[linkedVertices[0]])
                    oldConVertices.remove(self.__vertices_id[linkedVertices[1]])
                else:
                    # 最小的变化角比临界值大，则该点应该作为起始节点
                    oldConVertices.pop()
                # 断开该点与其它节点的连接关系
                if oldConVertices:
                    new_id = self.disconnect_vertex(vertex, oldConVertices, new_id, subVertex, auxVertex)
        '''if self.check_graph_simple():
            print('Constructing graph succeed!')
            print('The count of vertices is ' + str(len(list(self.__vertices_id.keys()))))
            print('The count of edges is ' + str(len(list(self.__edges_id.keys()))))'''
        return self.road_trace()

    """模拟退火算法构建新的相邻边关系"""

    def reconstruct_edge_sa(self, t: float, alpha: float) -> dict:
        """
        使用模拟退火算法重建图的顶点之间的新的相邻边关系

        Args:
            t（float）：模拟退火算法的初始温度。
            alpha（float）：模拟退火算法的温度衰减率。

        Returns:
            dict：道路字典。key是道路的ID，值是节点集合。
        """
        vertices_id = self.__vertices_id.keys()
        new_id: int = len(vertices_id) + 1
        judge_id = new_id
        vertex_id = 1
        subVertex = {}  # {v_id1: [new_id1, new_id2, ...], v_id2: [new_id3, ....]} 父节点对应分裂出的点号集合
        auxVertex = {}  # {new_id1: v_id1, new_id2: v_id2 } 分裂出的点号对应的父节点
        angleDict = {}
        if t <= 1:
            return {}
        # 初始化，所有度大于2的点分裂出度为1的点
        print('Starting to initialize')
        time_m = datetime.datetime.now()
        while vertex_id in self.__vertices_id.keys():
            vertex: GeoVertex = self.__vertices_id[vertex_id]
            conVertices = [i for i in vertex.get_con_vertex()]
            count = len(conVertices)
            vertex_id += 1
            if count <= 1:
                continue
            elif count == 2 and vertex_id <= judge_id:
                continue
            else:
                oldConVertices = [i for i in conVertices]
                oldConVertices.pop()
                new_id = self.disconnect_vertex(vertex, oldConVertices, new_id, subVertex, auxVertex)
        for v_id, value in subVertex.items():
            chosen = [v_id] + value
            angleDict[v_id] = {}
            val = 0
            while chosen:
                vertex_id1 = chosen.pop()
                for vertex_id2 in chosen:
                    conVertex1 = self.__vertices_id[vertex_id1].get_con_vertex()[0]
                    conVertex2 = self.__vertices_id[vertex_id2].get_con_vertex()[0]
                    angle = math.pi - self.calculate_angle(conVertex1.get_coord(), conVertex2.get_coord(),
                                                           self.__vertices_id[v_id].get_coord())
                    angleDict[v_id][(vertex_id1, vertex_id2)] = angle / math.pi
                    val += angle / math.pi
            # 对value进行升序排列
            angleDict[v_id] = {k: v for k, v in sorted(angleDict[v_id].items(), key=lambda item: item[1])}
        # 原始相邻关系字典
        iniDict = {}
        for v_id, value in self.__vertices_id.items():
            iniDict[v_id] = [i.get_id() for i in value.get_con_vertex()]
            self.__vertices_id[v_id].set_con_vertex([])
        time_e = datetime.datetime.now()
        print('初始化花费时间:', (time_e - time_m).total_seconds(), '秒')
        # 计算目标函数值
        cost = 99999999
        print('当前目标函数值:', round(cost, 2))
        time_m = datetime.datetime.now()
        result = {}  # 最终相邻关系字典
        for v_id, value in iniDict.items():
            result[v_id] = [i for i in value]
        time_e = datetime.datetime.now()
        print('拷贝花费时间:', (time_e - time_m).total_seconds(), '秒')
        print('Starting to anneal')
        while t > 1:
            print("当前温度: ", round(t, 3))
            time_m = datetime.datetime.now()
            # 回归初始状态
            nowDict = {}
            for v_id, value in iniDict.items():
                nowDict[v_id] = [i for i in value]
            nowCost = 0
            for v_id, value in subVertex.items():
                '''# 获取等待选择的节点号
                chosen = [v_id] + value
                while len(chosen) >= 2:
                    random_numbers = random.sample(range(0, len(chosen)), 2)
                    random_number1 = random_numbers[0]
                    random_number2 = random_numbers[1]
                    # 两个点相连
                    # 排序一个从小到大的节点号
                    ids: list = [chosen[random_number1], chosen[random_number2]]
                    ids.sort()
                    chosen.remove(ids[0])
                    chosen.remove(ids[1])
                    random_number1 = random.randint(0, len(chosen) - 1)
                    random_number2 = random.randint(0, len(chosen) - 1)
                    # 可能不相连
                    if random_number2 == random_number1:
                        del chosen[random_number1]
                        continue'''
                # 获取夹角值的字典
                tempDict = {k: v for k, v in angleDict[v_id].items()}
                while tempDict:
                    lst = self.adjust_list(list(tempDict.values()))
                    random_number = random.random()
                    count = 0
                    ids: tuple
                    for key, pro in zip(tempDict.keys(), lst):
                        count += pro
                        if random_number < count:
                            ids = key
                            break
                    # 合并两个节点
                    conId = nowDict[ids[1]][0]
                    nowDict[conId].append(ids[0])
                    nowDict[conId].remove(ids[1])
                    nowDict[ids[0]].append(conId)
                    nowDict[ids[1]] = []
                    ang = (self.calculate_angle(self.__vertices_id[conId].get_coord(),
                                                self.__vertices_id[nowDict[ids[0]][0]].get_coord(),
                                                self.__vertices_id[ids[0]].get_coord())) / math.pi
                    nowCost += ang ** 2
                    del tempDict[ids]
                    id1 = ids[0]
                    id2 = ids[1]
                    delList = []
                    for key in tempDict.keys():
                        if id1 in key or id2 in key:
                            delList.append(key)
                    for val in delList:
                        del tempDict[val]

            weig = self.get_cost(nowDict)
            nowCost += weig
            dE = nowCost - cost
            print('当前目标函数值:', round(nowCost, 3))
            time_e = datetime.datetime.now()
            print('单次循环花费时间:', (time_e - time_m).total_seconds(), '秒')
            if dE <= 0 or np.random.rand() < np.exp(-dE / t):
                # 如果能接受，则保存结果
                cost = nowCost
                print('接受当前目标函数值')
                for v_id, value in nowDict.items():
                    result[v_id] = [i for i in value]
            t *= alpha
        # 根据相邻关系字典重建
        for v_id, vertex in self.__vertices_id.items():
            realConV_id = result[v_id]
            for conV in realConV_id:
                vertex.add_con_vertex(self.__vertices_id[conV])
        return self.road_trace()

    '''路径追踪'''

    def road_trace(self) -> dict:
        roadDict = {}
        road_count = 1
        nodeVertex = []
        visitedVertex = {}
        for v_id, vertex in self.__vertices_id.items():
            visitedVertex[v_id] = False
            if len(vertex.get_con_vertex()) == 1:
                nodeVertex.append(v_id)
            elif len(vertex.get_con_vertex()) != 2:
                visitedVertex[v_id] = True
        '''端点'''
        for v_id in nodeVertex:
            if not visitedVertex[v_id]:
                visitedVertex[v_id] = True
                roadDict[road_count] = []
                nowVertex = self.__vertices_id[v_id]
                nextVertex = self.__vertices_id[v_id].get_con_vertex()[0]
                roadDict[road_count].append(nowVertex)
                while len(nextVertex.get_con_vertex()) != 1:
                    # 只要nextVertex不是端点
                    preVertex = nowVertex
                    nowVertex = nextVertex
                    vertices = [i for i in nowVertex.get_con_vertex()]
                    nextVertex = vertices[1] if vertices[0] == preVertex else vertices[0]
                    visitedVertex[nowVertex.get_id()] = True
                    roadDict[road_count].append(nowVertex)
                roadDict[road_count].append(nextVertex)
                visitedVertex[nextVertex.get_id()] = True
                road_count += 1
        '''环路'''
        for v_id, nowVertex in self.__vertices_id.items():
            if visitedVertex[v_id]:
                continue
            visitedVertex[v_id] = True
            roadDict[road_count] = []
            nextVertex = nowVertex.get_con_vertex()[0]
            roadDict[road_count].append(nowVertex)
            while not visitedVertex[nextVertex.get_id()]:
                preVertex = nowVertex
                nowVertex = nextVertex
                vertices = [i for i in nowVertex.get_con_vertex()]
                nextVertex = vertices[1] if vertices[0] == preVertex else vertices[0]
                roadDict[road_count].append(nowVertex)
                visitedVertex[nowVertex.get_id()] = True
            roadDict[road_count].append(nextVertex)
            road_count += 1

        return roadDict

    '''根据相邻关系表计算目标函数'''

    @staticmethod
    def get_cost(conDict: dict) -> float:
        road_count = 1
        nodeVertex = []
        visitedVertex = {}
        cost = 0
        for v_id, conVertex in conDict.items():
            visitedVertex[v_id] = False
            if len(conVertex) == 1:
                nodeVertex.append(v_id)
            elif len(conVertex) != 2:
                visitedVertex[v_id] = True
        '''端点'''
        for v_id in nodeVertex:
            if not visitedVertex[v_id]:
                visitedVertex[v_id] = True
                nowVertex = v_id
                nextVertex = conDict[v_id][0]
                count = 1
                while len(conDict[nextVertex]) != 1:
                    # 只要nextVertex不是端点
                    preVertex = nowVertex
                    nowVertex = nextVertex
                    vertices = [i for i in conDict[nowVertex]]
                    nextVertex = vertices[1] if vertices[0] == preVertex else vertices[0]
                    visitedVertex[nowVertex] = True
                    count += 1
                if count > 3:
                    cost -= 1
                visitedVertex[nextVertex] = True
                road_count += 1
        '''环路'''
        for v_id in conDict.keys():
            if visitedVertex[v_id]:
                continue
            visitedVertex[v_id] = True
            nowVertex = v_id
            nextVertex = conDict[v_id][0]
            count = 1
            while not visitedVertex[nextVertex]:
                preVertex = nowVertex
                nowVertex = nextVertex
                vertices = [i for i in conDict[nowVertex]]
                nextVertex = vertices[1] if vertices[0] == preVertex else vertices[0]
                visitedVertex[nowVertex] = True
                count += 1
            if count > 3:
                cost -= 1
            road_count += 1
        return cost

    '''利用BFS遍历从s到t的最短路径(无权图)'''

    def findPath_bfs(self, s: GeoVertex, t: GeoVertex) -> list[GeoVertex]:
        if s == t:
            return []
        res_path = []  # result
        '''use BFS to find the path'''
        open_list = []  # Queue FIFO
        visited_vertex = {}  # is visited?
        search_vertex = {}  # key is the son node, value is the father node
        for key in self.__vertices_id.keys():
            visited_vertex[key] = False
            search_vertex[key] = None
        next_vertex = s
        open_list.append(next_vertex)
        visited_vertex[next_vertex.get_id()] = True
        while True:
            open_list.remove(next_vertex)
            for v in next_vertex.get_con_vertex():
                if not visited_vertex[v.get_id()]:
                    open_list.append(v)
                    visited_vertex[v.get_id()] = True
                    # next_vertex is the father geo_vertex
                    search_vertex[v.get_id()] = next_vertex
                if v == t:
                    # find the path
                    res_path.append(t)
                    next_vertex = t
                    while search_vertex[next_vertex.get_id()] is not None:
                        res_path.append(search_vertex[next_vertex.get_id()])
                        next_vertex = search_vertex[next_vertex.get_id()]
                    return res_path[::-1]
            if len(open_list) == 0:
                # failure
                return []
            # get first geo_vertex
            next_vertex = open_list[0]

    '''非递归方法查找从s到t的所有路径'''

    @staticmethod
    def findAllPath(s: GeoVertex, t: GeoVertex) -> tuple[list, bool]:
        """build stack in order to get all paths form s to t"""
        '''initialize'''
        stack = [(s, [s])]
        paths = []
        flag = True
        while stack and flag:
            (vertex, path) = stack.pop()
            '''k -= 1
            if k < 0:
                break'''
            for neighbor in vertex.get_con_vertex():
                if neighbor in path:
                    # 避免重复经过环路中的节点
                    continue
                if neighbor == t:
                    if len(paths) == 1:
                        flag = False
                        break
                    paths.append(path + [t])

                else:
                    stack.append((neighbor, path + [neighbor]))
        delList = []
        for path in paths:
            if path[-1] != t:
                delList.append(path)
        for del_list in delList:
            paths.remove(del_list)
        return paths, flag

    def __str__(self) -> str:
        return str(self.__name)

    def __repr__(self) -> str:
        return str(self.__name)

    '''路径绘制'''

    def draw_geograph(self, out_path: str, roadDict: dict) -> None:
        """
        使用 pyshp 库画图。

        Args:
            out_path (str): 输出的路径和文件名，不包括后缀名。
            roadDict (dict): 道路字典，包含每一条道路的所有点，格式为 {id: [vertex1, vertex2, ...]}。

        Returns:
            None
        """
        # gdal对应的proj.db在这个文件夹下
        os.environ['PROJ_LIB'] = 'D:\\anaconda3\\Lib\\site-packages\\osgeo\\data\\proj'
        # 字段
        fields = ['id', 'length', 'vertices']
        print(fields)
        # 写字段
        w = shapefile.Writer(out_path, shapeType=3, encoding='utf-8')
        for i in list(fields):
            if i == 'length':
                w.field(i, 'N', decimal=5)
            else:
                w.field(i, 'N', decimal=0)
        for id, vertices in roadDict.items():
            preVertex = None
            # 这条线的坐标
            road_coord = []
            # 这条线路的长度
            road_length = 0
            for vertex in vertices:
                if preVertex is None:
                    preVertex = vertex
                    continue
                nowVertex = vertex
                road_length += self.calculate_distance(preVertex.get_coord(), nowVertex.get_coord())
                road_coord.append(self.mercator_tolonlat(preVertex.get_coord()))
                preVertex = nowVertex
            road_coord.append(self.mercator_tolonlat(preVertex.get_coord()))
            w.line([road_coord])
            w.record(str(id), str(road_length), str(len(vertices)))
        w.close()
        # 写投影信息
        proj = osr.SpatialReference()
        proj.ImportFromEPSG(4326)
        wkt = proj.ExportToWkt()
        # 写出prj文件
        with open(out_path.replace(".shp", ".prj"), 'w') as f:
            f.write(wkt)

        return None

    '''
    静态方法 计算距离
    '''

    @staticmethod
    def calculate_distance(coord1: tuple, coord2: tuple) -> float:
        return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5

    '''
    静态方法 计算角度变化
    '''

    @staticmethod
    def calculate_angle(coord1: tuple, coord2: tuple, mid: tuple) -> float:
        a = [coord1[0] - mid[0], coord1[1] - mid[1]]
        b = [coord2[0] - mid[0], coord2[1] - mid[1]]
        dot_product = sum([x * y for x, y in zip(a, b)])
        a_norm = math.sqrt(sum([x ** 2 for x in a]))
        b_norm = math.sqrt(sum([y ** 2 for y in b]))
        cos_theta = dot_product / (a_norm * b_norm)
        cos_theta = round(cos_theta, 6)
        theta = math.acos(cos_theta)
        if theta > math.pi:
            theta = 2 * math.pi - theta
        return round(math.pi - theta, 6)

    '''
    静态方法 坐标系3857转4326 (x, y)m->(longitude, latitude)°
    '''

    @staticmethod
    def mercator_tolonlat(coord_merca: tuple) -> tuple:
        x = coord_merca[0] / 20037508.34 * 180
        y = coord_merca[1] / 20037508.34 * 180
        y = 180.0 / math.pi * \
            (2 * math.atan(math.exp(y * math.pi / 180.0)) - math.pi / 2)
        out = (x, y)
        return out

    @staticmethod
    def adjust_list(lst):
        lst2 = [math.exp(i) - 1 for i in lst]

        # 确保所有值之和为1
        total = sum(lst2)
        for i in range(len(lst2)):
            lst2[i] /= total
        return lst2
