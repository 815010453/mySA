from attr import field
from GeoVertex import GeoVertex
from GeoEdge import GeoEdge
import numpy as np
import shapefile  # 使用pyshp
from osgeo import osr
import os
# gdal对应的proj.db在这个文件夹下
os.environ['PROJ_LIB'] = 'D:\\anaconda3\\Lib\\site-packages\\osgeo\\data\\proj'
"""
GeoGraph Class
----------

由GeoVertex组成的简单地理图. 

"""


class GeoGraph():
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
        '''检查点是否合法 无重边，无自环'''
        for id in self.__vertices.keys():
            tempValue = self.__vertices[id]
            if id in tempValue.get_conVertex():
                return False
            judge = {}
            for i in tempValue.get_conVertex():
                if i not in judge.keys() and tempValue in i.get_conVertex():
                    judge[i] = 1
                else:
                    return False
        '''检查边是否合法 无重边 无自边'''
        for id in self.__edges.keys():
            tempValue = self.__edges[id]
            v = list(tempValue.get_conEdge().keys())
            conEdge = list(tempValue.get_conEdge().values())
            for item in conEdge:
                if id in item:
                    return False
            for item in v:
                judge = {}
                conEdge = tempValue.get_conEdge()[item]
                for i in conEdge:
                    if i not in judge.keys() and tempValue in i.get_conEdge()[item]:
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

    def find_vertex(self, id: int = None) -> GeoVertex:
        if isinstance(id, int):
            return self.__vertices[id]
        else:
            raise('输入的参数不是int型')

    '''通过两节点找边'''

    def find_edge(self, vertex_1: GeoVertex, vertex_2: GeoVertex) -> GeoEdge:
        conV = vertex_1.get_conVertex()
        index = conV.index(vertex_2)
        return vertex_1.get_conEdge()[index]
            
    '''利用BFS遍历从s到t的最短路径(无权图)'''

    def findpath_BFS(self, s: 'GeoVertex', t: 'GeoVertex') -> 'list[GeoVertex]':
        if s == t:
            return []
        resPath = []  # result
        '''use BFS to find the path'''
        openList = []  # Queue FIFO
        visitedVertex = {}  # is visited?
        searchVertex = {}  # key is the son node, value is the father node
        for key in self.__vertices.keys():
            visitedVertex[self.__vertices[key]] = False
            searchVertex[self.__vertices[key]] = None
        nextVertex = s
        openList.append(nextVertex)
        visitedVertex[nextVertex] = True
        while True:
            openList.remove(nextVertex)
            for v in nextVertex.get_conVertex():
                if not visitedVertex[v]:
                    openList.append(v)
                    visitedVertex[v] = True
                    # nextVertex is the father geoVertex
                    searchVertex[v] = nextVertex
                if v == t:
                    # find the path
                    resPath.append(t)
                    nextVertex = t
                    while searchVertex[nextVertex] is not None:
                        resPath.append(searchVertex[nextVertex])
                        nextVertex = searchVertex[nextVertex]
                    return resPath[::-1]
            if len(openList) == 0:
                # failure
                return None
            # get first geoVertex
            nextVertex = openList[0]

    '''非递归方法查找从s到t的所有路径'''

    def findAllPath(self, s: GeoVertex, t: GeoVertex) -> dict:
        '''build stack in order to get all path form s to t'''
        '''initialize'''
        mainStack = []  # main stack
        subStack = []  # second stack
        mainStack.append(s)
        nextNodeList = []
        for v in s.get_conVertex():
            nextNodeList.append(v)
        subStack.append(nextNodeList)
        temp = subStack.pop()
        if len(temp) == 0:
            return {}
        nextNode = temp[0]
        mainStack.append(temp.pop(0))
        subStack.append(temp)
        count = 0
        allPath = {}  # key is the number of road, value is the path
        nextNodeList = []
        for v in nextNode.get_conVertex():
            if v not in mainStack:
                nextNodeList.append(v)
        subStack.append(nextNodeList)
        while len(mainStack) != 0:
            if mainStack[-1] == t:
                # find one path and save
                count += 1
                allPath[count] = []
                for v in mainStack:
                    allPath[count].append(v)
                mainStack.pop()
                subStack.pop()
            nextNodeList = subStack.pop()
            if len(nextNodeList) != 0:
                nextNode = nextNodeList[0]
                mainStack.append(nextNodeList.pop(0))
                subStack.append(nextNodeList)
                nextNodeList = []
                for v in nextNode.get_conVertex():
                    if v not in mainStack:
                        nextNodeList.append(v)
                subStack.append(nextNodeList)
            else:
                mainStack.pop()
        return allPath

    '''利用pyshp画图'''

    def draw_geograph(self, outpath: str = '') -> None:
        # 字段
        for id in self.__vertices.keys():
            if len(self.__vertices[id].get_conVertex()) == 0:
                continue
            fields = list(self.__vertices[id].get_edgeAtt().values())[0].keys()
            break
        print(fields)
        '''
        w = shapefile.Writer(outpath, shapeType=3, encoding='utf-8')
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
    @staticmethod
    def constructGraph_deltaAngle(geoGraph: 'GeoGraph') -> 'GeoGraph':
        resGeoGraph = geoGraph
        for id in resGeoGraph.get_edges().keys():
            tempV = resGeoGraph.get_edges()[id]
            tempConV = tempV.get_conEdge()
            # 这种情况是孤点或者端点，不做处理
            if len(tempConV) == 0 or len(tempConV) == 1:
                continue
            deltaAngleDict = tempV.get_deltaAngle()

            # 查找变化角最小,且<pi/6的边
            minAngle = min(deltaAngleDict.values())
            if minAngle < np.pi/6:
                minEdge = min(deltaAngleDict, key=lambda x: deltaAngleDict[x])
                resGeoGraph.get_vertices()[id].set_conVertex(list(minEdge))
            else:
                resGeoGraph.get_vertices()[id].set_conVertex([])
        return resGeoGraph

    '''求和'''
    @staticmethod
    def getSumValue(valueStr):
        sum = 0.0
        for item in valueStr:
            sum = sum + item
        return sum

    '''求出现次数最多的字符串'''
    @staticmethod
    def getMostTimesValue(valueStr):
        hash = dict()
        for item in valueStr:
            if item in hash:
                hash[item] += 1
            else:
                hash[item] = 1

        return max(hash, key=hash.get)
