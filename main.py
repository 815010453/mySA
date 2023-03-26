# -*- coding:utf-8 -*-
import math

import numpy as np
from sklearn.cluster import KMeans

from GeoVertex import GeoVertex
from GeoEdge import GeoEdge
from GeoGraph import GeoGraph
import datetime

if __name__ == '__main__':
    '''time_s = datetime.datetime.now()
    myGraph = GeoGraph('TW')
    myGraph.constructGraph_edge('data/cd_road/cd_road_processed.shp')
    time_m = datetime.datetime.now()
    print('构建花费时间:', (time_m - time_s).total_seconds(), '秒')
    # my_dict = myGraph.reconstruct_edge_min_delta_angle(math.pi / 6)
    my_dict = myGraph.reconstruct_edge_sa(100, 0.99)
    time_e = datetime.datetime.now()
    print('重建相邻关系花费时间:', (time_e - time_m).total_seconds(), '秒')
    print(len(my_dict.keys()))
    time_m = datetime.datetime.now()
    myGraph.draw_geograph_roads('out/cd_road/cd_sa.shp', my_dict)
    time_e = datetime.datetime.now()
    print('绘制花费时间:', (time_e - time_m).total_seconds(), '秒')'''

    time_s = datetime.datetime.now()
    myGraph = GeoGraph('CHN')
    myGraph.constructGraph_polygon('data/shi_polygon/Export_Output.shp')
    time_m = datetime.datetime.now()
    print('构建花费时间:', (time_m - time_s).total_seconds(), '秒')
    myGraph.my_kmeans('R_densit_3', 2)
    myGraph.spatial_constraints('R_densit_3')
    myGraph.draw_geograph_polygons('out/shi_polygon/output.shp', 'R_densit_3')

    '''
    myGraph = GeoGraph('Test')
    vertices = []
    vertex = GeoVertex(1, {}, (0, 1))
    vertices.append(vertex)
    vertex = GeoVertex(2, {}, (2, 1))
    vertices.append(vertex)
    vertex = GeoVertex(3, {}, (1, 2))
    vertices.append(vertex)
    vertex = GeoVertex(4, {}, (0, 0))
    vertices.append(vertex)
    vertex = GeoVertex(5, {}, (2, 0))
    vertices.append(vertex)
    vertex = GeoVertex(6, {}, (0, 2))
    vertices.append(vertex)
    vertex = GeoVertex(7, {}, (2, 2))
    vertices.append(vertex)

    count = 1
    edge = GeoEdge(e_id=count, edge_att={}, vertex_a=vertices[0], vertex_b=vertices[1])
    myGraph.add_edge(edge)

    count += 1
    edge = GeoEdge(e_id=count, edge_att={}, vertex_a=vertices[0], vertex_b=vertices[2])
    myGraph.add_edge(edge)

    count += 1
    edge = GeoEdge(e_id=count, edge_att={}, vertex_a=vertices[0], vertex_b=vertices[3])
    myGraph.add_edge(edge)

    count += 1
    edge = GeoEdge(e_id=count, edge_att={}, vertex_a=vertices[1], vertex_b=vertices[2])
    myGraph.add_edge(edge)

    count += 1
    edge = GeoEdge(e_id=count, edge_att={}, vertex_a=vertices[1], vertex_b=vertices[4])
    myGraph.add_edge(edge)

    count += 1
    edge = GeoEdge(e_id=count, edge_att={}, vertex_a=vertices[3], vertex_b=vertices[4])
    myGraph.add_edge(edge)

    count += 1
    edge = GeoEdge(e_id=count, edge_att={}, vertex_a=vertices[0], vertex_b=vertices[5])
    myGraph.add_edge(edge)

    count += 1
    edge = GeoEdge(e_id=count, edge_att={}, vertex_a=vertices[1], vertex_b=vertices[-1])
    myGraph.add_edge(edge)

    vertex1 = myGraph.find_vertex_id(1)
    vertex2 = myGraph.find_vertex_id(4)
    # my_dict = myGraph.reconstruct_edge_min_delta_angle(math.pi / 6)
    my_dict = myGraph.reconstruct_edge_sa(100, 0.9)
    print(my_dict)
    time_m = datetime.datetime.now()
    path = myGraph.findPath_bfs(vertex1, vertex2)
    print('The shortest path from ' + str(vertex1) + ' to ' + str(vertex2) + ' is :' + str(path))
    paths = myGraph.findAllPath(vertex1, vertex2)
    print('The paths from ' + str(vertex1) + ' to ' + str(vertex2) + ' are :')
    count = 1
    for p in paths:
        print(str(count) + ': ' + str(p))
        count += 1
    time_e = datetime.datetime.now()
    print('查询花费时间:', (time_e - time_m).total_seconds(), '秒')'''
