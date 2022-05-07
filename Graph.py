from Vertex import Vertex
from Edge import Edge
"""
Graph Class
----------

由vertex组成的简单图. 

"""


class Graph():
    # 定义私有变量
    __vertices: dict  # 节点字典 {keyid1: vertex1, keyid2: vertex2}
    __id: str  # 图名
    __edge: dict  # 边字典{(v1, v2): edge1, (v2, v3): edge2}

    def __init__(self, id: str = '') -> None:
        self.__vertices = {}
        self.__id = id
        self.__edge = {}

    '''检查该图是否合法'''

    def check_graph(self) -> bool:
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
        '''检查边是否合法 由两个点构成的唯一边'''
        for id in self.__edge.keys():
            tempValue = self.__edge[id]
            if len(id) != 2:
                return False
            judge = {}
            if tempValue not in judge.keys():
                judge[tempValue] = 1
            else:
                return False
            '''检查相邻边是否正确'''
            for i in tempValue.get_conEdge():
                if tempValue not in i.get_conEdge():
                    return False
            node = tempValue.get_vertices()
            if id != node and id.reverse() != node:
                return False
        return True
    '''
    这些都是私有变量的设置方法 set与get
    '''

    def get_vertices(self) -> 'list[Vertex]':
        return self.__vertices

    def get_id(self) -> str:
        return self.__id

    def set_id(self, id: str) -> None:
        self.__id = id

    '''节点的添加与删除'''

    def add_vertex(self, key: int, vertex: Vertex) -> None:
        self.__vertices[key] = vertex

    def remove_vertex(self, vertex: Vertex) -> None:
        self.__vertices.remove(vertex)

    '''图中边的添加与删除'''

    def add_edge(self, vertex_A: Vertex, vertex_B: Vertex, edge: Edge) -> None:
        vertex_A.add_conVertex(vertex_B)
        self.__edge[(vertex_A, vertex_B)] = edge

    def remove_edge(self, vertex_A: Vertex, vertex_B: Vertex, edge: Edge) -> None:
        vertex_A.remove_conVertex(vertex_B)
        del edge
        if (vertex_A, vertex_B) in self.__edge.keys():
            del self.__edge[(vertex_A, vertex_B)]
        if (vertex_B, vertex_A) in self.__edge.keys():
            del self.__edge[(vertex_B, vertex_A)]

    '''通过节点号查找节点'''

    def find_vertex(self, id: str = '') -> Vertex:
        return self.__vertices[id]

    '''通过(节点号1, 节点号2)查找边'''

    def find_edge(self, vertex_A, vertex_B) -> Edge:
        if (vertex_A, vertex_B) in self.__edge.keys():
            return self.__edge[(vertex_A, vertex_B)]
        if (vertex_B, vertex_A) in self.__edge.keys():
            return self.__edge[(vertex_B, vertex_A)]
        else:
            return None

    '''利用BFS遍历从s到t的最短路径'''

    def findpath_BFS(self, s: 'Vertex', t: 'Vertex') -> 'list[Vertex]':
        if s == t:
            return []
        resPath = []  # result
        '''use BFS to find the path'''
        openList = []  # Queue FIFO
        visitedVertex = {}  # is visited?
        searchVertex = {}  # key is the son node, value is the father node
        for key in self.__vertices:
            visitedVertex[key] = False
            searchVertex[key] = None
        nextVertex = s
        openList.append(nextVertex)
        visitedVertex[nextVertex] = True
        while True:
            openList.remove(nextVertex)
            for v in nextVertex.get_conVertex():
                if not visitedVertex[v]:
                    openList.append(v)
                    visitedVertex[v] = True
                    # nextVertex is the father vertex
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
            # get first vertex
            nextVertex = openList[0]

    '''非递归方法查找从s到t的所有路径'''

    def findAllPath(self, s: Vertex, t: Vertex) -> dict:
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

    def __str__(self) -> str:
        return str(self.__id)

    def __repr__(self) -> str:
        return str(self.__id)
