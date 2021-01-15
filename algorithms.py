from graph import GraphError

def kosaraju_sharir(graph):
    if graph.is_oriented == False:
        raise GraphError("Algorithm Kosaraju: Graph is not oriented")
    times = {}
    time = 0
    def find(node_name, times, time):
        times[node_name] = -1
        time += 1
        for node in graph.nodes[node_name].ribs.keys():
            if node in times.keys():
                continue
            time = find(node, times, time)
        time += 1
        times[node_name] = time
        return time
    for node in sorted(graph.nodes.keys()):
        if node not in times.keys():
            time = find(node, times, time)
    times = {k: v for k, v in sorted(times.items(), key=lambda item: item[1], reverse=True)}
    def find_components(node_name, comp, times):
        times[node_name] = -1
        comp.append(node_name)
        for node in times.keys():
            if times[node] != -1 and node_name in graph.nodes[node].ribs.keys():
                find_components(node, comp, times)
    components = []
    for node in times.keys():
        if times[node] != -1:
            component = []
            find_components(node, component, times)
            components.append(component)
    print("Result Kosaraju:")
    for comp in kosaraju(graph):
        print(comp)

def dijkstra(graph, start_node_name):
    for k in graph.nodes.keys():
        for r, v in graph.nodes[k].ribs.items():
            if v < 0:
                raise GraphError(f"Algorithm Dijsktra: Graph has negative rib")
    if start_node_name not in graph.nodes.keys():
        raise GraphError(f"Algorithm Dijsktra: Node {start_node_name} not in graph")
    start_node = graph.nodes[start_node_name]
    paths = {k: [start_node.getRib(k, -1), start_node_name] for k in sorted(graph.nodes.keys())}
    paths.pop(start_node_name)
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
        node = ''
        for node_name, path in paths.items():
            if path[0] != None and (path[0] < minimum or minimum == -1) and path[0] != -1:
                minimum = path[0]
                node = node_name
        if minimum == -1:
            break
        for node_name, len_node in graph.nodes[node].ribs.items():
            if node_name != start_node_name and paths[node_name][0] != None and (paths[node_name][0] > (minimum + len_node) or paths[node_name][0] == -1):
                paths[node_name] = [minimum + len_node, node]
        paths[node][0] = None
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
    keys = graph.nodes.keys()
    for k in keys:
        row = []
        node = graph.nodes[k]
        for col in keys:
            if k == col:
                row.append(0)
            else:
                row.append(node.getRib(col))
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
    if source not in graph.nodes.keys():
        raise GraphError(f"Algorithm Max Flow: No node {source} in graph")
    if target not in graph.nodes.keys():
        raise GraphError(f"Algorithm Max Flow: No node {target} in graph")
    for k in graph.nodes.keys():
        for r, v in graph.nodes[k].ribs.items():
            if v < 0:
                raise GraphError(f"Algorithm Max Flow: Graph has negative rib")
            flow[(k,r)] = 0
    while True:
        labels = {source: None}
        checked = [source]
        not_checked = list(graph.nodes.keys())
        not_checked.remove(source)
        for node_checked in checked:
            temp_checked = []
            for node in not_checked:
                if node in temp_checked:
                    continue
                if flow.get((node_checked, node), 0) < graph.nodes[node_checked].getRib(node, 0) or flow.get((node, node_checked), 0) > 0:
                    temp_checked.append(node)
                    labels[node] = node_checked
            checked.extend(temp_checked)
            for el in temp_checked:
                not_checked.remove(el)
        if target in not_checked:
            break
        else:
            mins = []
            node = target
            while node != source:
                prev_node = labels[node]
                if graph.nodes[prev_node].getRib(node, 0) - flow.get((prev_node, node), 0) > 0:
                    mins.append(graph.nodes[prev_node].getRib(node, 0) - flow.get((prev_node, node), 0))
                elif flow.get((node,prev_node),0) > 0:
                    mins.append(flow.get((node,prev_node),0))
                node = prev_node
            mins = min(mins)
            node = target
            while node != source:
                prev_node = labels[node]
                if graph.nodes[prev_node].getRib(node, 0) - flow.get((prev_node, node), 0) > 0:
                    flow[(prev_node, node)] += mins
                elif flow.get((node, prev_node), 0) > 0:
                    flow[(node,prev_node)] -= mins
                node = prev_node
    max_flow = 0
    for node, weight in graph.nodes[source].ribs.items():
        max_flow += flow.get((source,node), 0)
    print("Max Flow:", max_flow)

