# coding=utf-8
from GeoVertex import GeoVertex
from GeoEdge import GeoEdge
from GeoGraph import GeoGraph
import datetime
import shapefile  # 使用pyshp

'''图的构建'''


def init_graph(nodePath, edgePath, graphName) -> GeoGraph:
    """所有的点构成一张图"""
    '''开始构建图'''
    geo_graph = GeoGraph(graphName)
    '''读取边和点的shapefile文件'''
    '''构建节点类'''
    with shapefile.Reader(nodePath, encoding='utf-8') as nodeFile:
        # 读取属性
        all_records = nodeFile.records()
        key_list = []  # 字段名
        for i in nodeFile.fields:
            key_list.append(i[0])
        # 不需要第0个字段名
        del key_list[0]
        count = 0
        for item in all_records:
            # 创建节点
            # 将key和对应的value打包成一个字典
            temp_dict = dict(zip(key_list, item))
            if count % 100000 == 0:
                print(temp_dict)
            # 通过id和坐标构建该点
            temp = GeoVertex(id=temp_dict['id'], coord=nodeFile.shape(
                count).points, att=temp_dict)
            geo_graph.add_vertex(id=temp_dict['id'], geoVertex=temp)
            count += 1
    '''构建点与点之间的相邻关系以及构建边'''
    with shapefile.Reader(edgePath, encoding='utf-8') as edgeFile:
        # 读取属性
        all_records = edgeFile.records()
        key_list = []  # 字段名
        for i in edgeFile.fields:
            key_list.append(i[0])
        print(key_list)
        # 不需要第0个字段名
        del key_list[0]
        count = 0
        for item in all_records:
            # 创建边
            # 将key和对应的value打包成一个字典
            temp_dict = dict(zip(key_list, item))

            if count % 100000 == 0:
                print(temp_dict)
            vertex_a = geo_graph.find_vertex(int(temp_dict['from_']))
            vertex_b = geo_graph.find_vertex(int(temp_dict['to']))
            # 构建该边
            temp_edge = GeoEdge(id=temp_dict['keyId'], coord=edgeFile.shape(
                count).points, edgeAtt=temp_dict, vertex_A=vertex_a, vertex_B=vertex_b)
            '''在图中添加该边'''
            geo_graph.add_edge(vertex_a, vertex_b, temp_edge)
            count += 1
    # geo_graph.construct_Edge_minDeltaAngle()
    print('construct geo_graph successfully')
    return geo_graph


if __name__ == '__main__':
    time_s = datetime.datetime.now()
    geoGraph = init_graph('T_ROAD/Desktop/T_ROAD_NODE_webmerc.shp',
                          'T_ROAD/T_ROAD_webmerc.shp', 'TWgraph')

    time_e = datetime.datetime.now()
    print('构建花费时间:', (time_e - time_s).total_seconds(), '秒')
    '''
    vertex_A = geoGraph.find_vertex(1)
    vertex_B = geoGraph.find_vertex(2871)
    vertex_C = geoGraph.find_vertex(1000)
    print('A, id:', vertex_A.get_id())
    print('B, id:', vertex_B.get_id())
    print('C, id:', vertex_C.get_id())

    print('A, coord:', vertex_A.get_coord())
    print('A, 节点:', vertex_A.get_nodeAtt())
    print('A, 相邻点:', vertex_A.get_conVertex())
    print('A, 相邻边', vertex_A.get_conEdge())

    print(geoGraph.find_edge(vertex_A, vertex_B))
    print(geoGraph.findpath_BFS(vertex_A, vertex_C))
    '''
    vertex_A = geoGraph.find_vertex(312)
    print('A, coord:', vertex_A.get_coord())
    print('A, 节点:', vertex_A.get_nodeAtt())
    print('A, 相邻点:', vertex_A.get_conVertex())
    print('A, 相邻边', vertex_A.get_conEdge())
    edge_A = geoGraph.find_edge_id(483)
    edge_B = geoGraph.find_edge_id(484)

    print('A, id:', edge_A.get_id())
    print('A, coord:', edge_A.get_coord())
    print('A, 节点:', edge_A.get_edgeAtt())
    print('A, 相邻边', edge_A.get_conEdge())
    print(edge_A.get_deltaAngle())

    print('B, id:', edge_B.get_id())
    print('B, coord:', edge_B.get_coord())
    print('B, 节点:', edge_B.get_edgeAtt())
    print('B, 相邻边', edge_B.get_conEdge())
    print(edge_B.get_deltaAngle())

'''
    deltaAngleGeoGraph=GeoGraph.constructGraph_deltaAngle(geoGraph)

    vertex_A = deltaAngleGeoGraph.find_vertex(281)
    vertex_B = deltaAngleGeoGraph.find_vertex(1)
    vertex_C = deltaAngleGeoGraph.find_vertex(2871)
    print('A, id:', vertex_A.get_id())
    print('B, id:', vertex_B.get_id())
    print('C, id:', vertex_C.get_id())
    
    print('A, coord:', vertex_A.get_coord())
    print('A, 节点:', vertex_A.get_nodeAtt())
    print('A, 相邻点:', vertex_A.get_conVertex())


    print(deltaAngleGeoGraph.find_edge(vertex_C, vertex_B))
    print(deltaAngleGeoGraph.findpath_BFS(vertex_A, vertex_C))
    print(deltaAngleGeoGraph.findAllPath(vertex_A,vertex_C))
    print(deltaAngleGeoGraph.draw_geograph())
'''
