class Vertex:

    def __init__(self, name):
        self.name = name
        self.edges = {}

    def addEdge(self, vertex, weight = 1):
        self.edges[vertex] = weight

    def delEdge(self, vertex):
        self.edges.pop(vertex, None)

    def getEdge(self, vertex, ret = None):
        return self.edges.get(vertex, ret)

    def sort(self):
        sort_edges = {}
        for k in sorted(self.edges.keys()):
            sort_edges[k] = self.edges[k]
        self.edges = sort_edges

    def __str__(self):
        return str(self.edges)