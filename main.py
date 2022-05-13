# coding=utf-8
from GeoVertex import GeoVertex
from GeoEdge import GeoEdge
from GeoGraph import GeoGraph
import datetime
import shapefile  # 使用pyshp

'''图的构建'''


def init_graph(node_path, edge_path, graph_name) -> GeoGraph:
    """所有的点构成一张图"""
    '''开始构建图'''
    geo_graph = GeoGraph(graph_name)
    '''读取边和点的shapefile文件'''
    '''构建节点类'''
    with shapefile.Reader(node_path, encoding='utf-8') as nodeFile:
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
            temp = GeoVertex(v_id=temp_dict['id'], coord=nodeFile.shape(
                count).points, att=temp_dict)
            geo_graph.add_vertex(geo_vertex=temp)
            count += 1
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
            temp_edge = GeoEdge(e_id=temp_dict['keyId'], coord=edgeFile.shape(
                count).points, edge_att=temp_dict, vertex_a=vertex_a, vertex_b=vertex_b)
            '''在图中添加该边'''
            geo_graph.add_edge(temp_edge)
            count += 1
    # 通过最小变化角重建该图边的相邻关系
    geo_graph.reconstruct_edge_min_delta_angle()
    print(geo_graph.check_graph_simple())

    print('construct geo_graph successfully')
    return geo_graph


if __name__ == '__main__':
    time_s = datetime.datetime.now()
    geoGraph = init_graph('T_ROAD/Desktop/T_ROAD_NODE_webmerc.shp',
                          'T_ROAD/T_ROAD_webmerc.shp', 'TWgraph')

    time_e = datetime.datetime.now()
    print('构建花费时间:', (time_e - time_s).total_seconds(), '秒')
    '''
    vertex_a = geoGraph.find_vertex(1)
    vertex_b = geoGraph.find_vertex(2871)
    vertex_C = geoGraph.find_vertex(1000)
    print('A, v_id:', vertex_a.get_id())
    print('B, v_id:', vertex_b.get_id())
    print('C, v_id:', vertex_C.get_id())

    print('A, coord:', vertex_a.get_coord())
    print('A, 节点:', vertex_a.get_node_att())
    print('A, 相邻点:', vertex_a.get_con_vertex())
    print('A, 相邻边', vertex_a.get_con_edge())

    print(geoGraph.find_edge(vertex_a, vertex_b))
    print(geoGraph.findpath_bfs(vertex_a, vertex_C))
    '''
    edge_A = geoGraph.find_edge_id(483)
    edge_B = geoGraph.find_edge_id(16833)
    edge_C = geoGraph.find_edge_id(16836)

    print('A, e_id:', edge_A.get_id())
    print('A, coord:', edge_A.get_coord())
    print('A, 边:', edge_A.get_edge_att())
    print('A, 相邻边', edge_A.get_con_edge())
    print(edge_A.get_delta_angle())

    print('B, e_id:', edge_B.get_id())
    print('B, coord:', edge_B.get_coord())
    print('B, 边:', edge_B.get_edge_att())
    print('B, 相邻边', edge_B.get_con_edge())
    print(edge_B.get_delta_angle())

    print('C, e_id:', edge_C.get_id())
    print('C, coord:', edge_C.get_coord())
    print('C, 边:', edge_C.get_edge_att())
    print('C, 相邻边', edge_C.get_con_edge())
    print(edge_C.get_delta_angle())

'''
    deltaAngleGeoGraph=GeoGraph.constructGraph_deltaAngle(geoGraph)

    vertex_a = deltaAngleGeoGraph.find_vertex(281)
    vertex_b = deltaAngleGeoGraph.find_vertex(1)
    vertex_C = deltaAngleGeoGraph.find_vertex(2871)
    print('A, v_id:', vertex_a.get_id())
    print('B, v_id:', vertex_b.get_id())
    print('C, v_id:', vertex_C.get_id())
    
    print('A, coord:', vertex_a.get_coord())
    print('A, 节点:', vertex_a.get_node_att())
    print('A, 相邻点:', vertex_a.get_con_vertex())


    print(deltaAngleGeoGraph.find_edge(vertex_C, vertex_b))
    print(deltaAngleGeoGraph.findpath_bfs(vertex_a, vertex_C))
    print(deltaAngleGeoGraph.find_all_path(vertex_a,vertex_C))
    print(deltaAngleGeoGraph.draw_geograph())
'''
