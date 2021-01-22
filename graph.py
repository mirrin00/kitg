import json
from vertex import Vertex

class GraphError(BaseException):
    pass

class Graph:

    def __init__(self):
        self.vertices = {}
        self.is_oriented = False

    def addEdge(self, edge, weight = 1):
        vertex_start = self.vertices.get(edge[0])
        vertex_end = self.vertices.get(edge[1])
        if vertex_start == None:
            raise GraphError(f"No vertex {edge[0]} in graph")
        if vertex_end == None:
            raise GraphError(f"No vertex {edge[1]} in graph")
        if self.is_oriented:
            vertex_start.addEdge(edge[1], weight)
        else:
            vertex_start.addEdge(edge[1], weight)
            vertex_end.addEdge(edge[0], weight)

    def removeEdge(self, edge):
        vertex_start = self.vertices.get(edge[0])
        vertex_end = self.vertices.get(edge[1])
        if vertex_start == None:
            raise GraphError(f"No vertex {edge[0]} in graph")
        if vertex_end == None:
            raise GraphError(f"No vertex {edge[1]} in graph")
        if self.is_oriented:
            self.vertices[vertex_start].edges.pop(vertex_end, None)
        else:
            self.vertices[vertex_start].edges.pop(vertex_end, None)
            self.vertices[vertex_end].edges.pop(vertex_start, None)

    def removeVertex(self, vertex):
        if vertex not in self.vertices.keys():
            raise GraphError(f'No vertex {vertex} in graph')
        self.vertices.pop(vertex, None)
        for v in self.vertices.values():
            v.edges.pop(vertex, None)

    def clearEdges(self):
        for vertex in self.vertices.values():
            vertex.edges.clear()


    def loadFromJSON(self, file):
        with open(file, 'r') as f:
            data = json.load(f)
        self.is_oriented = data["oriented"]
        for vertex in data["vertices"]:
            self.vertices[vertex] = Vertex(vertex)
        edges = data["edges"]
        for key in edges.keys():
            for edge in edges[key]:
                if type(edge) == list:
                    self.addEdge((key, edge[0]), edge[1])
                else:
                    self.addEdge((key, edge))
        sort_vertices = {}
        for key in sorted(self.vertices.keys()):
            self.vertices[key].sort()
            sort_vertices[key] = self.vertices[key]
        self.vertices = sort_vertices

    def print(self):
        print("Graph:\nis_oriented", self.is_oriented)
        print("vertices: ", self.vertices.keys())
        print("edges:")
        for k in self.vertices.keys():
            print(k,self.vertices[k])