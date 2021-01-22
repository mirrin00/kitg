from graph import Graph
import algorithms

if __name__ == "__main__":
    graph = Graph()
    graph.loadFromJSON("graph.json")
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
            algorithms.kosaraju_sharir(graph)
            break
        if s == 'pru':
            print("\nPrufer algorithm")
            print("to - create code from graph")
            print("from - create graph from code")
            s = input().split(' ')[0]
            if s == 'to':
                algorithms.prufer(graph)
            elif s == 'from':
                print('Enter code through a space')
                s = input().split(' ')
                algorithms.prufer(graph, False, s)
            else:
                print('Wrong input')
            break
        if s == 'kru':
            print("\nKruskal algorithm")
            algorithms.kruskal(graph)
            break
        elif s == 'dij':
            print("\nDijkstra algorithm")
            start = input("Enter start vertex ").split(' ')[0]
            algorithms.dijkstra(graph, start)
            break
        elif s == 'fl':
            print("\nFloyd algorithm")
            algorithms.floyd(graph)
            break
        elif s == 'ford':
            print("\nFord-Fulkerson algorithm (Max Flow)")
            vertices = input("Enter source and target through a space ").split(' ')
            algorithms.max_flow(graph, vertices[0], vertices[1])
            break
        else:
            print("Wrong enter!")
