from GeoVertex import GeoVertex
from GeoEdge import GeoEdge
import numpy as np
import shapefile  # 使用pyshp
from osgeo import osr
import os
import copy

glob_cost = []
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

    def __init__(self, g_id: str = '') -> None:
        self.__vertices = {}
        self.__id = g_id
        self.__edges = {}

    '''检查该图是否合法（简单图）'''

    def check_graph_simple(self) -> bool:
        """检查点是否合法 无重边，无自环"""
        for edge_id in self.__vertices.keys():
            temp_value = self.__vertices[edge_id]
            if edge_id in temp_value.get_con_vertex():
                print("vertex: error 1")
                return False
            judge = {}
            for i in temp_value.get_con_vertex():
                if i not in judge.keys() and temp_value in i.get_con_vertex():
                    judge[i] = 1
                else:
                    print("edge: error 2")
                    return False
        '''检查边是否合法 无重边 无自边'''
        for edge_id in self.__edges.keys():
            temp_edge = self.__edges[edge_id]
            con_v = list(temp_edge.get_con_edge().keys())
            con_edge = list(temp_edge.get_con_edge().values())
            for item in con_edge:
                if temp_edge in item:
                    print("edge: error 1")
                    return False
            for item in con_v:
                judge = {}
                con_edge = temp_edge.get_con_edge()[item]
                for i in con_edge:
                    if i not in judge.keys() and temp_edge in i.get_con_edge()[item]:
                        judge[i] = 1
                    else:
                        print(temp_edge)
                        print("edge: error 2")
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

    def set_id(self, g_id: str) -> None:
        self.__id = g_id

    '''添加节点'''

    def add_vertex(self, geo_vertex: GeoVertex) -> None:
        self.__vertices[geo_vertex.get_id()] = geo_vertex

    '''删除节点'''

    def remove_vertex_v(self, geo_vertex: GeoVertex) -> None:
        v_id = geo_vertex.get_id()
        del self.__vertices[v_id]

    '''图中边的添加与删除'''

    def add_edge(self, edge: GeoEdge) -> None:
        vertices = list(edge.get_con_edge().keys())
        self.__edges[edge.get_id()] = edge
        # 添加相邻关系
        if len(vertices) == 2:
            vertices[0].add_con_vertex(vertices[1], edge)
        elif len(vertices) == 1:
            vertices[0].add_con_vertex(vertices[0], edge)

    def remove_edge(self, edge: GeoEdge) -> None:
        vertices = list(edge.get_con_edge().keys())
        del self.__edges[edge.get_id()]
        # 删除相邻关系
        if len(vertices) == 2:
            vertices[0].remove_con_vertex(vertices[1], edge)
        elif len(vertices) == 1:
            vertices[0].remove_con_vertex(vertices[0], edge)

    '''通过节点id查找节点'''

    def find_vertex(self, v_id: int) -> GeoVertex:
        return self.__vertices[v_id]

    '''通过两节点找边'''

    @staticmethod
    def find_edge_v(vertex_1: GeoVertex, vertex_2: GeoVertex) -> GeoEdge:
        con_v = vertex_1.get_con_vertex()
        index = con_v.index(vertex_2)
        return vertex_1.get_con_edge()[index]

    '''通过边号找边 消除引用'''

    def find_edge_id(self, e_id: int) -> GeoEdge:
        return self.__edges[e_id]

    '''利用BFS遍历从s到t的最短路径(无权图)'''

    def findpath_bfs(self, s: 'GeoVertex', t: 'GeoVertex') -> 'list[GeoVertex]':
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
            for v in next_vertex.get_con_vertex():
                if not visited_vertex[v]:
                    open_list.append(v)
                    visited_vertex[v] = True
                    # next_vertex is the father geo_vertex
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
                return []
            # get first geo_vertex
            next_vertex = open_list[0]

    '''非递归方法查找从s到t的所有路径'''

    @staticmethod
    def find_all_path(s: GeoVertex, t: GeoVertex) -> dict:
        """build stack in order to get all path form s to t"""
        '''initialize'''
        main_stack = []  # main stack
        sub_stack = []  # second stack
        main_stack.append(s)
        next_node_list = []
        for v in s.get_con_vertex():
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
        for v in next_node.get_con_vertex():
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
                for v in next_node.get_con_vertex():
                    if v not in main_stack:
                        next_node_list.append(v)
                sub_stack.append(next_node_list)
            else:
                main_stack.pop()
        return all_path

    def __str__(self) -> str:
        return str(self.__id)

    def __repr__(self) -> str:
        return str(self.__id)

    '''最小变化角构建新的相邻边关系'''

    def reconstruct_edge_min_delta_angle(self) -> None:
        key_id = self.__edges.keys()
        for e_id in key_id:
            temp_edge: GeoEdge = self.__edges[e_id]
            temp_con_edge = temp_edge.get_con_edge()
            # 这种环路比较特殊 需要特殊处理
            if len(temp_con_edge.keys()) == 1:
                continue
            vertex1: GeoVertex
            vertex2: GeoVertex
            [vertex1, vertex2] = temp_con_edge.keys()
            """fclass相等的边才能进行连接判断"""
            fclass: str = temp_edge.get_edge_att()['fclass']
            fclass_con_edge = {vertex1: [x for x in temp_con_edge[vertex1]
                                         if x.get_edge_att()['fclass'] != fclass],
                               vertex2: [x for x in temp_con_edge[vertex2]
                                         if x.get_edge_att()['fclass'] != fclass]}
            for i in fclass_con_edge[vertex1]:
                temp_edge.remove_con_edge(i, vertex1)
            for i in fclass_con_edge[vertex2]:
                temp_edge.remove_con_edge(i, vertex2)
            delta_angle = temp_edge.get_delta_angle()
            if len(temp_con_edge[vertex1]) == 1:
                # 判断相邻的是不是环路 如果是 则不计算变化角
                if len(temp_con_edge[vertex1][0].get_con_edge().keys()) != 1:
                    delta_angle_vertex1 = delta_angle[vertex1][0]
                    if abs(delta_angle_vertex1) >= np.pi / 6:
                        temp_edge.remove_con_edge(temp_con_edge[vertex1][0], vertex1)
            # == 0的情况是端点，不做处理
            elif len(temp_con_edge[vertex1]) != 0:
                delta_angle_vertex1 = delta_angle[vertex1]
                # 查找变化角最小,且<pi/6的边
                min_angle = min(delta_angle_vertex1)
                if abs(min_angle) < np.pi / 6:
                    min_edge = temp_con_edge[vertex1][delta_angle_vertex1.index(min_angle)]
                    temp_con_edge_vertex1 = [x for x in temp_con_edge[vertex1] if x != min_edge]
                    for i in temp_con_edge_vertex1:
                        temp_edge.remove_con_edge(i, vertex1)
                else:
                    temp_con_edge_vertex1 = [x for x in temp_con_edge[vertex1]]
                    for i in temp_con_edge_vertex1:
                        temp_edge.remove_con_edge(i, vertex1)
            if len(temp_con_edge[vertex2]) == 1:
                # 判断相邻的是不是环路 如果是 则不计算变化角
                if len(temp_con_edge[vertex2][0].get_con_edge().keys()) != 1:
                    delta_angle_vertex2 = delta_angle[vertex2][0]
                    if abs(delta_angle_vertex2) >= np.pi / 6:
                        temp_edge.remove_con_edge(temp_con_edge[vertex2][0], vertex2)
            elif len(temp_con_edge[vertex2]) != 0:
                delta_angle_vertex2 = delta_angle[vertex2]
                # 查找变化角最小,且<pi/6的边
                min_angle = min(delta_angle_vertex2)
                if abs(min_angle) < np.pi / 6:
                    """仅保留最小变化角的边相连关系，删除其它边的相连关系"""
                    min_edge = temp_con_edge[vertex2][delta_angle_vertex2.index(min_angle)]
                    temp_con_edge_vertex2 = [x for x in temp_con_edge[vertex2] if x != min_edge]
                    for i in temp_con_edge_vertex2:
                        temp_edge.remove_con_edge(i, vertex2)
                else:
                    """相邻边全部删除"""
                    temp_con_edge_vertex2 = [x for x in temp_con_edge[vertex2]]
                    for i in temp_con_edge_vertex2:
                        temp_edge.remove_con_edge(i, vertex2)

    """模拟退火算法构建新的相邻边关系"""

    @staticmethod
    def reconstruct_edge_sa(graph: 'GeoGraph') -> 'GeoGraph':
        basic_graph = copy.copy(graph)  # 拷贝建立原始相邻边关系
        result_graph = copy.copy(graph)
        t = 100  # 初始温度100
        alpha = 0.95  # 退火速率
        """
        马尔科夫链长(为了方便 存储的是{边id: bool} False代表本次迭代没有它) = key个数是边数 算法在马尔可夫链的长度内持续进行产生新解、判断、接受/舍弃的迭代过程
                    随着t的降低 马尔科夫链链长也会减少
        """
        markov_len = {}
        for eId in list(graph.__edges.keys()):
            markov_len[eId] = True
        func_value = None
        # 开始退火
        while t > 1:
            for eId in markov_len.keys():
                if not markov_len[eId]:
                    continue
                edge: GeoEdge = basic_graph.__edges[eId]
                loop_edge: GeoEdge = graph.__edges[eId]
                con_edge_dict = edge.get_con_edge()
                loop_con_edge_dict = loop_edge.get_con_edge()
                vertices = list(con_edge_dict.keys())
                for v in vertices:
                    if not con_edge_dict[v]:
                        continue
                    # 相邻边
                    con_edge = con_edge_dict[v]
                    loop_con_edge = loop_con_edge_dict[v]
                    # 概率
                    pro_list = edge.get_probability()[v]
                    chose_edge = None
                    for index, e in enumerate(con_edge):
                        if np.random.rand() <= pro_list[index]:
                            # 选中了
                            chose_edge = e
                            break
                    remove_list = [x for x in loop_con_edge]
                    for e in remove_list:
                        loop_edge.remove_con_edge(e, v)
                    if chose_edge is not None:
                        loop_edge.add_con_edge(chose_edge, v)
            last_value = func_value
            markov_len, func_value = graph.calculate_graph_cost(markov_len, t)
            if last_value is None:
                continue
            if last_value > func_value:
                result_graph = copy.copy(graph)
            elif np.random.rand() < np.exp(-(func_value - last_value) / t):
                result_graph = copy.copy(graph)
            print("当前温度: ", t)
            t *= alpha
        print('MAX:' + str(max(glob_cost)))
        return result_graph

    """计算目标函数值"""

    def calculate_graph_cost(self, markov_len, t):
        # cost
        cost = 0.0
        # 判断当前路计算了没
        flag_edge = {}
        # 计数 构建的线路数
        count_road = 0
        for eId in self.__edges.keys():
            flag_edge[eId] = False
        for eId in self.__edges.keys():
            if np.random.rand() >= 1:  # (100 - t) / 99
                markov_len[eId] = False
            if flag_edge[eId]:
                continue
            edge: GeoEdge = self.__edges[eId]
            # 它是环路
            if len(list(edge.get_con_edge().keys())) == 1:
                next_edge = edge
                next_vertex: GeoVertex = list(next_edge.get_con_edge().keys())[0]
                # 线路数+=1
                count_road += 1
                # 这条线路的坐标
                road_coord = []
                # 循环数
                count_while = 0
                # 没到下一个环路或端点就一直循环
                while True:
                    count_while += 1
                    flag_edge[next_edge.get_id()] = True
                    # 坐标
                    road_coord.append(next_edge.get_coord())
                    # next_edge不是起始边
                    if count_while != 1:
                        # next_edge是环路 则终止while
                        if len(next_edge.get_con_edge().keys()) == 1:
                            road_coord.pop()
                            break
                        # next_edge是端点 则终止while
                        elif (not list(next_edge.get_con_edge().values())[0] and
                              list(next_edge.get_con_edge().values())[
                                  1]) or (not list(next_edge.get_con_edge().values())[1]
                                          and list(next_edge.get_con_edge().values())[0]):
                            break
                    # 否则找到下一个next_edge
                    # 它是环路
                    if len(list(next_edge.get_con_edge().keys())) == 1:
                        # 它是环路且是孤边
                        if not next_edge.get_con_edge()[next_vertex]:
                            road_coord = []
                            break
                        else:
                            road_coord = []
                            cost += 220000
                            next_edge = next_edge.get_con_edge()[next_vertex][0]
                    else:
                        next_vertices = list(next_edge.get_con_edge().keys())
                        if next_vertex == next_vertices[0]:
                            next_vertex = next_vertices[1]
                        else:
                            next_vertex = next_vertices[0]
                        next_edge = next_edge.get_con_edge()[next_vertex][0]

                # 根据coord计算偏移量
                cost += GeoGraph.get_cost(road_coord)
            # 它是孤边 edge.__conEdge = {v1: [], v2: []}
            elif not list(edge.get_con_edge().values())[0] and not list(edge.get_con_edge().values())[1]:
                flag_edge[eId] = True
                count_road += 1
                vertices = list(edge.get_con_edge().keys())
                # 它本来就是孤边
                if not vertices[0].get_con_vertex() and not vertices[1].get_con_vertex():
                    continue
                # 我们后来把它分成了孤边
                else:
                    cost += GeoGraph.get_cost(edge.get_coord())
            # 它是端点 edge.__conEdge = {v1: [e1, ...], v2: []} or edge.__conEdge = {v1: [], v2: [e1, ...]}
            elif (not list(edge.get_con_edge().values())[0] and list(edge.get_con_edge().values())[1]) or \
                    (not list(edge.get_con_edge().values())[1] and list(edge.get_con_edge().values())[0]):
                next_edge = edge
                # 这条线路的id
                count_road += 1
                # 这条线路的坐标
                road_coord = []
                # while循环计数
                count_while = 0
                # 找到下一个节点
                if list(next_edge.get_con_edge().values())[0]:
                    next_vertex = list(next_edge.get_con_edge().keys())[1]
                else:
                    next_vertex = list(next_edge.get_con_edge().keys())[0]
                # 没到端点或环路就一直循环
                while True:
                    count_while += 1
                    flag_edge[next_edge.get_id()] = True
                    # 坐标
                    road_coord.append(next_edge.get_coord())
                    # next_edge不是起始边
                    if count_while != 1:
                        # next_edge是环路 则终止while
                        if len(next_edge.get_con_edge().keys()) == 1:
                            road_coord.pop()
                            cost += 220000
                            break
                        # next_edge是端点 则终止while
                        elif (not list(next_edge.get_con_edge().values())[0] and
                              list(next_edge.get_con_edge().values())[
                                  1]) or (not list(next_edge.get_con_edge().values())[1]
                                          and list(next_edge.get_con_edge().values())[0]):
                            break
                    # next_edge即不是起始边也不是终止边，则找到下一个next_edge
                    if len(list(next_edge.get_con_edge().keys())) == 1:
                        next_edge = next_edge.get_con_edge()[next_vertex][0]
                    else:
                        next_vertices = list(next_edge.get_con_edge().keys())
                        if next_vertex == next_vertices[0]:
                            next_vertex = next_vertices[1]
                        else:
                            next_vertex = next_vertices[0]
                        next_edge = next_edge.get_con_edge()[next_vertex][0]
                # 对坐标数组求cost
                cost += GeoGraph.get_cost(road_coord)

        return markov_len, cost

    '''对数组进行求和'''

    @staticmethod
    def get_sum_value(value_str):
        my_sum = 0.0
        for item in value_str:
            my_sum = my_sum + item
        return my_sum

    """通过coord计算cost"""

    @staticmethod
    def get_cost(road_coord):
        if not road_coord:
            return 0.0
        coord = road_coord[0]
        temp_coord = []
        if isinstance(coord, tuple):
            return 220000
        else:
            # 降维
            for index, d in enumerate(road_coord):
                temp_coord.append(d[0])
                temp_coord.append(d[-1])
        x0 = temp_coord[0][0]
        y0 = temp_coord[0][1]
        xn = temp_coord[-1][0]
        yn = temp_coord[-1][1]
        if x0 == xn and y0 == yn:
            return 0
        if xn == x0:
            # 总的直线方程是x=x0 无斜率
            temp_coord2 = temp_coord[1:]
            temp_coord.pop()
            # 这条路线积分
            square = 0.0
            # 这条线路边长
            length = 0.0
            for index, coord in enumerate(temp_coord):
                # 这时的coord是一个tuple
                x1 = coord[0]
                y1 = coord[1]
                x2 = temp_coord2[index][0]
                y2 = temp_coord2[index][1]
                my_coord1 = (x1, y1)
                my_coord2 = (x2, y2)
                length += GeoEdge.calculate_distance(my_coord1, my_coord2)
                if y2 == y1:
                    continue
                if (x1 >= x0 and x2 >= x0) or (x1 <= x0 and x2 <= x0):
                    # 同边
                    # 经过(x1, y1)的直线且垂直于x=x0的方程为y=y1
                    # 经过(x2, y2)的直线且垂直于x=x1的方程为y=y2
                    # 上底
                    top_length = abs(x2 - x0)
                    # 下底
                    last_length = abs(x1 - x0)
                    # 高
                    height = abs(y2 - y1)
                    # 面积
                    square += (top_length + last_length) * height / 2
                else:
                    # 异边 这条直线一定有斜率
                    k = y2 - y1 / x2 - x1
                    b = y1 - k * x1
                    # 交点y坐标
                    y = k * x0 + b
                    height1 = abs(y - y1)
                    height2 = abs(y - y2)
                    square += height1 * abs(x1 - x0) / 2 + height2 * abs(x2 - x0)
            cost = square / (length ** 2)  # cost = 路径积分/边长^2
        elif yn == y0:
            # 总的直线方程是y=y0
            temp_coord2 = temp_coord[1:]
            temp_coord.pop()
            # 这条路线积分
            square = 0.0
            # 这条线路边长
            length = 0.0
            for index, coord in enumerate(temp_coord):
                # 这时的coord是一个tuple
                x1 = coord[0]
                y1 = coord[1]
                x2 = temp_coord2[index][0]
                y2 = temp_coord2[index][1]
                my_coord1 = (x1, y1)
                my_coord2 = (x2, y2)
                length += GeoEdge.calculate_distance(my_coord1, my_coord2)
                if x2 == x1:
                    continue
                if (x1 >= x0 and x2 >= x0) or (x1 <= x0 and x2 <= x0):
                    # 同边
                    # 经过(x1, y1)的直线且垂直于y=y0的方程为x=x1
                    # 经过(x2, y2)的直线且垂直于y=y1的方程为x=x2
                    # 上底
                    top_length = abs(y2 - y0)
                    # 下底
                    last_length = abs(y1 - y0)
                    # 高
                    height = abs(x2 - x1)
                    # 面积
                    square += (top_length + last_length) * height / 2
                else:
                    if x1 == x2:
                        continue
                    # 异边 这条直线一定有斜率
                    k = y2 - y1 / x2 - x1
                    b = y1 - k * x1
                    # 交点x坐标
                    x = (y0 - b) / k
                    height1 = abs(x - x1)
                    height2 = abs(x - x2)
                    square += height1 * abs(y1 - y0) / 2 + height2 * abs(y2 - y0)
            cost = square / (length ** 2)  # cost = 路径积分/边长^2
        else:
            # 起点到终点的斜率 直线方程为y=kx+b
            k = (yn - y0) / (xn - x0)
            b = yn - k * xn
            temp_coord2 = temp_coord[1:]
            temp_coord.pop()
            # 这条线路面积
            square = 0.0
            # 这条线路边长
            length = 0.0
            for index, coord in enumerate(temp_coord):
                # 这时的coord是一个tuple
                x1 = coord[0]
                y1 = coord[1]
                x2 = temp_coord2[index][0]
                y2 = temp_coord2[index][1]
                my_coord1 = (x1, y1)
                my_coord2 = (x2, y2)
                length += GeoEdge.calculate_distance(my_coord1, my_coord2)
                if (x1 >= x0 and x2 >= x0) or (x1 <= x0 and x2 <= x0):
                    # 同边
                    # 经过(x1, y1)的直线且垂直于y=kx+b的方程为 y = -x/k + b1
                    b1 = y1 + x1 / k
                    # 交点
                    x3 = (b1 - b) / (k + 1 / k)
                    y3 = k * x3 + b
                    # 经过(x2, y2)的直线且垂直于y=kx+b的方程为y = -x/k + b2
                    b2 = y2 + x2 / k
                    # 交点
                    x4 = (b2 - b1) / (k + 1 / k)
                    y4 = k * x4 + b
                    # 上底
                    top_length = GeoEdge.calculate_distance(my_coord1, (x3, y3))
                    # 下底
                    last_length = GeoEdge.calculate_distance(my_coord2, (x4, y4))
                    # 高
                    height = GeoEdge.calculate_distance((x3, y3), (x4, y4))
                    # 面积
                    square += (top_length + last_length) * height / 2
                else:
                    if x1 == x2:
                        # y=kx+b与x=x1交点(x,y)坐标
                        y = k * x1 + b
                        x = x1
                    else:
                        # y=kx+b 与过(x1,y1) (x2,y2)的直线的交点
                        y = (y1 - b + (y1 - y2) * x1 / (x2 - x1)) / (k + (y1 - y2) / (x2 - x1))
                        x = (y - b) / k
                    # 经过(x1, y1)的直线且垂直于y=kx+b的方程为 y = -x/k + b1
                    b1 = y1 + x1 / k
                    # 交点
                    x3 = (b1 - b) / (k + 1 / k)
                    y3 = k * x3 + b
                    # 经过(x2, y2)的直线且垂直于y=kx+b的方程为y = -x/k + b2
                    b2 = y2 + x2 / k
                    # 交点
                    x4 = (b2 - b1) / (k + 1 / k)
                    y4 = k * x4 + b
                    # 高1
                    height1 = GeoEdge.calculate_distance(my_coord1, (x3, y3))
                    # 高2
                    height2 = GeoEdge.calculate_distance(my_coord2, (x4, y4))
                    # 底1
                    length1 = GeoEdge.calculate_distance((x3, y3), (x, y))
                    # 底2
                    length2 = GeoEdge.calculate_distance((x4, y4), (x, y))
                    # 面积
                    square += height1 * length1 + height2 * length2
            cost = square / (length ** 2)  # 路径积分/边长^2
            glob_cost.append(cost)
        return cost

    '''求出现次数最多的字符串'''

    @staticmethod
    def get_most_times_value(value_str):
        my_hash = dict()
        for item in value_str:
            if item in my_hash:
                my_hash[item] += 1
            else:
                my_hash[item] = 1

        return max(my_hash, key=my_hash.get)

    def draw_geograph(self, out_path: str = '') -> None:
        """利用pyshp画图"""
        # gdal对应的proj.db在这个文件夹下
        os.environ['PROJ_LIB'] = 'D:\\anaconda3\\Lib\\site-packages\\osgeo\\data\\proj'
        # 字段
        fields: list = []
        for eId in self.__edges.keys():
            fields = list(self.__edges[eId].get_edge_att().keys())
            break
        fields.remove('osmid')
        fields.remove('keyId')
        fields.append('包含的路段id')
        fields.append('id')
        print(fields)

        # 写字段
        w = shapefile.Writer(out_path, shapeType=3, encoding='utf-8')
        for i in list(fields):
            if i == 'length':
                w.field(i, 'N', decimal=5)
            elif i == 'id':
                w.field('id', 'N', decimal=0)
            else:
                w.field(i, 'C')

        # 判断当前路画了没
        flag_edge = {}
        # 计数 处理的路段数
        count_line = 0
        # 计数 构建的线路数 当成构建线路时的唯一id
        count_road = 0
        for eId in self.__edges.keys():
            flag_edge[eId] = False
        for eId in self.__edges.keys():
            if flag_edge[eId]:
                continue
            edge: GeoEdge = self.__edges[eId]
            # 它是环路
            if len(list(edge.get_con_edge().keys())) == 1:
                next_edge = edge
                next_vertex: GeoVertex = list(next_edge.get_con_edge().keys())[0]
                # 这条线路的id
                count_road += 1
                # 这条线路的属性
                road_record = []
                # 这条线路的坐标
                road_coord = []
                # 循环数
                count_while = 0
                # 找到起始节点
                from_id = list(edge.get_con_edge().keys())[0].get_id()
                # 没到下一个环路或端点就一直循环
                while True:
                    count_while += 1
                    flag_edge[next_edge.get_id()] = True
                    # 当前路段的属性
                    temp_road_record = []
                    count_line += 1
                    for t in fields:
                        if t == 'from_' or t == 'to':
                            temp_road_record.append(int(next_edge.get_edge_att()[t]))
                        elif t == 'osmid' or t == 'keyId':
                            continue
                        elif t == '包含的路段id':
                            temp_road_record.append(int(next_edge.get_edge_att()['keyId']))
                        elif t == 'id':
                            temp_road_record.append(count_road)
                        else:
                            temp_road_record.append(next_edge.get_edge_att()[t])
                    # 添加进总线路属性中
                    road_record.append(temp_road_record)
                    # 坐标
                    road_coord.append(GeoEdge.mercator_tolonlat(next_edge.get_coord()))
                    # next_edge不是起始边
                    if count_while != 1:
                        # next_edge是环路 则终止while
                        if len(next_edge.get_con_edge().keys()) == 1:
                            # 找到终止节点
                            to_id = list(next_edge.get_con_edge().keys())[0].get_id()
                            break
                        # next_edge是端点 则终止while
                        elif (not list(next_edge.get_con_edge().values())[0] and
                              list(next_edge.get_con_edge().values())[
                                  1]) or (not list(next_edge.get_con_edge().values())[1]
                                          and list(next_edge.get_con_edge().values())[0]):
                            # 终止节点
                            if list(next_edge.get_con_edge().values())[0]:
                                to_id = list(next_edge.get_con_edge().keys())[0].get_id()
                            else:
                                to_id = list(next_edge.get_con_edge().keys())[1].get_id()
                            break
                    # 否则找到下一个next_edge
                    # 它是环路
                    if len(list(next_edge.get_con_edge().keys())) == 1:
                        # 它是环路且是孤边
                        if not next_edge.get_con_edge()[next_vertex]:
                            to_id = from_id
                            break
                        else:
                            next_edge = next_edge.get_con_edge()[next_vertex][0]
                    else:
                        next_vertices = list(next_edge.get_con_edge().keys())
                        if next_vertex == next_vertices[0]:
                            next_vertex = next_vertices[1]
                        else:
                            next_vertex = next_vertices[0]
                        next_edge = next_edge.get_con_edge()[next_vertex][0]
                # 对总线路属性进行整理 保留出现次数最多的字符串 求和等
                road_record = list(map(list, zip(*road_record)))
                final_record = []
                for index, rec in enumerate(road_record):
                    # 求和字段
                    if fields[index] == 'length':
                        final_record.append(GeoGraph.get_sum_value(rec))
                    # 该线路id
                    elif fields[index] == 'id':
                        final_record.append(count_road)
                    # 起始节点
                    elif fields[index] == 'from_':
                        final_record.append(int(from_id))
                    # 终止节点
                    elif fields[index] == 'to':
                        final_record.append(int(to_id))
                    # 包含的路段id
                    elif fields[index] == '包含的路段id':
                        final_record.append(rec)
                    # 否则获取出现次数最多的字符串
                    else:
                        final_record.append(GeoGraph.get_most_times_value(rec))
                # 写这条线路
                w.record(*final_record)
                w.line(road_coord)
            # 它是孤边 edge.__conEdge = {v1: [], v2: []}
            elif not list(edge.get_con_edge().values())[0] and not list(edge.get_con_edge().values())[1]:
                flag_edge[eId] = True
                count_line += 1
                count_road += 1
                # 记录属性
                road_record = []
                for t in fields:
                    if t == 'from_' or t == 'to':
                        road_record.append(int(edge.get_edge_att()[t]))
                    elif t == 'osmid' or t == 'keyId':
                        continue
                    elif t == '包含的路段id':
                        road_record.append(int(edge.get_edge_att()['keyId']))
                    elif t == 'id':
                        # 加入唯一id
                        road_record.append(count_road)
                    else:
                        road_record.append(edge.get_edge_att()[t])
                # 画这条线路
                w.record(*road_record)  # 属性
                w.line([GeoEdge.mercator_tolonlat(edge.get_coord())])  # 坐标

            # 它是端点 edge.__conEdge = {v1: [e1, ...], v2: []} or edge.__conEdge = {v1: [], v2: [e1, ...]}
            elif (not list(edge.get_con_edge().values())[0] and list(edge.get_con_edge().values())[1]) or \
                    (not list(edge.get_con_edge().values())[1] and list(edge.get_con_edge().values())[0]):
                next_edge = edge
                # 这条线路的id
                count_road += 1
                # 这条线路的属性
                road_record = []
                # 这条线路的坐标
                road_coord = []
                # while循环计数
                count_while = 0
                # 找到起始节点
                if list(next_edge.get_con_edge().values())[0]:
                    from_id = list(next_edge.get_con_edge().keys())[0].get_id()
                    next_vertex = list(next_edge.get_con_edge().keys())[1]
                else:
                    from_id = list(next_edge.get_con_edge().keys())[1].get_id()
                    next_vertex = list(next_edge.get_con_edge().keys())[0]
                # 没到端点或环路就一直循环
                while True:
                    count_while += 1
                    flag_edge[next_edge.get_id()] = True
                    # 当前路段的属性
                    temp_road_record = []
                    count_line += 1
                    for t in fields:
                        if t == 'from_' or t == 'to':
                            temp_road_record.append(int(next_edge.get_edge_att()[t]))
                        elif t == 'osmid' or t == 'keyId':
                            continue
                        elif t == '包含的路段id':
                            temp_road_record.append(int(next_edge.get_edge_att()['keyId']))
                        elif t == 'id':
                            temp_road_record.append(count_road)
                        else:
                            temp_road_record.append(next_edge.get_edge_att()[t])
                    # 添加进总线路属性中
                    road_record.append(temp_road_record)
                    # 坐标
                    road_coord.append(GeoEdge.mercator_tolonlat(next_edge.get_coord()))
                    # next_edge不是起始边
                    if count_while != 1:
                        # next_edge是环路 则终止while
                        if len(next_edge.get_con_edge().keys()) == 1:
                            # 找到终止节点
                            to_id = list(next_edge.get_con_edge().keys())[0].get_id()
                            break
                        # next_edge是端点 则终止while
                        elif (not list(next_edge.get_con_edge().values())[0] and
                              list(next_edge.get_con_edge().values())[
                                  1]) or (not list(next_edge.get_con_edge().values())[1]
                                          and list(next_edge.get_con_edge().values())[0]):
                            # 找到终止节点
                            if list(next_edge.get_con_edge().values())[0]:
                                to_id = list(next_edge.get_con_edge().keys())[0].get_id()
                            else:
                                to_id = list(next_edge.get_con_edge().keys())[1].get_id()
                            break
                    # next_edge即不是起始边也不是终止边，则找到下一个next_edge
                    if len(list(next_edge.get_con_edge().keys())) == 1:
                        next_edge = next_edge.get_con_edge()[next_vertex][0]
                    else:
                        next_vertices = list(next_edge.get_con_edge().keys())
                        if next_vertex == next_vertices[0]:
                            next_vertex = next_vertices[1]
                        else:
                            next_vertex = next_vertices[0]
                        next_edge = next_edge.get_con_edge()[next_vertex][0]
                # 对总线路属性进行整理 保留出现次数最多的字符串 求和等
                road_record = list(map(list, zip(*road_record)))
                final_record = []
                for index, rec in enumerate(road_record):
                    # 求和字段
                    if fields[index] == 'length':
                        final_record.append(GeoGraph.get_sum_value(rec))
                    # 该线路id
                    elif fields[index] == 'id':
                        final_record.append(count_road)
                    # 起始节点
                    elif fields[index] == 'from_':
                        final_record.append(int(from_id))
                    # 终止节点
                    elif fields[index] == 'to':
                        final_record.append(int(to_id))
                    # 包含的路段id
                    elif fields[index] == '包含的路段id':
                        final_record.append(rec)
                    # 否则获取出现次数最多的字符串
                    else:
                        final_record.append(GeoGraph.get_most_times_value(rec))
                # 写这条线路
                w.record(*final_record)
                w.line(road_coord)
        # 现在都是由不是端点的路组成的新的环路
        for eId in self.__edges.keys():
            if flag_edge[eId]:
                continue
            edge: GeoEdge = self.__edges[eId]
            next_edge = edge
            next_vertex = list(next_edge.get_con_edge().keys())[0]
            from_id = to_id = next_vertex.get_id()
            # 这条线路的id
            count_road += 1
            # 这条线路的属性
            road_record = []
            # 这条线路的坐标
            road_coord = []
            while True:
                flag_edge[next_edge.get_id()] = True
                # 当前路段的属性
                temp_road_record = []
                count_line += 1
                for t in fields:
                    if t == 'from_' or t == 'to':
                        temp_road_record.append(int(next_edge.get_edge_att()[t]))
                    elif t == 'osmid' or t == 'keyId':
                        continue
                    elif t == '包含的路段id':
                        temp_road_record.append(int(next_edge.get_edge_att()['keyId']))
                    elif t == 'id':
                        temp_road_record.append(count_road)
                    else:
                        temp_road_record.append(next_edge.get_edge_att()[t])
                # 添加进总线路属性中
                road_record.append(temp_road_record)
                # 坐标
                road_coord.append(GeoEdge.mercator_tolonlat(next_edge.get_coord()))
                next_vertices = list(next_edge.get_con_edge().keys())
                # 找下一个nex_edge
                if next_vertex == next_vertices[0]:
                    next_vertex = next_vertices[1]
                else:
                    next_vertex = next_vertices[0]
                next_edge = next_edge.get_con_edge()[next_vertex][0]
                # 如果该next_edge写过了 则终止while循环
                if flag_edge[next_edge.get_id()]:
                    break
            # 对总线路属性进行整理 保留出现次数最多的字符串 求和等
            road_record = list(map(list, zip(*road_record)))
            final_record = []
            for index, rec in enumerate(road_record):
                # 求和字段
                if fields[index] == 'length':
                    final_record.append(GeoGraph.get_sum_value(rec))
                # 该线路id
                elif fields[index] == 'id':
                    final_record.append(count_road)
                # 起始节点
                elif fields[index] == 'from_':
                    final_record.append(int(from_id))
                # 终止节点
                elif fields[index] == 'to':
                    final_record.append(int(to_id))
                # 包含的路段id
                elif fields[index] == '包含的路段id':
                    final_record.append(rec)
                # 否则获取出现次数最多的字符串
                else:
                    final_record.append(GeoGraph.get_most_times_value(rec))
            # 写这条线路
            w.record(*final_record)
            w.line(road_coord)
        print('处理了', count_line, '条路段，生成', count_road, '条路')
        w.close()
        # 写投影信息
        proj = osr.SpatialReference()
        proj.ImportFromEPSG(4326)
        wkt = proj.ExportToWkt()
        # 写出prj文件
        f = open(out_path.replace(".shp", ".prj"), 'w')
        f.write(wkt)
        f.close()
        for e_id in flag_edge.keys():
            if not flag_edge[e_id]:
                print(e_id)

        return None
