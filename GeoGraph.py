from GeoVertex import GeoVertex
"""
GeoGraph Class
----------

由GeoVertex组成的简单地理图. 

"""


class GeoGraph():
    # 定义私有变量
    __vertices: dict  # 节点字典 {id1: vertex1, id2: vertex2, ...}
    __id: str  # 图名

    def __init__(self, id: str = '') -> None:
        self.__vertices = {}
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

    def get_vertices(self) -> 'list[GeoVertex]':
        return self.__vertices

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

    def add_edge(self, vertex_A: GeoVertex, vertex_B: GeoVertex, edgeAtt: dict = {}) -> None:
        vertex_A.add_conVertex(vertex_B, edgeAtt)


    def remove_edge(self, vertex_A: GeoVertex, vertex_B: GeoVertex) -> None:
        vertex_A.remove_conVertex(vertex_B)

    '''通过节点id查找节点'''

    def find_vertex(self, id: int = None) -> GeoVertex:
        if isinstance(id, int):
            return self.__vertices[id]
        else:
            raise('输入的参数不是int型')

    '''通过两节点找边'''

    def find_edge(self, vertex_1: GeoVertex = None, vertex_2: GeoVertex = None) -> dict:
        if isinstance(vertex_1, GeoVertex) and isinstance(vertex_2, GeoVertex):
            key = vertex_1.get_edgeAtt().keys()
            if (vertex_1, vertex_2) in key:
                return vertex_1.get_edgeAtt()[(vertex_1, vertex_2)]
            if (vertex_2, vertex_1) in key:
                return vertex_1.get_edgeAtt()[(vertex_2, vertex_1)]
        else:
            return None

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

    def __str__(self) -> str:
        return str(self.__id)

    def __repr__(self) -> str:
        return str(self.__id)