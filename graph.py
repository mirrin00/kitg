import json
from node import Node

class GraphError(BaseException):
    pass

class Graph:

    def __init__(self):
        self.nodes = {}
        self.is_oriented = False

    def addRib(self, rib, is_oriented, weight = 1):
        node_start = self.nodes.get(rib[0])
        node_end = self.nodes.get(rib[1])
        if node_start == None:
            raise GraphError(f"No node {rib[0]} in graph")
        if node_end == None:
            raise GraphError(f"No node {rib[1]} in graph")
        if self.is_oriented:
            node_start.addRib(rib[1], weight)
        else:
            node_start.addRib(rib[1], weight)
            node_end.addRib(rib[0], weight)

    def loadFromJSON(self, file):
        with open(file, 'r') as f:
            data = json.load(f)
        self.is_oriented = data["oriented"]
        for node in data["nodes"]:
            self.nodes[node] = Node(node)
        ribs = data["ribs"]
        for key in ribs.keys():
            for rib in ribs[key]:
                if type(rib) == list:
                    self.addRib((key, rib[0]), self.is_oriented, rib[1])
                else:
                    self.addRib((key, rib), self.is_oriented)
        sort_nodes = {}
        for key in sorted(self.nodes.keys()):
            self.nodes[key].sort()
            sort_nodes[key] = self.nodes[key]
        self.nodes = sort_nodes

    def print(self):
        print("Graph:\nis_oriented", self.is_oriented)
        print("nodes: ", self.nodes.keys())
        print("ribs:")
        for k in self.nodes.keys():
            print(k,self.nodes[k])