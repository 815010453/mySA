from GeoVertex import GeoVertex
from GeoEdge import GeoEdge
from GeoGraph import GeoGraph

x = {1: []}  # {1: [2, 3], 2: []}
y = {1: [], 2: []}
z = {1: [3], 2: [4]}
a = x.keys()
if len(x.keys()) == 1:
    a = list(x.keys())[0]
elif (not list(x.values())[0] and list(x.values())[1]) or (not list(x.values())[1] and list(x.values())[0]):
    if list(x.values())[0]:
        a = x.keys()

print(a)
