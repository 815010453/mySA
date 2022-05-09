from Vertex import Vertex
"""
Graph Class
----------

由vertex组成的简单图. 

"""


class Graph():
    # 定义私有变量
    __vertices: dict  # 节点字典 {id1: vertex1, id2: vertex2, ...}
    # 反转__vertices的key和value 构建节点字典 {vertex1: id1, vertex2: id2, ...}
    __vertices_reverse: dict
    __id: str  # 图名

    def __init__(self, id: str = '') -> None:
        self.__vertices = {}
        self.__vertices_reverse = {}
        self.__id = id

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

    '''节点的添加'''

    def add_vertex(self, id: int, vertex: Vertex) -> None:
        self.__vertices[id] = vertex
        self.__vertices_reverse[vertex] = id

    '''通过id删除节点'''

    def remove_vertex_id(self, id: int) -> None:
        del self.__vertices_reverse[self.__vertices[id]]
        del self.__vertices[id]

    '''通过vertex删除节点'''

    def remove_vertex_v(self, vertex: Vertex) -> None:
        del self.__vertices[self.__vertices_reverse[vertex]]
        del self.__vertices_reverse[vertex]

    '''图中边的添加与删除'''

    def add_edge(self, vertex_A: Vertex, vertex_B: Vertex, edgeAtt: dict = {}) -> None:
        vertex_A.add_conVertex(vertex_B, edgeAtt)

    def remove_edge(self, vertex_A: Vertex, vertex_B: Vertex) -> None:
        vertex_A.remove_conVertex(vertex_B)

    '''通过节点id查找节点'''

    def find_vertex(self, id: int = None) -> Vertex:
        if isinstance(id, int):
            return self.__vertices[id]
        else:
            raise('输入的参数不是int型')

    '''通过vertex查找节点id'''

    def find_vertex_id(self, vertex: Vertex = None) -> int:
        if isinstance(vertex, Vertex):
            return self.__vertices_reverse[vertex]
        else:
            return None

    '''通过两节点或节点号找边'''

    def find_edge(self, vertex_1: Vertex = None, vertex_2: Vertex = None, id1: int = None, id2: int = None) -> dict:
        if isinstance(id1, int):
            vertex_1 = self.find_vertex_id(id1)
        if isinstance(id2, int):
            vertex_2 = self.find_vertex_id(id2)
        if isinstance(vertex_1, Vertex) and isinstance(vertex_2, Vertex):
            key = vertex_1.get_edgeAtt().keys()
            if (vertex_1, vertex_2) in key:
                return vertex_1.get_edgeAtt()[(vertex_1, vertex_2)]
            if (vertex_2, vertex_1) in key:
                return vertex_1.get_edgeAtt()[(vertex_2, vertex_1)]
        else:
            return None

    '''利用BFS遍历从s到t的最短路径(无权图)'''

    def findpath_BFS(self, s: 'Vertex', t: 'Vertex') -> 'list[Vertex]':
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
