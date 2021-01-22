import json

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

def kosaraju_sharir(graph):
    if graph.is_oriented == False:
        raise GraphError("Algorithm Kosaraju: Graph is not oriented")
    times = {}
    time = 0
    def find(vertex_name, times, time):
        times[vertex_name] = -1
        time += 1
        for vertex in graph.vertices[vertex_name].edges.keys():
            if vertex in times.keys():
                continue
            time = find(vertex, times, time)
        time += 1
        times[vertex_name] = time
        return time
    for vertex in sorted(graph.vertices.keys()):
        if vertex not in times.keys():
            time = find(vertex, times, time)
    times = {k: v for k, v in sorted(times.items(), key=lambda item: item[1], reverse=True)}
    def find_components(vertex_name, comp, times):
        times[vertex_name] = -1
        comp.append(vertex_name)
        for vertex in times.keys():
            if times[vertex] != -1 and vertex_name in graph.vertices[vertex].edges.keys():
                find_components(vertex, comp, times)
    components = []
    for vertex in times.keys():
        if times[vertex] != -1:
            component = []
            find_components(vertex, component, times)
            components.append(component)
    print("Result Kosaraju:")
    for comp in components:
        print(comp)

def dijkstra(graph, start_vertex_name):
    for k in graph.vertices.keys():
        for r, v in graph.vertices[k].edges.items():
            if v < 0:
                raise GraphError(f"Algorithm Dijsktra: Graph has negative edge")
    if start_vertex_name not in graph.vertices.keys():
        raise GraphError(f"Algorithm Dijsktra: Vertex {start_vertex_name} not in graph")
    start_vertex = graph.vertices[start_vertex_name]
    paths = {k: [start_vertex.getEdge(k, -1), start_vertex_name] for k in sorted(graph.vertices.keys())}
    paths.pop(start_vertex_name)
    for k in paths.keys():
        print(f"  {k}  ",end='|')
    print()
    for v in paths.values():
        if v[0] == -1:
            print(" inf ", end='|')
        else:
            print(f"{v[0]:3}/{v[1]}",end='|')
    print()
    while True:
        minimum = -1
        vertex = ''
        for vertex_name, path in paths.items():
            if path[0] != None and (path[0] < minimum or minimum == -1) and path[0] != -1:
                minimum = path[0]
                vertex = vertex_name
        if minimum == -1:
            break
        for vertex_name, len_vertex in graph.vertices[vertex].edges.items():
            if vertex_name != start_vertex_name and paths[vertex_name][0] != None and (paths[vertex_name][0] > (minimum + len_vertex) or paths[vertex_name][0] == -1):
                paths[vertex_name] = [minimum + len_vertex, vertex]
        paths[vertex][0] = None
        for v in paths.values():
            if v[0] == -1:
                print(" inf ", end='|')
            elif v[0] == None:
                print("     ", end='|')
            else:
                print(f"{v[0]:3}/{v[1]}", end='|')
        print()
    print("\nEnd Dijsktra")

def floyd(graph):
    tabl = []
    keys = graph.vertices.keys()
    for k in keys:
        row = []
        vertex = graph.vertices[k]
        for col in keys:
            if k == col:
                row.append(0)
            else:
                row.append(vertex.getEdge(col))
        tabl.append(row)
    def print_tabl(tabl, keys, index):
        print("     ", end='|')
        for k in keys:
            print(f"  {k}  ", end = '|')
        print()
        for i in range(len(tabl)):
            print(f"  {list(keys)[i]}  ", end='|')
            for j in range(len(tabl)):
                if tabl[i][j] == None:
                    print(" inf ", end = '|')
                else:
                    print(f" {tabl[i][j]:3} ", end='|')
            if i == index:
                print("|||")
            else:
                print()
        print("     ", end=" ")
        for j in range(len(tabl)):
            if j == index:
                print(" ||| ", end = " ")
            else:
                print("     ", end=" ")
        print()
    for number in range(len(tabl)):
        print_tabl(tabl, keys, number)
        print("\n\n")
        for i in range(len(tabl)):
            for j in range(len(tabl)):
                if tabl[i][number] == None or tabl[number][j] == None:
                    continue
                if tabl[i][j] == None or tabl[i][number] + tabl[number][j] < tabl[i][j]:
                    tabl[i][j] = tabl[i][number] + tabl[number][j]
        for i in range(len(tabl)):
            if tabl[i][i] != 0:
                raise GraphError("Algorithm Floyd: Graph has negative loop")
    print("Result Floyd:")
    print_tabl(tabl,keys, -1)

def max_flow(graph, source, target):
    flow = {}
    if source not in graph.vertices.keys():
        raise GraphError(f"Algorithm Max Flow: No vertex {source} in graph")
    if target not in graph.vertices.keys():
        raise GraphError(f"Algorithm Max Flow: No vertex {target} in graph")
    for k in graph.vertices.keys():
        for r, v in graph.vertices[k].edges.items():
            if v < 0:
                raise GraphError(f"Algorithm Max Flow: Graph has negative edge")
            flow[(k,r)] = 0
    while True:
        labels = {source: None}
        checked = [source]
        not_checked = list(graph.vertices.keys())
        not_checked.remove(source)
        for vertex_checked in checked:
            temp_checked = []
            for vertex in not_checked:
                if vertex in temp_checked:
                    continue
                if flow.get((vertex_checked, vertex), 0) < graph.vertices[vertex_checked].getEdge(vertex, 0) or flow.get((vertex, vertex_checked), 0) > 0:
                    temp_checked.append(vertex)
                    labels[vertex] = vertex_checked
            checked.extend(temp_checked)
            for el in temp_checked:
                not_checked.remove(el)
        if target in not_checked:
            break
        else:
            mins = []
            vertex = target
            while vertex != source:
                prev_vertex = labels[vertex]
                if graph.vertices[prev_vertex].getEdge(vertex, 0) - flow.get((prev_vertex, vertex), 0) > 0:
                    mins.append(graph.vertices[prev_vertex].getEdge(vertex, 0) - flow.get((prev_vertex, vertex), 0))
                elif flow.get((vertex,prev_vertex),0) > 0:
                    mins.append(flow.get((vertex,prev_vertex),0))
                vertex = prev_vertex
            mins = min(mins)
            cur_way = [target]
            vertex = target
            while vertex != source:
                prev_vertex = labels[vertex]
                if graph.vertices[prev_vertex].getEdge(vertex, 0) - flow.get((prev_vertex, vertex), 0) > 0:
                    flow[(prev_vertex, vertex)] += mins
                elif flow.get((vertex, prev_vertex), 0) > 0:
                    flow[(vertex,prev_vertex)] -= mins
                vertex = prev_vertex
                cur_way.append(prev_vertex)
            print("Path: ", end='')
            for v in reversed(cur_way):
                print(v, end=' ')
            print('Flow:', mins)
    max_flow = 0
    for vertex, weight in graph.vertices[source].edges.items():
        max_flow += flow.get((source,vertex), 0)
    print("Max Flow:", max_flow)

def kruskal(graph):
    edges = {}
    colors = {}
    for i, k in enumerate(graph.vertices.keys()):
        colors[k] = i + 1
        for r, v in graph.vertices[k].edges.items():
            if (r,k) not in edges.keys():
                edges[(k,r)] = v
    edges = {edge: weight for edge, weight in sorted(edges.items(), key=lambda x: x[1])}
    weight_of_mst = 0
    for k in colors.keys():
        print(f'  {k}  ', end='|')
    print()
    for v in colors.values():
        print(f' {v:3} ', end='|')
    print()
    for edge, weight in edges.items():
        if colors[edge[0]] != colors[edge[1]]:
            weight_of_mst += weight
            old, new = min(colors[edge[0]], colors[edge[1]]), max(colors[edge[0]], colors[edge[1]])
            for v, k in colors.items():
                if k == old:
                    colors[v] = new
            for v in colors.values():
                print(f' {v:3} ', end='|')
            print(" Edge", edge, "=", weight)
        if list(colors.values()).count(list(colors.values())[0]) == len(colors.values()):
            break
    print("Minimum weight spanning tree:", weight_of_mst)

def prufer(graph, toCode = True, code = []):
    if toCode:
        if graph.is_oriented == True:
            raise GraphError("Algorithm Kosaraju: Graph is oriented")
        code = []
        while len(graph.vertices) > 2:
            for v in sorted(graph.vertices.keys(), key=lambda x: int(x)):
                if len(graph.vertices[v].edges) == 1:
                    print(f"Delete vertex {v}")
                    code.append(list(graph.vertices[v].edges.keys())[0])
                    graph.removeVertex(v)
                    break
        print('Code: ', end='')
        for c in code:
            print(c,end=' ')
        print()
    else:
        graph.clearEdges()
        vertices = sorted(list(graph.vertices.keys()), key=lambda x: int(x))
        while len(code) > 0:
            for vertex in vertices:
                if vertex not in code:
                    print('Add edge',(vertex, code[0]))
                    graph.addEdge((vertex, code[0]))
                    code.pop(0)
                    vertices.remove(vertex)
                    break
        print('Add edge', (vertices[0], vertices[1]))
        graph.addEdge((vertices[0], vertices[1]))
        graph.print()

if __name__ == "__main__":
    graph = Graph()
    graph.loadFromJSON("../graph.json")
    print("You have entered the following graph")
    graph.print()
    while True:
        print("Choose algorithm:")
        print("kos - Kosaraju-Sharir algorithm")
        print("pru - Prufer algorithm")
        print("kru - Kruskal algorithm")
        print("dij - Dijkstra algorithm")
        print("fl - Floyd algorithm")
        print("ford - Ford-Fulkerson algorithm (Max Flow)")
        s = input().split(' ')[0]
        if s == 'kos':
            print("\nKosaraju algorithm")
            kosaraju_sharir(graph)
            break
        if s == 'pru':
            print("\nPrufer algorithm")
            print("to - create code from graph")
            print("from - create graph from code")
            s = input().split(' ')[0]
            if s == 'to':
                prufer(graph)
            elif s == 'from':
                print('Enter code through a space')
                s = input().split(' ')
                prufer(graph, False, s)
            else:
                print('Wrong input')
            break
        if s == 'kru':
            print("\nKruskal algorithm")
            kruskal(graph)
            break
        elif s == 'dij':
            print("\nDijkstra algorithm")
            start = input("Enter start vertex ").split(' ')[0]
            dijkstra(graph, start)
            break
        elif s == 'fl':
            print("\nFloyd algorithm")
            floyd(graph)
            break
        elif s == 'ford':
            print("\nFord-Fulkerson algorithm (Max Flow)")
            vertices = input("Enter source and target through a space ").split(' ')
            max_flow(graph, vertices[0], vertices[1])
            break
        else:
            print("Wrong enter!")
