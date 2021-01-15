class Node:

    def __init__(self, name):
        self.name = name
        self.ribs = {}

    def addRib(self, node, weight = 1):
        self.ribs[node] = weight

    def delRib(self, node):
        self.ribs.pop(node, None)

    def getRib(self, node, ret = None):
        return self.ribs.get(node, ret)

    def sort(self):
        sort_ribs = {}
        for k in sorted(self.ribs.keys()):
            sort_ribs[k] = self.ribs[k]
        self.ribs = sort_ribs

    def __str__(self):
        return str(self.ribs)