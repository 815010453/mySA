from GeoVertex import GeoVertex
from GeoGraph import GeoGraph
import datetime
import numpy as np
import shapefile  # 使用pyshp
from osgeo import osr
import os
import sys
# gdal对应的proj.db在这个文件夹下
os.environ['PROJ_LIB'] = 'D:\\anaconda3\\Lib\\site-packages\\osgeo\\data\\proj'

'''
求和
'''


def getSumValue(valueStr):
    sum = 0.0
    for item in valueStr:
        sum = sum + item
    return sum


'''
求出现次数最多的字符串
'''


def getMostTimesValue(valueStr):
    hash = dict()
    for item in valueStr:
        if item in hash:
            hash[item] += 1
        else:
            hash[item] = 1

    return max(hash, key=hash.get)


'''图的构建'''


def init_graph(nodePath, edgePath, graphName) -> str:
    # 设置系统最大递归深度
    sys.setrecursionlimit(20000)
    '''所有的点构成一张图'''
    '''开始构建图'''
    geoGraph = GeoGraph('TW_graph')
    '''读取边和点的shapefile文件'''
    '''构建节点类'''
    with shapefile.Reader(nodePath, encoding='utf-8') as nodeFile:
        # 读取属性
        allRecords = nodeFile.records()
        keyList = []  # 字段名
        for i in nodeFile.fields:
            keyList.append(i[0])
        # 不需要第0个字段名
        del keyList[0]
        count = 0
        for item in allRecords:
            # 创建节点
            # 将key和对应的value打包成一个字典
            tempDict = dict(zip(keyList, item))
            if count % 100000 == 0:
                print(tempDict)
            # 通过id和坐标构建该点
            temp = GeoVertex(id=tempDict['id'], coord=nodeFile.shape(
                count).points, att=tempDict)
            geoGraph.add_vertex(id=tempDict['id'], geoVertex=temp)
            count += 1
    '''构建点与点之间的相邻关系（构建边）'''
    with shapefile.Reader(edgePath, encoding='utf-8') as edgeFile:
        # 读取属性
        allRecords = edgeFile.records()
        keyList = []  # 字段名
        for i in edgeFile.fields:
            keyList.append(i[0])
        print(keyList)
        # 不需要第0个字段名
        del keyList[0]
        count = 0
        for item in allRecords:
            # 创建边
            # 将key和对应的value打包成一个字典
            tempDict = dict(zip(keyList, item))
            if count % 100000 == 0:
                print(tempDict)
            vertex_A = geoGraph.find_vertex(int(tempDict['from_']))
            vertex_B = geoGraph.find_vertex(int(tempDict['to']))
            '''记录该边坐标'''
            tempDict['coord'] = edgeFile.shape(count).points

            '''在图中添加该边'''
            geoGraph.add_edge(vertex_A, vertex_B, tempDict)
            count += 1
    if geoGraph.check_graph_simple():

        return [geoGraph, 'construct geoGraph successfully']

    else:
        return [None, 'construct geoGraph unsuccessfully, please check your code!']


if __name__ == '__main__':
    time_s = datetime.datetime.now()
    geoGraph = GeoGraph()
    [geoGraph, msg] = init_graph('T_ROAD/Desktop/T_ROAD_NODE_webmerc.shp',
                              'T_ROAD/T_ROAD_webmerc.shp', 'TWgraph')

    time_e = datetime.datetime.now()
    print(msg)
    print('构建花费时间:', (time_e-time_s).total_seconds(), '秒')
    vertex_A = geoGraph.find_vertex(1)
    vertex_B = geoGraph.find_vertex(2871)
    vertex_C = geoGraph.find_vertex(1000)
    print('A, id:', vertex_A.get_id())
    print('B, id:', vertex_B.get_id())
    print('C, id:', vertex_C.get_id())
    
    print('A, coord:', vertex_A.get_coord())
    print('A, 节点:', vertex_A.get_nodeAtt())
    print('A, 相邻点:', vertex_A.get_conVertex())
    print('A, 连接边:', vertex_A.get_edgeAtt())
    print('A, 变化角:',vertex_A.get_deltaAngle())

    print(geoGraph.find_edge(vertex_A, vertex_B))
    print(geoGraph.findpath_BFS(vertex_A, vertex_C))
