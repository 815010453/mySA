from Vertex import Vertex
from Edge import Edge
from Graph import Graph
import datetime
import numpy as np
import shapefile  # 使用pyshp
from osgeo import osr
import os
import pickle
import sys
import traceback
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


'''图的构建与保存'''


def init_graph(nodePath, edgePath, graphName) -> str:
    # 设置系统最大递归深度
    sys.setrecursionlimit(20000)
    '''所有的点构成一张图'''
    '''开始构建图'''
    graph = Graph('TW_graph')
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
            tempdict = dict(zip(keyList, item))
            if count % 100000 == 0:
                print(tempdict)
            temp = Vertex(id=tempdict['id'], coord=nodeFile.shape(
                count).points, att=tempdict)
            graph.add_vertex(key=tempdict['id'], vertex=temp)
            count += 1
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
            tempdict = dict(zip(keyList, item))
            if count % 100000 == 0:
                print(tempdict)
            vertex_A = graph.find_vertex(tempdict['from_'])
            vertex_B = graph.find_vertex(tempdict['to'])
            temp = Edge(id=tempdict['keyId'], coord=edgeFile.shape(
                count).points, att=tempdict, vertex_A=vertex_A, vertex_B=vertex_B)
            '''在图中添加该边'''
            graph.add_edge(vertex_A, vertex_B, temp)
            count += 1
    if graph.check_graph():

        
        return [graph, 'construct graph successfully']
        
    else:
        return [None, 'construct graph unsuccessfully, please check your code!']


if __name__ == '__main__':
    time_s = datetime.datetime.now()
    [graph, msg] = init_graph('T_ROAD/Desktop/T_ROAD_NODE_webmerc.shp',
                     'T_ROAD/T_ROAD_webmerc.shp', 'TWgraph')
    
    time_e = datetime.datetime.now()
    print(msg)
    print('构建花费时间:',(time_e-time_s).total_seconds(), '秒')
    vertex_A = graph.find_vertex(1)
    vertex_B = graph.find_vertex(2871)
    vertex_C = graph.find_vertex(281)

    print(graph.find_edge(vertex_A, vertex_B))
    print(graph.findpath_BFS(vertex_A, vertex_C))
