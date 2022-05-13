from GeoVertex import GeoVertex
from GeoEdge import GeoEdge
from GeoGraph import GeoGraph


graph = GeoGraph()
vertex_1 = GeoVertex(1)
vertex_2 = GeoVertex(2)
vertex_3 = GeoVertex(3)
vertex_4 = GeoVertex(4)

graph.add_vertex(1, vertex_1)
graph.add_vertex(2, vertex_2)
graph.add_vertex(3, vertex_3)
graph.add_vertex(4, vertex_4)
edge_1 = GeoEdge(12, vertex_1, vertex_2)
edge_2 = GeoEdge(23, vertex_2, vertex_3)
edge_3 = GeoEdge(34, vertex_3, vertex_4)
edge_4 = GeoEdge(41, vertex_4, vertex_1)
edge_5 = GeoEdge(5, vertex_1, vertex_1)
graph.add_edge(edge_1)
graph.add_edge(edge_2)
graph.add_edge(edge_3)
graph.add_edge(edge_4)
graph.add_edge(edge_5)
print(edge_4.get_con_edge())
print(edge_1.get_con_edge())
print(edge_5.get_con_edge())
edge_4.remove_con_edge(edge_5, vertex_1)
print(edge_4.get_con_edge())
print(edge_1.get_con_edge())
print(edge_5.get_con_edge())